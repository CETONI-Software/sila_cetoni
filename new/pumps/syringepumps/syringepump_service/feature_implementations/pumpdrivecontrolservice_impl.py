from __future__ import annotations
import datetime
import logging

import time
from threading import Event
from concurrent.futures import Executor

from typing import Any, Dict, Union

from sila2.framework import FullyQualifiedIdentifier, Command, Property
from sila2.framework.command.execution_info import CommandExecutionStatus
from sila2.server import ObservableCommandInstance
from sila2.framework.errors.undefined_execution_error import UndefinedExecutionError

from application.system import ApplicationSystem
from qmixsdk.qmixbus import PollingTimer
from qmixsdk.qmixpump import Pump
from ..generated.pumpdrivecontrolservice import (
    DisablePumpDrive_Responses,
    EnablePumpDrive_Responses,
    InitializePumpDrive_Responses,
    PumpDriveControlServiceBase,
    PumpDriveControlServiceFeature,
    InitializationFailed,
    InitializationNotFinished,
)


class SystemNotOperationalError(UndefinedExecutionError):
    def __init__(self, command_or_property: Union[Command, Property]):
        super().__init__(
            "Cannot {} {} because the system is not in an operational state.".format(
                "execute" if isinstance(command_or_property, Command) else "read from",
                command_or_property.fully_qualified_identifier,
            )
        )


class PumpDriveControlServiceImpl(PumpDriveControlServiceBase):
    __pump: Pump
    __system: ApplicationSystem
    __stop_event: Event
    __force_fault_state_update: bool = True
    __force_pump_drive_state_update: bool = True

    __CALIBRATION_TIMEOUT = datetime.timedelta(seconds=60)

    def __init__(self, pump: Pump, executor: Executor):
        super().__init__()
        self.__pump = pump
        self.__system = ApplicationSystem()
        self.__stop_event = Event()

        # TODO restore drive position counter

        def update_fault_state(stop_event: Event):
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_fault_state = self.__pump.is_in_fault_state()
                if self.__force_fault_state_update or new_fault_state != fault_state:
                    fault_state = new_fault_state
                    self.update_FaultState(fault_state)
                    self.__force_fault_state_update = False
                time.sleep(0.1)

        def update_pump_drive_state(stop_event: Event):
            while not stop_event.is_set():
                new_is_enabled = self.__pump.is_enabled() and self.__system.state.is_operational()
                if self.__force_pump_drive_state_update or new_is_enabled != is_enabled:
                    is_enabled = new_is_enabled
                    self.update_PumpDriveState("Enabled" if is_enabled else "Disabled")
                    self.__force_pump_drive_state_update = False
                time.sleep(0.1)

        executor.submit(update_fault_state, self.__stop_event)
        executor.submit(update_pump_drive_state, self.__stop_event)

    def FaultState_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        self.__force_fault_state_update = True

    def PumpDriveState_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        self.__force_pump_drive_state_update = True

    def EnablePumpDrive(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> EnablePumpDrive_Responses:
        if not self.__system.state.is_operational():
            raise SystemNotOperationalError(PumpDriveControlServiceFeature["EnablePumpDrive"])
        self.__pump.enable(True)

    def DisablePumpDrive(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> DisablePumpDrive_Responses:
        if not self.__system.state.is_operational():
            raise SystemNotOperationalError(PumpDriveControlServiceFeature["DisablePumpDrive"])
        self.__pump.enable(False)

    def InitializePumpDrive(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any], instance: ObservableCommandInstance
    ) -> InitializePumpDrive_Responses:
        if not self.__system.state.is_operational():
            raise SystemNotOperationalError(PumpDriveControlServiceFeature["InitializePumpDrive"])

        if not self.__pump.is_calibration_finished():
            raise InitializationNotFinished()

        # send first info immediately
        instance.status = CommandExecutionStatus.running
        instance.progress = 0
        instance.estimated_remaining_time = self.__CALIBRATION_TIMEOUT

        self.__pump.calibrate()
        time.sleep(0.2)

        calibration_finished = self.__pump.is_calibration_finished()
        if calibration_finished:
            instance.status = CommandExecutionStatus.finishedSuccessfully
            instance.progress = 1
            instance.estimated_remaining_time = 0

        timeout: datetime.timedelta = self.__CALIBRATION_TIMEOUT
        timer = PollingTimer(timeout.seconds * 1000)
        message_timer = PollingTimer(period_ms=500)
        POLLING_TIMEOUT = datetime.timedelta(seconds=0.1)
        while not (calibration_finished or timer.is_expired()):
            time.sleep(POLLING_TIMEOUT.total_seconds())
            timeout -= POLLING_TIMEOUT
            if message_timer.is_expired():
                instance.status = CommandExecutionStatus.running
                instance.progress = 100 * (self.__CALIBRATION_TIMEOUT - timeout) / self.__CALIBRATION_TIMEOUT
                instance.estimated_remaining_time = timeout
                message_timer.restart()
            calibration_finished = self.__pump.is_calibration_finished()

        if calibration_finished and not self.__pump.is_in_fault_state():
            instance.status = CommandExecutionStatus.finishedSuccessfully
        else:
            instance.status = CommandExecutionStatus.finishedWithError
            logging.error("An unexpected error occurred: %s", self.__pump.read_last_error())
        instance.progress = 1
        instance.estimated_remaining_time = datetime.timedelta(0)

        logging.info("Pump calibrated: %s", calibration_finished)
        last_error = self.__pump.read_last_error()
        if not calibration_finished and last_error.code != 0:
            raise InitializationFailed(
                f"The initialization did not end properly. The last error that occurred was {last_error}"
            )

    def stop(self) -> None:
        self.__stop_event.set()
