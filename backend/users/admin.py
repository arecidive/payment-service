from typing import Optional

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Административная панель для работы с пользователями."""

    list_display: tuple[str, ...] = ("username", "is_superuser")
    search_fields: tuple[str, ...] = ("username",)
    list_filter: tuple[str, ...] = ()

    fieldsets: tuple[tuple[Optional[str], dict[str, tuple[str, ...]]]] = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    add_fieldsets: tuple[tuple[Optional[str], dict[str, tuple[str, ...]]]] = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
