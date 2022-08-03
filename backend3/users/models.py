from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class FoodgramUserManager(UserManager):
    def create_user(self, email, username, first_name,
                    last_name, password=None):
        if not email:
            raise ValueError("Должен быть e-mail")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        # password_hash = user.make_password(password, None, "pbkdf2_sha256")
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name,
                         last_name, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(
        "Адрес электронной почты",
        unique=True,
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
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name", "password")

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name}  {self.last_name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
