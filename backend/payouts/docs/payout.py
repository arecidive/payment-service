from typing import Callable

from drf_spectacular.utils import extend_schema, extend_schema_view

TAGS: list[str] = ["Платежи | Заявки на выплату денежных средств"]

payout_schema: Callable = extend_schema_view(
    list=extend_schema(
        tags=TAGS,
        summary="Список заявок на выплату денежных средств",
        description="Эндпоинт для вывода списка заявок на выплату денежных средств."
    ),
    retrieve=extend_schema(
        tags=TAGS,
        summary="Получение заявки на выплату денежных средств",
        description=(
            "Эндпоинт для получение детальной информации о заявке на "
            "выплату денежных средств."
        ),
    ),
    create=extend_schema(
        tags=TAGS,
        summary="Создание заявки на выплату денежных средств",
        description=(
            "Эндпоинт для создания заявки на выплату денежных средств "
            "с отправкой заявки на обработку."
        ),
    ),
    partial_update=extend_schema(
        tags=TAGS,
        summary="Обновление заявки на выплату денежных средств",
        description="Эндпоинт для обновления заявки на выплату денежных средств.",
    ),
    destroy=extend_schema(
        tags=TAGS,
        summary="Удаление заявки на выплату денежных средств",
        description=(
            "Эндпоинт для удаления заявки на выплату денежных средств. "
            "Возможно удаление только тех заявок, которые еще не начали "
            "обрабатываться или отменены."
        ),
    ),
)
