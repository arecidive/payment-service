from django.db.models import QuerySet
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from payouts.constants import PayoutStatuses
from payouts.docs import payout_schema
from payouts.models import Payout
from payouts.serializers import (
    PayoutListSerializer,
    PayoutRetrieveSerializer,
    PayoutUpdateSerializer,
)
from payouts.tasks import process_payout_task


@payout_schema
class PayoutViewSet(viewsets.ModelViewSet):
    """API для управления заявками на выплату денежных средств."""

    http_method_names: tuple[str, ...] = (
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
    )

    def get_queryset(self) -> QuerySet:
        """Получение QuerySet для заявок на выплату денежных средств в зависимости от действия.

        Удалению подлежат заявки, которые имеют статус 'PayoutStatuses.PENDING' или
        'PayoutStatuses.CANCELLED'.
        """
        queryset: QuerySet = Payout.objects.select_related("currency")
        return (
            queryset.filter(status__in=PayoutStatuses.allowed_delete_statuses())
            if self.action == "destroy"
            else queryset
        )

    def get_serializer_class(self) -> BaseSerializer:
        """Получение сериализатора в зависимости от действия."""
        if self.action == self.list.__name__:
            return PayoutListSerializer
        if self.action == self.partial_update.__name__:
            return PayoutUpdateSerializer
        return PayoutRetrieveSerializer

    def create(self, request: Request) -> Response:
        """Создание заявки на выплату денежных средств с запуском обработки заявки."""
        serializer: BaseSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment: Payout = serializer.save()
        process_payout_task.delay(payment.id)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data),
        )
