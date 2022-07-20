from abc import ABC, abstractmethod


class DeviceDriverABC(ABC):
    """
    The interface for every device driver interface used in sila_cetoni
    """

    @abstractmethod
    def start(self):
        raise NotImplementedError()

    @abstractmethod
    def stop(self):
        raise NotImplementedError()
