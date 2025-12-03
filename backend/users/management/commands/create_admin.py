from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from users.models import User


class Command(BaseCommand):
    """Команда для создания администратора."""

    help: str = "Создание администратора с указанным именем и паролем"

    def add_arguments(self, parser: CommandParser) -> None:
        """Определение аргументов командной строки."""
        parser.add_argument("--username", type=str, required=True, help="Имя")
        parser.add_argument("--password", type=str, required=True, help="Пароль")

    def handle(self, *_: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """Выполнение команды создания администратора."""
        username: str = kwargs.get("username")
        password: str = kwargs.get("password")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Пользователь {username} уже существует"))
            return

        User.objects.create_superuser(username=username, password=password)
        self.stdout.write(self.style.SUCCESS(f"Администратор {username} успешно создан"))
