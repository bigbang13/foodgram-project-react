from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscription
from .serializers import SubscriptionSerializer

User = get_user_model()


class SubscribeViewSet(UserViewSet):
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        hash_pwd = make_password(serializer.validated_data.get("password"))
        serializer.save(password=hash_pwd)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response({
                'errors': 'Нельзя подписываться на самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if Subscription.objects.filter(user=user, author=author).exists():
            return Response({
                'errors': 'Вы уже подписаны на данного пользователя'
            }, status=status.HTTP_400_BAD_REQUEST)

        subscribe = Subscription.objects.create(user=user, author=author)
        serializer = SubscriptionSerializer(
            subscribe, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response({
                'errors': 'Нельзя отписываться от самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        subscribe = Subscription.objects.filter(user=user, author=author)
        if not subscribe.exists():
            return Response({
                'errors': 'Вы не подписаны на этого автора'
            }, status=status.HTTP_400_BAD_REQUEST)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='subscribtions'
    )
    def subscriptions(self, request):
        subscriptions = User.objects.filter(following__user=self.request.user)
        page = self.paginate_queryset(subscriptions)
        serializer = SubscriptionSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
