from django.db.models import TextChoices


class PayoutStatuses(TextChoices):
    """Класс для хранения констант статусов заявки на выплату денежных средств."""

    PENDING: tuple[str, str] = "pending", "Ожидает обработки"
    PROCESSING: tuple[str, str] = "processing", "В обработке"
    APPROVED: tuple[str, str] = "approved", "Одобрена"
    REJECTED: tuple[str, str] = "rejected", "Отклонена"
    PAID: tuple[str, str] = "paid", "Выплачена"
    CANCELED: tuple[str, str] = "canceled", "Отменена"

    @classmethod
    def allowed_delete_statuses(cls: type["PayoutStatuses"]) -> tuple[str, ...]:
        """Получение статусов, с которыми можно удалить заявку на выплату денежных средств."""
        return cls.PENDING, cls.CANCELED

    @classmethod
    def allowed_process_statuses(cls: type["PayoutStatuses"]) -> tuple[str, ...]:
        """Получение статусов, с которыми можно обработать заявку на выплату денежных средств."""
        return cls.PENDING, cls.PROCESSING
