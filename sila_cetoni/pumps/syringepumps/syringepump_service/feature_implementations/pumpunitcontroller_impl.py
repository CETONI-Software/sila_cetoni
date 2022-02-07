from __future__ import annotations
from collections import namedtuple
from threading import Event

from typing import Any, Dict
import logging
import time
from threading import Event
from concurrent.futures import Executor

from typing import Any, Dict, Union

from sila2.framework import FullyQualifiedIdentifier, Command, Property
from sila2.framework.errors.validation_error import ValidationError
from sila2.framework.errors.undefined_execution_error import UndefinedExecutionError

from .....application.system import ApplicationSystem
from qmixsdk.qmixpump import Pump

from .... import unit_conversion as uc

from ..generated.pumpunitcontroller import (
    PumpUnitControllerBase,
    PumpUnitControllerFeature,
    SetFlowUnit_Responses,
    SetVolumeUnit_Responses,
    VolumeUnit,
)


class SystemNotOperationalError(UndefinedExecutionError):
    def __init__(self, command_or_property: Union[Command, Property]):
        super().__init__(
            "Cannot {} {} because the system is not in an operational state.".format(
                "execute" if isinstance(command_or_property, Command) else "read from",
                command_or_property.fully_qualified_identifier,
            )
        )


FlowUnit = namedtuple("FlowUnit", ["VolumeUnit", "TimeUnit"])


class PumpUnitControllerImpl(PumpUnitControllerBase):
    __pump: Pump
    __system: ApplicationSystem
    __stop_event: Event

    def __init__(self, pump: Pump, executor: Executor):
        super().__init__()
        self.__pump = pump
        self.__system = ApplicationSystem()
        self.__stop_event = Event()

        def update_flow_unit(stop_event: Event):
            new_flow_unit = flow_unit = FlowUnit(*uc.flow_unit_to_tuple(self.__pump.get_flow_unit()))
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_flow_unit = FlowUnit(*uc.flow_unit_to_tuple(self.__pump.get_flow_unit()))
                if new_flow_unit != flow_unit:
                    flow_unit = new_flow_unit
                    self.update_FlowUnit(flow_unit)
                time.sleep(0.1)

        def update_volume_unit(stop_event: Event):
            new_volume_unit = volume_unit = uc.volume_unit_to_string(self.__pump.get_volume_unit())
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_volume_unit = uc.volume_unit_to_string(self.__pump.get_volume_unit())
                if new_volume_unit != volume_unit:
                    volume_unit = new_volume_unit
                    self.update_VolumeUnit(volume_unit)
                time.sleep(0.1)

        # initial values
        self.update_FlowUnit(FlowUnit(*uc.flow_unit_to_tuple(self.__pump.get_flow_unit())))
        self.update_VolumeUnit(uc.volume_unit_to_string(self.__pump.get_volume_unit()))

        executor.submit(update_flow_unit, self.__stop_event)
        executor.submit(update_volume_unit, self.__stop_event)

    def SetFlowUnit(self, FlowUnit: Any, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> SetFlowUnit_Responses:
        if not self.__system.state.is_operational():
            raise SystemNotOperationalError(PumpUnitControllerFeature["SetFlowUnit"])

        logging.debug(f"flow unit {FlowUnit} {type(FlowUnit)}")

        # try:
        flow_unit = FlowUnit
        prefix, volume_unit, time_unit = uc.evaluate_units(
            parameter=PumpUnitControllerFeature["SetFlowUnit"].parameters.fields[0],
            requested_volume_unit=flow_unit.VolumeUnit,
            requested_time_unit=flow_unit.TimeUnit,
        )
        # except ValueError:
        #     raise ValidationError(
        #         PumpUnitControllerFeature["SetFlowUnit"].parameters.fields[0],
        #         "The given flow unit is malformed. It has to be something like 'ml/s', for instance."
        #     )
        # else:
        self.__pump.set_flow_unit(prefix, volume_unit, time_unit)

    def SetVolumeUnit(
        self, VolumeUnit: VolumeUnit, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetVolumeUnit_Responses:
        if not self.__system.state.is_operational():
            raise SystemNotOperationalError(PumpUnitControllerFeature["SetVolumeUnit"])

        prefix, volume_unit = uc.evaluate_units(
            parameter=PumpUnitControllerFeature["SetVolumeUnit"].parameters.fields[0], requested_volume_unit=VolumeUnit
        )
        self.__pump.set_volume_unit(prefix, volume_unit)

    def stop(self) -> None:
        self.__stop_event.set()
