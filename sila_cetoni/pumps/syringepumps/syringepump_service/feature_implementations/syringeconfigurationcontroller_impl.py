from __future__ import annotations

import time, math
from threading import Event
from concurrent.futures import Executor

from typing import Any, Dict, Union

from sila2.framework import FullyQualifiedIdentifier, Command, Property
from sila2.framework.errors.validation_error import ValidationError
from sila2.framework.errors.undefined_execution_error import UndefinedExecutionError

from .....application.system import ApplicationSystem
from qmixsdk.qmixpump import Pump

from ..generated.syringeconfigurationcontroller import (
    SetSyringeParameters_Responses,
    SyringeConfigurationControllerBase,
    SyringeConfigurationControllerFeature,
)


class SystemNotOperationalError(UndefinedExecutionError):
    def __init__(self, command_or_property: Union[Command, Property]):
        super().__init__(
            "Cannot {} {} because the system is not in an operational state.".format(
                "execute" if isinstance(command_or_property, Command) else "read from",
                command_or_property.fully_qualified_identifier,
            )
        )


class SyringeConfigurationControllerImpl(SyringeConfigurationControllerBase):
    __pump: Pump
    __system: ApplicationSystem
    __stop_event: Event

    def __init__(self, pump: Pump, executor: Executor):
        super().__init__()
        self.__pump = pump
        self.__system = ApplicationSystem()
        self.__stop_event = Event()

        def update_inner_diameter(stop_event: Event):
            new_inner_diameter = self.__pump.get_syringe_param().inner_diameter_mm
            inner_diameter = -1  # force sending first value
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_inner_diameter = self.__pump.get_syringe_param().inner_diameter_mm
                if not math.isclose(new_inner_diameter, inner_diameter):
                    inner_diameter = new_inner_diameter
                    self.update_InnerDiameter(inner_diameter)
                time.sleep(0.1)

        def update_max_piston_stroke(stop_event: Event):
            new_max_piston_stroke = self.__pump.get_syringe_param().max_piston_stroke_mm
            max_piston_stroke = -1  # force sending first value
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_max_piston_stroke = self.__pump.get_syringe_param().max_piston_stroke_mm
                if not math.isclose(new_max_piston_stroke, max_piston_stroke):
                    max_piston_stroke = new_max_piston_stroke
                    self.update_MaxPistonStroke(max_piston_stroke)
                time.sleep(0.1)

        executor.submit(update_inner_diameter, self.__stop_event)
        executor.submit(update_max_piston_stroke, self.__stop_event)

    def SetSyringeParameters(
        self, InnerDiameter: float, MaxPistonStroke: float, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetSyringeParameters_Responses:
        if not self.__system.state.is_operational():
            raise SystemNotOperationalError(SyringeConfigurationControllerFeature["SetSyringeParameters"])

        def _validate(value: float, parameter: str, parameter_id: int):
            if value < 0:
                raise ValidationError(
                    SyringeConfigurationControllerFeature["SetSyringeParameters"].parameters.fields[parameter_id],
                    f"The {parameter} ({value}) is invalid. It cannot be less than 0!",
                )

        _validate(InnerDiameter, "InnerDiameter", 0)
        _validate(MaxPistonStroke, "MaxPistonStroke", 1)
        self.__pump.set_syringe_param(InnerDiameter, MaxPistonStroke)

    def stop(self) -> None:
        self.__stop_event.set()
