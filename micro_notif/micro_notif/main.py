import asyncio
from micro_notif import events, utils


async def main() -> None:
    utils.bootstrap_logging()

    try:
        await events.on_startup()
        await asyncio.Future()
    finally:
        await events.on_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
