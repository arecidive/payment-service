from django.apps import AppConfig


class CommonConfig(AppConfig):
    """Конфигурация для общего функционала приложения."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "common"
    verbose_name: str = "Конфигурация для общего функционала"
