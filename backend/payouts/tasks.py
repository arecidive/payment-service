import logging
import random
import time

from celery import shared_task

from payouts.constants import PayoutStatuses
from payouts.models import Payout

logger: logging.Logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def process_payout_task(self, payout_id: int) -> None:
    """Задача для обработки заявки на выплату, если заявка существует и имеет статус обработки."""
    payout: Payout | None = Payout.objects.filter(id=payout_id).first()
    if not payout:
        msg: str = f"Заявка с ID '{payout_id}' не найдена"
        logger.warning(msg)
        return

    if payout.status not in PayoutStatuses.allowed_process_statuses():
        msg: str = f"Заявка с ID '{payout_id}' уже была обработана или отменена"
        logger.warning(msg)
        return

    if payout.status != PayoutStatuses.PROCESSING:
        payout.status = PayoutStatuses.PROCESSING
        payout.save(update_fields=("status", "updated_at"))

    try:
        # Имитация запроса к стороннему серверу
        time.sleep(2)

        # Имитация ответа от стороннего сервера
        is_approved: bool = random.choice((True, False))

        if is_approved:
            payout.status = PayoutStatuses.APPROVED
            logger.info(f"Заявка с ID '{payout_id}' одобрена")
        else:
            payout.status = PayoutStatuses.REJECTED
            logger.info(f"Заявка с ID '{payout_id}' отклонена")

        payout.save(update_fields=("status", "updated_at"))

    except Exception as exc:
        msg: str = f"Ошибка при обработке заявки с ID '{payout_id}': {str(exc)}"
        logger.error(msg, exc_info=True)
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc, countdown=60)
