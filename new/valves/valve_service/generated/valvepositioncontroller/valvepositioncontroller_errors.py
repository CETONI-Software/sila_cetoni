from __future__ import annotations

from typing import Optional

from sila2.framework.errors.defined_execution_error import DefinedExecutionError

from .valvepositioncontroller_feature import ValvePositionControllerFeature


class ValveNotToggleable(DefinedExecutionError):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = (
                "The current valve does not support toggling because it has more than only two possible positions."
            )
        super().__init__(ValvePositionControllerFeature.defined_execution_errors["ValveNotToggleable"], message=message)


class ValvePositionNotAvailable(DefinedExecutionError):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The actual position of the current valve cannot be retrieved. This is most likely a temporary error that can be fixed by setting a specific valve position."
        super().__init__(
            ValvePositionControllerFeature.defined_execution_errors["ValvePositionNotAvailable"], message=message
        )
