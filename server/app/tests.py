from django.test import TestCase

# Create your tests here.
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Chat, Organization

class SignupViewTests(APITestCase):
    
    def test_signup_success(self):
        url = reverse('signup')
        data = {
            'organization': 'TestOrg',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(Organization.objects.count(), 1)

class LoginViewTests(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
    
    def test_login_success(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_login_failure(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class LogoutViewTests(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_logout(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(user=self.user)

from unittest.mock import patch
import json
import pandas as pd

class QueryViewTests(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    @patch('app.utils.chat_with_groq')
    @patch('app.utils.execute_duckdb_query')
    @patch('app.utils.get_summarization')
    def test_query_success(self, mock_get_summarization, mock_execute_duckdb_query, mock_chat_with_groq):
        # Mock the responses from Groq API and other functions
        mock_chat_with_groq.return_value = json.dumps({
            'sql': 'SELECT * FROM some_table'
        })
        mock_execute_duckdb_query.return_value = pd.DataFrame({
            'column1': [1, 2],
            'column2': ['value1', 'value2']
        })
        mock_get_summarization.return_value = 'Summary of the results'

        url = reverse('query')
        data = {
            'question': 'What is the total revenue?'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question'], data['question'])
        self.assertEqual(response.data['summary'], 'Summary of the results')

    def test_query_missing_question(self):
        url = reverse('query')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'No question provided'})

class ChatViewSetTests(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.organization = Organization.objects.create(name='TestOrg')
        self.chat = Chat.objects.create(
            user=self.user,
            organization=self.organization,
            message='What is the total revenue?',
            response='The total revenue is $1000.'
        )
    
    def test_list_chats(self):
        url = reverse('chat-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question'], self.chat.message)
        self.assertEqual(response.data[0]['summary'], self.chat.response)

class UserDetailsViewTests(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_user_details(self):
        url = reverse('user-details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['is_admin'], self.user.is_admin)
