from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ("user", "user"),
    ("admin", "admin"),
)


class User(AbstractUser):
    email = models.EmailField(
        "Адрес электронной почты",
        max_length=254,
    )
    username = models.CharField(
        "Уникальный юзернейм",
        unique=True,
        max_length=150,
    )
    first_name = models.CharField(
        "Имя",
        max_length=150,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=150,
    )
    password = models.CharField(
        "Пароль",
        max_length=150,
    )
    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        default="user",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
       User, on_delete=models.CASCADE, related_name='follower'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'], name='author_follow'
            ),
        ]