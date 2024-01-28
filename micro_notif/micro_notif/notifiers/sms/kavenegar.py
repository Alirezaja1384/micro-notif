import logging
from typing import cast
from decouple import config
from aio_kavenegar import AIOKavenegarAPI, APIException, HTTPException

from .base import AbstractSMSNotifier


logger = logging.getLogger(__name__)


KAVENEGAR_API_KEY = cast(str, config("KAVENEGAR_API_KEY"))
KAVENEGAR_SENDER = cast(str, config("KAVENEGAR_SENDER"))


class KavenegarSMSNotifier(AbstractSMSNotifier):
    _api_key: str
    _sender: str
    _client: AIOKavenegarAPI

    def __init__(self):
        self._api_key = KAVENEGAR_API_KEY
        self._sender = KAVENEGAR_SENDER
        self._client = AIOKavenegarAPI(apikey=self._api_key)

    async def send(self, to: str, message: str) -> bool:
        try:
            await self._client.sms_send(
                {"receptor": to, "sender": self._sender, "message": message}
            )
            return True

        except (APIException, HTTPException) as e:
            logger.exception(e)
            return False
