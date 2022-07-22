from django.contrib.auth.models import AbstractUser
from django.db import models

# Add later validation for username
class User(AbstractUser):
    email = models.EmailField(
        "Адрес электронной почты",
        max_length=254,
    ),
    username = models.CharField(
        "Уникальный юзернейм",
        max_length=150,
    ),
    first_name = models.CharField(
        "Имя",
        max_length=150,
    ),
    last_name = models.CharField(
        "Фамилия",
        max_length=150,
    ),
    password = models.CharField(
        "Пароль",
        max_length=150,
    )
