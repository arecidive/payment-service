from datetime import datetime
from decimal import Decimal

from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models

from payouts.constants import PayoutStatuses
from payouts.validators import validate_digits


class Payout(models.Model):
    """Модель для хранения заявок на выплату денежных средств."""

    status: str = models.CharField(
        verbose_name="Статус заявки",
        max_length=20,
        choices=PayoutStatuses.choices,
        default=PayoutStatuses.PENDING,
        db_index=True,
    )
    payment: Decimal = models.DecimalField(
        verbose_name="Сумма выплаты",
        max_digits=15,
        decimal_places=2,
        validators=(MinValueValidator(0.01), MaxValueValidator(100_000_000.00)),
    )
    currency: models.Model = models.ForeignKey(
        verbose_name="Валюта",
        to="payouts.Currency",
        on_delete=models.PROTECT,
        db_index=True,
    )
    description: str = models.TextField(
        verbose_name="Описание",
        blank=True,
        validators=(MaxLengthValidator(2_000),)
    )

    # Реквизиты выплаты денежных средств по заявке
    bik: str = models.CharField(
        verbose_name="БИК банка получателя",
        max_length=9,
        validators=(MinLengthValidator(9), validate_digits),
    )
    correspondent_account: str = models.CharField(
        verbose_name="Корреспондентский счёт получателя",
        max_length=20,
        validators=(MinLengthValidator(20), validate_digits),
    )
    bank_account_number: str = models.CharField(
        verbose_name="Номер банковского счёта получателя",
        max_length=20,
        validators=(MinLengthValidator(20), validate_digits),
    )

    created_at: datetime = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        db_index=True,
    )
    updated_at: datetime = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    class Meta:
        verbose_name: str = "Заявка на выплату денежных средств"
        verbose_name_plural: str = "Заявки на выплату денежных средств"
        ordering: tuple[str, ...] = ("-created_at",)

    def __str__(self) -> str:
        return f"{self._meta.verbose_name} № {self.pk}"
