from django.contrib.auth.hashers import check_password, make_password
from rest_framework import filters, generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import RetrieveDestroyAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAdminOrReadOnly, UserPermission
from .mixins import CreateDestroyListViewSet, CreateListViewSet
from .models import Subscription, User
from .serializers import (LoginSerializer, RegistrationSerializer,
                          SubscriptionSerializer, UserIDSerializer)
from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404


class UserAPIList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserIDSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        hash_pwd = make_password(serializer.validated_data.get("password"))
        serializer.save(password=hash_pwd)


class RegisterView(APIView):
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


class SubscriptionViewSet(ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(following__user=self.request.user)
        # queryset = queryset.filter(user=self.request.user)
        return queryset


class SubscribeViewSet(RetrieveDestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    pagination_class = LimitOffsetPagination

    def post(self, request, user_id):
        user = request.user
        author = get_object_or_404(User, id=user_id)
        if user == author:
            return Response({
                "errors": "Нельзя подписываться на себя"
            }, status=status.HTTP_400_BAD_REQUEST)
        if Subscription.objects.filter(user=user, author=author).exists():
            return Response({
                "errors": "Вы уже подписаны на этого пользователя"
            }, status=status.HTTP_400_BAD_REQUEST)
        subscribe = Subscription.objects.create(user=user, author=author)
        serializer = SubscriptionSerializer(
            subscribe, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#    def perform_create(self, serializer):
#        if serializer.is_valid():
#            serializer.save(
#                user=self.request.user,
#            )

#   @action(
#       methods=["get"],
#       url_path="subscriptions",
#       detail=False,
#       permission_classes=[IsAuthenticated],
#   )
#   def subscriptions(self, request):
#       # queryset = self.request.user.follower
#       user = request.user
#       queryset = Subscription.objects.filter(user=user)
#       pages = self.paginate_queryset(queryset)
#       serializer = SubscriptionSerializer(
#           pages,
#           many=True,
#           context={'request': request}
#       )
#       return self.get_paginated_response(serializer.data)
