import logging
from . import settings


def mask_str(
    val: str,
    mask_char: str = "*",
    from_index: int | None = None,
    to_index: int | None = None,
) -> str:
    from_index = from_index or 0
    to_index = to_index or len(val) - 1

    return "".join(
        [
            mask_char if i in range(from_index, to_index + 1) else c
            for i, c in enumerate(val)
        ]
    )


def bootstrap_logging():
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format="> %(levelname)s | %(name)s | %(message)s",
    )
    logging.getLogger("httpx").setLevel(
        logging.DEBUG if settings.DEBUG else logging.WARNING
    )
