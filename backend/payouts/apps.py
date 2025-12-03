from django.apps import AppConfig


class PayoutsConfig(AppConfig):
    """Конфигурация для функционала платежей."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "payouts"
    verbose_name: str = "Платежи"
