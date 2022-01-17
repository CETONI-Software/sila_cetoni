from __future__ import annotations

import time
from concurrent.futures import Executor
from threading import Event
from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier

from device_drivers.balance import BalanceInterface

from ..generated.balanceservice import BalanceServiceBase, Tare_Responses


class BalanceServiceImpl(BalanceServiceBase):
    __balance: BalanceInterface
    __stop_event: Event

    def __init__(self, balance: BalanceInterface, executor: Executor):
        super().__init__()
        self.__balance = balance
        self.__stop_event = Event()

        def update_value(stop_event: Event):
            while not stop_event.is_set():
                self.update_Value(self.__balance.value)
                time.sleep(0.1)

        executor.submit(update_value, self.__stop_event)

    def Tare(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Tare_Responses:
        self.__balance.tare()

    def stop(self) -> None:
        self.__stop_event.set()
