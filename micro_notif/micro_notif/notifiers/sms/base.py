from abc import ABCMeta, abstractmethod


class AbstractSMSNotifier(metaclass=ABCMeta):
    @abstractmethod
    async def send(self, to: str, message: str) -> bool:
        pass
