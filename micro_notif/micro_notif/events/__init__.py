from . import v1


async def on_startup():
    await v1.on_startup()


async def on_shutdown():
    await v1.on_shutdown()


__all__ = ["on_startup", "on_shutdown"]
