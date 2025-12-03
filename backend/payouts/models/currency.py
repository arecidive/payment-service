from django.db import models


class Currency(models.Model):
    """Класс для хранения валюты."""

    name: str = models.CharField(verbose_name="Название", max_length=100)
    code: str = models.CharField(
        verbose_name="Код",
        unique=True,
        max_length=3,
        help_text="Код в формате ISO 4217",
    )

    class Meta:
        verbose_name: str = "Валюта"
        verbose_name_plural: str = "Валюты"

    def __str__(self) -> str:
        return self.name
