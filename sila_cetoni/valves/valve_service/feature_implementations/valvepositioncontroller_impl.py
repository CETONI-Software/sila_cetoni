from __future__ import annotations
import logging
from queue import Queue

import time
from threading import Event
from concurrent.futures import Executor

from typing import Any, Dict, List, Optional, Union

from sila2.framework import FullyQualifiedIdentifier, Command, Property
from sila2.framework.errors.validation_error import ValidationError
from sila2.framework.errors.undefined_execution_error import UndefinedExecutionError

from ....application.system import ApplicationSystem
from qmixsdk.qmixbus import DeviceError
from qmixsdk.qmixvalve import Valve

from .valvegatewayservice_impl import ValveGatewayServiceImpl

from ..generated.valvepositioncontroller import (
    SwitchToPosition_Responses,
    TogglePosition_Responses,
    ValvePositionControllerBase,
    ValvePositionControllerFeature,
    ValveNotToggleable,
    ValvePositionNotAvailable,
)

from ..generated.valvegatewayservice import InvalidValveIndex


class SystemNotOperationalError(UndefinedExecutionError):
    def __init__(self, command_or_property: Union[Command, Property]):
        super().__init__(
            "Cannot {} {} because the system is not in an operational state.".format(
                "execute" if isinstance(command_or_property, Command) else "read from",
                command_or_property.fully_qualified_identifier,
            )
        )


class ValvePositionControllerImpl(ValvePositionControllerBase):
    __valve: Optional[Valve]
    __valve_gateway: Optional[ValveGatewayServiceImpl]
    __position_queues: List[Queue[int]]  # same number of items and order as `__valve_gateway.valves`
    __system: ApplicationSystem
    __stop_event: Event

    def __init__(
        self, executor: Executor, valve: Optional[Valve] = None, gateway: Optional[ValveGatewayServiceImpl] = None
    ):
        super().__init__()
        self.__valve = valve
        self.__valve_gateway = gateway
        self.__system = ApplicationSystem()
        self.__stop_event = Event()

        if self.__valve:
            # initial value
            try:
                self.update_Position(self.__valve.actual_valve_position())
            except DeviceError as err:
                logging.error(err)

            executor.submit(self.__make_position_updater(), self.__stop_event)
        else:
            self.__position_queues = []
            for i in range(len(self.__valve_gateway.valves)):
                self.__position_queues += [Queue()]

                # initial value
                self.update_Position(
                    self.__valve_gateway.valves[i].actual_valve_position(), queue=self.__position_queues[i]
                )

                executor.submit(self.__make_position_updater(i), self.__stop_event)

    def __make_position_updater(self, i: Optional[int] = None):
        def update_position(stop_event: Event):
            valve = self.__valve or self.__valve_gateway.valves[i]
            new_position = position = valve.actual_valve_position()
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_position = valve.actual_valve_position()
                if new_position != position:
                    position = new_position
                    self.update_Position(position, queue=self.__position_queues[i])
                time.sleep(0.1)

        return update_position

    def get_NumberOfPositions(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        valve = self.__valve or self.__valve_gateway.get_valve(metadata)
        return valve.number_of_valve_positions()

    def Position_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[int]]:
        if self.__valve_gateway is None:
            return super().Position_on_subscription(metadata=metadata)

        valve_index: int = metadata.pop(self.__valve_gateway.valve_index_identifier)
        try:
            return self.__position_queues[valve_index]
        except IndexError:
            raise InvalidValveIndex(
                message=f"The sent Valve Index {valve_index} is invalid. The index must be between 0 and {len(self.__valve_gateway.valves) - 1}.",
            )

    @staticmethod
    def _try_switch_valve_to_position(valve: Valve, position: int):
        try:
            valve.switch_valve_to_position(position)
        except DeviceError as err:
            if err.errorcode == 2:
                raise ValvePositionNotAvailable()
            raise err

    def SwitchToPosition(
        self, Position: int, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SwitchToPosition_Responses:
        if not self.__system.state.is_operational():
            raise SystemNotOperationalError(ValvePositionControllerFeature["SwitchToPosition"])

        valve = self.__valve or self.__valve_gateway.get_valve(metadata)
        if 0 > Position or Position >= valve.number_of_valve_positions():
            raise ValidationError(
                ValvePositionControllerFeature["SwitchToPosition"].parameters.fields[0],
                f"The given position ({Position}) is not in the range for this valve. "
                f"Adjust the valve position to fit in the range between 0 and {valve.number_of_valve_positions() - 1}!",
            )

        self._try_switch_valve_to_position(valve, Position)

    def TogglePosition(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> TogglePosition_Responses:
        if not self.__system.state.is_operational():
            raise SystemNotOperationalError(ValvePositionControllerFeature["TogglePosition"])

        valve = self.__valve or self.__valve_gateway.get_valve(metadata)
        if valve.number_of_valve_positions() > 2:
            raise ValveNotToggleable()

        self._try_switch_valve_to_position(valve, (valve.actual_valve_position() + 1) % 2)

    def stop(self) -> None:
        self.__stop_event.set()
