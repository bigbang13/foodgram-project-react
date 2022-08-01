from django.contrib.auth.tokens import PasswordResetTokenGenerator
from djoser.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User
