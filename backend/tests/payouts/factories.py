from decimal import Decimal

import factory
from django.db.models import Model
from factory import fuzzy

from payouts.models import Currency, Payout


class CurrencyFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания тестовых объектов валют."""

    name: str = factory.Sequence(lambda n: f"Валюта {n}")
    code: str = factory.Iterator(("RUB", "USD", "EUR"))

    class Meta:
        model: type[Model] = Currency


class PayoutFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания тестовых объектов заявок на выплату денежных средств."""

    payment: Decimal = fuzzy.FuzzyDecimal(low=100.00, high=10000.00, precision=2)
    currency: Currency = factory.SubFactory(CurrencyFactory)
    bik: str = "123456789"
    correspondent_account: str = "12345678901234567890"
    bank_account_number: str = "98765432109876543210"

    class Meta:
        model: type[Model] = Payout
