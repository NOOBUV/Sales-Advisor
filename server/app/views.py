from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Organization, Database, Chat
from .serializers import UserSerializer, DatabaseSerializer, ChatSerializer
from .utils import chat_with_groq, execute_duckdb_query, get_summarization
from groq import Groq
import json, os, sqlparse
from django.utils.decorators import method_decorator

# Signup view
class SignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    @extend_schema(
        request=UserSerializer,
        responses={status.HTTP_201_CREATED: UserSerializer},
        summary='Register a new user',
        description='Create a new user with an associated organization. The organization is created if it does not already exist.'
    )
    def create(self, request, *args, **kwargs):
        org_name = request.data.get('organization')
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Ensure the organization is created
        organization, created = Organization.objects.get_or_create(name=org_name)

        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'is_admin': created,
            'organization': organization.pk
        }

        user_serializer = self.get_serializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

# Login view
class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request={
            'type': 'object',
            'properties': {
                'username': {'type': 'string'},
                'password': {'type': 'string'}
            }
        },
        responses={
            status.HTTP_200_OK: {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string'},
                    'is_admin': {'type': 'boolean'}
                }
            },
            status.HTTP_401_UNAUTHORIZED: OpenApiParameter(name='error', description='Error message', type='string')
        },
        summary='Login a user',
        description='Authenticate a user and return an authentication token along with the user’s admin status.'
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        User = get_user_model()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': "User doesn't exist"}, status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'is_admin': user.is_admin
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Logout view
class LogoutView(generics.GenericAPIView):
    
    @extend_schema(
        responses={status.HTTP_204_NO_CONTENT: None},
        summary='Logout a user',
        description='Log out the user by deleting their authentication token.'
    )
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@method_decorator(csrf_exempt, name='dispatch')
class QueryView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    @extend_schema(
        request={
            'type': 'object',
            'properties': {
                'question': {'type': 'string'}
            },
            'required': ['question']
        },
        responses={
            status.HTTP_200_OK: {
                'type': 'object',
                'properties': {
                    'question': {'type': 'string'},
                    'summary': {'type': 'string'}
                }
            },
            status.HTTP_400_BAD_REQUEST: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'details': {'type': 'string', 'description': 'Additional error details'}
                }
            }
        },
        summary='Query the database',
        description='Submit a question to be processed and generate a SQL query. The response includes the summarized results based on the query.'
    )

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        user_question = data.get('question')

        if not user_question:
            return JsonResponse({'error': 'No question provided'}, status=400)

        # Load the base prompt
        with open('./app/templates/prompts/base_prompt.txt', 'r') as file:
            base_prompt = file.read()

        # Generate the full prompt for the AI
        full_prompt = base_prompt.format(user_question=user_question)

        # Get the Groq API key and create a Groq client
        groq_api_key = os.getenv('GROQ_API_KEY')
        client = Groq(api_key=groq_api_key)
        model = "llama3-70b-8192"

        # Get the AI's response
        llm_response = chat_with_groq(client, full_prompt, model, {"type": "json_object"})
        result_json = json.loads(llm_response)

        if 'sql' in result_json:
            sql_query = result_json['sql']
            results_df = execute_duckdb_query(sql_query)

            formatted_sql_query = sqlparse.format(sql_query, reindent=True, keyword_case='upper')
            summarization = get_summarization(client, user_question, results_df, model)

            # Create a new chat entry
            chat_data = {
                'user': request.user.id,
                'organization': request.user.organization.id,
                'message': user_question,
                'response': summarization
            }
            serializer = self.get_serializer(data=chat_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            response = {
                'question': user_question,
                'summary': summarization
            }
        elif 'error' in result_json:
            response = {'error': 'Could not generate valid SQL for this question', 'details': result_json['error']}
        else:
            response = {'error': 'Unexpected response format'}

        return JsonResponse(response)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, organization=self.request.user.organization)

class ChatViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            status.HTTP_200_OK: ChatSerializer(many=True)
        },
        summary='List chat messages',
        description='Retrieve a list of chat messages related to the user’s organization.'
    )
    def get_queryset(self):
        return Chat.objects.filter(organization=self.request.user.organization)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        chats = [{
            'question': chat.message,
            'summary': chat.response
        } for chat in queryset]
        return Response(chats)

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            status.HTTP_200_OK: {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'is_admin': {'type': 'boolean'}
                }
            }
        },
        summary='Get user details',
        description='Retrieve details about the authenticated user, including username and admin status.'
    )
    def get(self, request):
        return Response({
            'username': request.user.username,
            'is_admin': request.user.is_admin
        })


# # To Do: Have to implement this functionality in future where user will be able to connect the sql db
# # Database create/update view
# class DatabaseCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = DatabaseSerializer

#     @extend_schema(
#         request=DatabaseSerializer,
#         responses={status.HTTP_201_CREATED: DatabaseSerializer, status.HTTP_200_OK: DatabaseSerializer},
#         summary='Create or update a database',
#         description='Allows an admin user to create or update a database associated with their organization.'
#     )
#     def get_queryset(self):
#         # Only allow access to databases associated with the user's organization
#         return Database.objects.filter(organization=self.request.user.organization)

#     def perform_create(self, serializer):
#         # Ensure the user is an admin before creating a database
#         if self.request.user.is_admin:
#             # Check if organization pk is provided in the request data
#             org_pk = self.request.data.get('organization')
#             if org_pk is None:
#                 # If not provided, use the user's organization
#                 organization = self.request.user.organization
#             else:
#                 # If provided, fetch the organization by pk
#                 organization = Organization.objects.get(pk=org_pk)

#             serializer.save(organization=organization)
#         else:
#             raise PermissionDenied("You do not have permission to create a database.")

#     def perform_update(self, serializer):
#         # Ensure the user is an admin before updating a database
#         if self.request.user.is_admin:
#             serializer.save()
#         else:
#             raise PermissionDenied("You do not have permission to update this database.")