from unittest.mock import Mock, patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from payouts.constants import PayoutStatuses
from payouts.models import Currency, Payout
from tests.payouts.factories import CurrencyFactory, PayoutFactory


@pytest.mark.django_db
class TestPayoutViewSet(APITestCase):
    """Класс для тестирования API для управления заявками на выплату денежных средств."""

    list_url: str = reverse("payouts-list")

    def test_list(self) -> None:
        """Тест для проверки получения списка заявок."""
        payouts: list[Payout] = PayoutFactory.create_batch(size=2)

        with self.assertNumQueries(1):
            response: Response = self.client.get(self.list_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(payouts)

    def test_retrieve(self) -> None:
        """Тест для проверки получения конкретной заявки."""
        payout: Payout = PayoutFactory()

        with self.assertNumQueries(1):
            response: Response = self.client.get(
                path=reverse("payouts-detail", kwargs={"pk": payout.id}),
            )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == payout.id

    @patch("payouts.viewsets.payout.process_payout_task.delay")
    def test_create(self, mock_task: Mock) -> None:
        """Тест для проверки создания заявки с вызовом задачи на обработку заявки."""
        currency: Currency = CurrencyFactory()

        data: dict[str, str] = {
            "payment": "1000.00",
            "currency": currency.code,
            "description": "Тестовая заявка",
            "bik": "123456789",
            "correspondent_account": "12345678901234567890",
            "bank_account_number": "98765432109876543210",
        }

        with self.assertNumQueries(2):
            response: Response = self.client.post(self.list_url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Payout.objects.count() == 1
        assert mock_task.call_count == 1

    def test_partial_update_payout(self) -> None:
        """Тест для проверки частичного обновления конкретной заявки."""
        payout: Payout = PayoutFactory(status=PayoutStatuses.PROCESSING)

        data: dict[str, str] = {
            "status": PayoutStatuses.APPROVED,
        }

        with self.assertNumQueries(2):
            response: Response = self.client.patch(
                path=reverse("payouts-detail", kwargs={"pk": payout.id}),
                data=data,
                format="json",
            )
        payout.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == payout.status

    def test_destroy(self) -> None:
        """Тест для проверки удаления заявки."""
        payout: Payout = PayoutFactory(status=PayoutStatuses.PENDING)

        with self.assertNumQueries(2):
            response: Response = self.client.delete(
                path=reverse("payouts-detail", kwargs={"pk": payout.id}),
            )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Payout.objects.count() == 0

    def test_destroy__with_not_allowed_status(self) -> None:
        """Тест для проверки удаления заявки с неразрешенным статусом."""
        payout: Payout = PayoutFactory(status=PayoutStatuses.APPROVED)

        with self.assertNumQueries(1):
            response: Response = self.client.delete(
                path=reverse("payouts-detail", kwargs={"pk": payout.id}),
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND
