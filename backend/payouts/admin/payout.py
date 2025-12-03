from django.contrib import admin

from payouts.models import Payout


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    """Административная панель для работы с заявками на выплату денежных средств."""

    list_display: tuple[str, ...] = ("id", "status", "payment", "currency", "created_at")
    list_select_related: tuple[str, ...] = ("currency",)
    list_filter: tuple[str, ...] = ("status", "created_at")
    search_fields: tuple[str, ...] = (
        "bik",
        "correspondent_account",
        "bank_account_number",
        "description",
    )
    readonly_fields: tuple[str, ...] = ("created_at", "updated_at")
