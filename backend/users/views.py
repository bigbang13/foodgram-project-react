from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet, NumberFilter)
from rest_framework import filters, status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password

from .models import User

from api.permissions import IsAdminOrReadOnly, UserPermission
from .serializers import (RegistrationSerializer, UserIDSerializer, LoginSerializer, PasswordChangeSerializer)



class UserAPIList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserIDSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination


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
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class LoginView(ObtainAuthToken):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data.get("password")
        email = serializer.data.get("email")
        user = User.objects.filter(email=email).first()
        if not check_password(password, user.password):
            return Response("Неверный пароль", status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"auth_token": token.key}, status.HTTP_200_OK)
        # return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer
    model = User

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            current_password = serializer.data.get("current_password")
            new_password = serializer.data.get("new_password")
            # if not request.user.password == current_password:
            #    return Response("Неверный пароль", status.HTTP_400_BAD_REQUEST)
            z = (request.user.check_password(current_password))
            #    return Response("Неверный пароль", status.HTTP_400_BAD_REQUEST)
            # request.user.password = new_password
            # request.user.save()
            # return Response("dsaf", status.HTTP_204_NO_CONTENT)
            return Response("dsaf", status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
