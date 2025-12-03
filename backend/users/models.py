from typing import Any

from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Класс-менеджер для работы с пользователем."""

    def _create_user(self, username: str, password: str, **kwargs: dict[str, Any]) -> AbstractUser:
        """Создание пользователя с указанным именем и паролем."""
        if not username:
            raise ValueError("Необходимо указать имя")

        GlobalUserModel: AbstractUser = apps.get_model(
            self.model._meta.app_label,
            self.model._meta.object_name,
        )

        username: str = GlobalUserModel.normalize_username(username)
        user: AbstractUser = self.model(username=username, **kwargs)
        user.password = make_password(password)

        user.save(using=self._db)
        return user

    def create_user(
        self,
        username: str,
        password: str | None = None,
        **kwargs: dict[str, Any],
    ) -> AbstractUser:
        """Создание пользователя."""
        kwargs.update(is_staff=False, is_superuser=False)
        return self._create_user(username, password, **kwargs)

    def create_superuser(
        self,
        username: str,
        password: str | None = None,
        **kwargs: dict[str, Any],
    ) -> AbstractUser:
        """Создание администратора."""
        kwargs.update(is_staff=True, is_superuser=True)
        return self._create_user(username, password, **kwargs)


class User(AbstractUser):
    """Модель для хранения пользователя."""

    REQUIRED_FIELDS: list[str] = []

    objects: models.Manager = UserManager()

    class Meta:
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"

    def __str__(self) -> str:
        return self.username
