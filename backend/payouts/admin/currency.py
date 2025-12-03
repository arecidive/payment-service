from django.contrib import admin

from payouts.models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """Административная панель для работы с валютами."""

    list_display: tuple[str, ...] = ("name", "code")
    search_fields: tuple[str, ...] = ("name",)
