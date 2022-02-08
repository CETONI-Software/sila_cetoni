from __future__ import annotations

import datetime
import logging
import time
from concurrent.futures import Executor
from queue import Queue
from threading import Event
from typing import Any, Dict, Optional, Union

from qmixsdk.qmixbus import DeviceError, PollingTimer
from qmixsdk.qmixpump import Pump
from sila2.framework import Command, FullyQualifiedIdentifier, Property
from sila2.framework.command.execution_info import CommandExecutionStatus
from sila2.framework.errors.undefined_execution_error import UndefinedExecutionError
from sila2.server import ObservableCommandInstance

from .....application.config import Config
from .....application.system import ApplicationSystem
from ..generated.pumpdrivecontrolservice import (
    DisablePumpDrive_Responses,
    EnablePumpDrive_Responses,
    InitializationFailed,
    InitializationNotFinished,
    InitializePumpDrive_Responses,
    NotSupported,
    PumpDriveControlServiceBase,
    PumpDriveControlServiceFeature,
    RestoreDrivePositionCounter_Responses,
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
    __config: Config
    __stop_event: Event

    __CALIBRATION_TIMEOUT = datetime.timedelta(seconds=60)

    def __init__(self, pump: Pump, executor: Executor):
        super().__init__()
        self.__pump = pump
        self.__system = ApplicationSystem()
        self.__config = Config(self.__pump.get_pump_name())
        self.__stop_event = Event()

        self._restore_last_drive_position_counter()

        def update_fault_state(stop_event: Event):
            new_fault_state = fault_state = self.__pump.is_in_fault_state()
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_fault_state = self.__pump.is_in_fault_state()
                if new_fault_state != fault_state:
                    fault_state = new_fault_state
                    self.update_FaultState(fault_state)
                time.sleep(0.1)

        def update_pump_drive_state(stop_event: Event):
            new_is_enabled = is_enabled = self.__pump.is_enabled() and self.__system.state.is_operational()
            while not stop_event.is_set():
                new_is_enabled = self.__pump.is_enabled() and self.__system.state.is_operational()
                if new_is_enabled != is_enabled:
                    is_enabled = new_is_enabled
                    self.update_PumpDriveState("Enabled" if is_enabled else "Disabled")
                time.sleep(0.1)

        def update_drive_position_counter(stop_event: Event):
            new_pos_counter = pos_counter = (
                self.__pump.get_position_counter_value() if self.__system.state.is_operational() else 0
            )
            while not stop_event.is_set():
                new_pos_counter = (
                    self.__pump.get_position_counter_value() if self.__system.state.is_operational() else 0
                )
                if new_pos_counter != pos_counter:
                    pos_counter = new_pos_counter
                    self.update_DrivePositionCounter(pos_counter)
                time.sleep(0.1)

        # initial values
        self.update_FaultState(self.__pump.is_in_fault_state())
        self.update_PumpDriveState("Enabled" if self.__pump.is_enabled() else "Disabled")
        self.update_DrivePositionCounter(self.__pump.get_position_counter_value())

        executor.submit(update_fault_state, self.__stop_event)
        executor.submit(update_pump_drive_state, self.__stop_event)
        executor.submit(update_drive_position_counter, self.__stop_event)

    def _restore_last_drive_position_counter(self):
        """
        Reads the last drive position counter from the server's config file.
        """
        drive_pos_counter = self.__config.pump_drive_position_counter
        if drive_pos_counter is not None:
            logging.debug(f"Restoring drive position counter: {drive_pos_counter}")
            self.__pump.restore_position_counter_value(drive_pos_counter)
        else:
            logging.warning(
                f"Could not read drive position counter for {self.__pump.get_pump_name()} from config file. "
                "Reference move needed!"
            )

    def update_DrivePositionCounter(self, DrivePositionCounter: int, queue: Optional[Queue[int]] = None):
        self.__config.pump_drive_position_counter = DrivePositionCounter
        return super().update_DrivePositionCounter(DrivePositionCounter, queue)

    def EnablePumpDrive(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> EnablePumpDrive_Responses:
        if not self.__system.state.is_operational():
            raise SystemNotOperationalError(PumpDriveControlServiceFeature["EnablePumpDrive"])
        self.__pump.enable(True)

    def DisablePumpDrive(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> DisablePumpDrive_Responses:
        if not self.__system.state.is_operational():
            raise SystemNotOperationalError(PumpDriveControlServiceFeature["DisablePumpDrive"])
        self.__pump.enable(False)

    def RestoreDrivePositionCounter(
        self, DrivePositionCounterValue: int, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> RestoreDrivePositionCounter_Responses:
        if not self.__system.state.is_operational():
            raise SystemNotOperationalError(PumpDriveControlServiceFeature["RestoreDrivePositionCounter"])

        try:
            self.__pump.restore_position_counter_value(DrivePositionCounterValue)
        except DeviceError as err:
            if err.errorcode == -0x00CA:  # -ERR_DEVNOSUPP
                raise NotSupported(str(err))
            raise

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
        self.__config.write()
