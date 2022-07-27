from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet, NumberFilter)
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView, RetrieveAPIView

from recipes.models import Ingredient, Recipe, Tag
from users.models import User

from api.permissions import IsAdminOrReadOnly, UserPermission
from .serializers import (RegistrationSerializer, UserSerializer, UserIDSerializer, LoginSerializer, PasswordChangeSerializer)


class RegisterView(APIView):
    """
    Анонимный пользователь высылает JSON c данными для регистрации.
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = RegistrationSerializer(users, many=True)
        return Response(serializer.data)
               

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                **serializer.validated_data, role="user"
            )
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserMeView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserIDSerializer

    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

class UserIDView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserIDSerializer

    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(
            User,
            id=self.kwargs["user_id"],
        )


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            user = User.objects.filter(email=email).first()
            return Response(
                self.get_token_for_user(user), status.HTTP_200_OK
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "auth_token": str(refresh.access_token),
        }

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.access_token.delete()
        return Response(status.HTTP_200_OK)


class PasswordChangeView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer
    model = User

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            current_password = serializer.data.get("current_password")
            new_password = serializer.data.get("new_password")
            if not request.user.password == current_password:
                return Response("Неверный пароль", status.HTTP_400_BAD_REQUEST)
            request.user.password = new_password
            request.user.save()
            return Response("Password change successfully", status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
