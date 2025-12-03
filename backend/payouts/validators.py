from django.core.exceptions import ValidationError


def validate_digits(value: str) -> None:
    """Валидация, что в переданном значении только цифры."""
    if not value.isdigit():
        raise ValidationError("В переданном значении могут быть только цифры")
