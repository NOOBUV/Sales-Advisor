from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from .models import Organization, User, Database
from .serializers import UserSerializer, DatabaseSerializer

class SignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        org_name = request.data.get('organization')
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Ensure the organization is created
        organization, created = Organization.objects.get_or_create(name=org_name)

        print(f"Organization created: {created}, ID: {organization.id}")

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

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        print(username)
        print(password)
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': "User doesn't exist"}, status=status.HTTP_401_UNAUTHORIZED)
        print(user)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DatabaseCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DatabaseSerializer

    def get_queryset(self):
        # Only allow access to databases associated with the user's organization
        return Database.objects.filter(organization=self.request.user.organization)

    def perform_create(self, serializer):
        # Ensure the user is an admin before creating a database
        if self.request.user.is_admin:
            # Check if organization pk is provided in the request data
            org_pk = self.request.data.get('organization')
            if org_pk is None:
                # If not provided, use the user's organization
                organization = self.request.user.organization
            else:
                # If provided, fetch the organization by pk
                organization = Organization.objects.get(pk=org_pk)

            serializer.save(organization=organization)
        else:
            raise PermissionDenied("You do not have permission to create a database.")

    def perform_update(self, serializer):
        # Ensure the user is an admin before updating a database
        if self.request.user.is_admin:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this database.")
        