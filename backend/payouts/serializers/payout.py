from django.db.models import Model
from rest_framework import serializers

from payouts.models import Currency, Payout


class PayoutListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка заявок на выплату денежных средств."""

    currency: str = serializers.SlugRelatedField(slug_field="code", queryset=Currency.objects.all())

    class Meta:
        model: type[Model] = Payout
        fields: tuple[str, ...] = (
            "id",
            "status",
            "payment",
            "currency",
            "description",
            "created_at",
        )


class PayoutRetrieveSerializer(PayoutListSerializer):
    """Сериализатор для заявки на выплату денежных средств."""

    class Meta(PayoutListSerializer.Meta):
        fields: tuple[str, ...] = (
            *PayoutListSerializer.Meta.fields,
            "bik",
            "correspondent_account",
            "bank_account_number",
            "updated_at",
        )


class PayoutUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления заявки на выплату денежных средств."""

    class Meta:
        model: type[Model] = Payout
        fields: tuple[str, ...] = ("status", "description")
