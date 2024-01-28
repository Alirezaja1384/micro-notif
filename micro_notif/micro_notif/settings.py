from typing import cast
from decouple import config

DEBUG = cast(bool, config("DEBUG", cast=bool, default=False))
RABBITMQ_EXCHANGE = cast(str, config("RABBITMQ_EXCHANGE"))
RABBITMQ_CONN_STR = cast(str, config("RABBITMQ_CONN_STR"))

SMS_NOTIFIER_CLS = cast(str | None, config("SMS_NOTIFIER_CLS", default=None))
