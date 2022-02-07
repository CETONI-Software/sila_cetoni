from __future__ import annotations

from typing import Optional

from sila2.framework.errors.defined_execution_error import DefinedExecutionError

from .pumpdrivecontrolservice_feature import PumpDriveControlServiceFeature


class InitializationFailed(DefinedExecutionError):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The initialization did not end properly."
        super().__init__(
            PumpDriveControlServiceFeature.defined_execution_errors["InitializationFailed"], message=message
        )


class InitializationNotFinished(DefinedExecutionError):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "There is already another initialization running that hasn't finished yet. Starting a new initialization move is not allowed."
        super().__init__(
            PumpDriveControlServiceFeature.defined_execution_errors["InitializationNotFinished"], message=message
        )


class NotSupported(DefinedExecutionError):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The Command is not supported by this device."
        super().__init__(PumpDriveControlServiceFeature.defined_execution_errors["NotSupported"], message=message)
