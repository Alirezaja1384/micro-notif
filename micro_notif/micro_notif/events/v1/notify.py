import logging

from aio_pika import ExchangeType
from aio_pika.abc import AbstractChannel, AbstractIncomingMessage
from pydantic import ValidationError
from micro_notif.schemas.sms import SMSEvent
from micro_notif.settings import RABBITMQ_EXCHANGE
from micro_notif.notifiers import get_sms_notifier
from micro_notif.utils import mask_str

BASE_ROUTING_KEY = "micro_notif.v1.notify"

logger = logging.getLogger(__name__)
sms_notifier = get_sms_notifier()


async def handle_sms_notification(message: AbstractIncomingMessage):
    if not sms_notifier:
        await message.reject()
        logger.warning("SMS message rejected - SMS notifier not configured!")
        return

    try:
        sms = SMSEvent.model_validate_json(message.body.decode())
    except ValidationError as e:
        logger.exception(e)
        await message.reject()
        logger.error("SMS message rejected - JSON validation failed!")
        return

    masked_to = mask_str(sms.to, from_index=4, to_index=8)

    if not await sms_notifier.send(to=sms.to, message=sms.message):
        await message.reject()
        logger.error(
            'SMS message rejected - Sending SMS to "%s" failed!', masked_to
        )
        return

    logger.debug('SMS message sent to "%s" successfully!', masked_to)
    await message.ack()


async def listen_for_events(channel: AbstractChannel):
    notif_handlers = {
        "sms": handle_sms_notification,
    }

    exchange = await channel.declare_exchange(
        name=RABBITMQ_EXCHANGE, type=ExchangeType.DIRECT
    )

    for notif_type, handler in notif_handlers.items():
        routing_key = f"{BASE_ROUTING_KEY}.{notif_type}"

        queue = await channel.declare_queue(routing_key)

        await queue.bind(exchange=exchange.name, routing_key=routing_key)
        await queue.consume(handler)
