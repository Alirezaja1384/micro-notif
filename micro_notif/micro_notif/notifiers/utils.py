from importlib import import_module
from functools import lru_cache

from micro_notif.settings import SMS_NOTIFIER_CLS
from .sms import AbstractSMSNotifier


@lru_cache(maxsize=None)
def _get_class_by_name(name: str):
    module_name, class_name = name.rsplit(".", 1)
    module = import_module(module_name)
    return getattr(module, class_name)


def get_sms_notifier() -> AbstractSMSNotifier | None:
    if not SMS_NOTIFIER_CLS:
        return None

    return _get_class_by_name(SMS_NOTIFIER_CLS)()
