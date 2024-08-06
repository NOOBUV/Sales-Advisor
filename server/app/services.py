from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from rest_framework.authtoken.models import Token
from .models import Organization
from .exceptions import UserCreationError, AuthenticationError