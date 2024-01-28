import asyncio

import logging
import aio_pika
from aio_pika.abc import AbstractConnection

from micro_notif.settings import RABBITMQ_CONN_STR
from . import notify

logger = logging.getLogger(__name__)
EVENT_LISTENERS = [notify.listen_for_events]


class AIOPikaConnectionProvider:
    connection_string: str
    connection: AbstractConnection | None = None

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string

    async def get_connection(self) -> AbstractConnection:
        if not self.connection or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(
                self.connection_string
            )

        return self.connection

    async def close_connection(self) -> None:
        if not self.connection:
            raise ValueError("Connection not initialize!")

        if not self.connection.is_closed:
            await self.connection.close()


connection_provider = AIOPikaConnectionProvider(
    connection_string=RABBITMQ_CONN_STR
)


get_pika_connection = connection_provider.get_connection


async def on_startup():
    connection = await connection_provider.get_connection()

    if EVENT_LISTENERS:
        channel = await connection.channel()

        logger.info("Registering V1 event listeners...")

        # Register all event listeners
        await asyncio.gather(
            *[
                event_listener(channel=channel)
                for event_listener in EVENT_LISTENERS
            ]
        )

        logger.info("V1 event listeners registered successfully!")


async def on_shutdown():
    await connection_provider.close_connection()


__all__ = [
    "notify",
    "get_pika_connection",
    "on_startup",
    "on_shutdown",
]
