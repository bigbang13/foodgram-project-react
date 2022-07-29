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

from recipes.models import Ingredient, Recipe, Tag
from users.models import User

from .mixins import CreateListDestroyViewSet
from .permissions import IsAdminOrReadOnly, IsAuthorOrStaff, UserPermission
from .serializers import (CustomTokenObtainSerializer, IngredientSerializer,
                          RecipeSerializer, SignUpSerializer, TagSerializer,
                          UserMeSerializer, UserSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = TitleFilter

    # def get_serializer_class(self):
    #    if self.action in ["list", "retrieve"]:
    #        return TitleSerializer
    #    return TitlePostSerializer


class TagViewSet(CreateListDestroyViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class IngredientViewSet(CreateListDestroyViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = "slug"
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class SignUpAPIView(APIView):
    """
    Анонимный пользователь высылает JSON c "email" и "username".
    В ответ на почту получает confirmation_code.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if User.objects.filter(
            email=request.data.get("email"),
            username=request.data.get("username"),
        ).exists():
            user = User.objects.get(username=request.data.get("username"))
        if serializer.is_valid():
            user = User.objects.create(
                **serializer.validated_data, role="user"
            )
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        self.send_token(user, request.data.get("email"))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def send_token(self, user, email):
        send_mail(
            "Confirmation code for receiving a token",
            PasswordResetTokenGenerator().make_token(user),
            settings.ADMIN_MAIL,
            [email],
            fail_silently=False,
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    pagination_class = LimitOffsetPagination
    lookup_field = "username"

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated],
        url_path="me",
    )
    def get_me(self, request):
        if request.method == "GET":
            user = User.objects.get(username=request.user.username)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserMeSerializer(
                user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class CustomTokenObtainView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CustomTokenObtainSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=serializer.data.get("username")
            )
            return Response(
                self.get_tokens_for_user(user), status.HTTP_200_OK
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "token": str(refresh.access_token),
        }
