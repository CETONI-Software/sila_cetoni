from __future__ import annotations

from typing import Optional

from sila2.framework.errors.defined_execution_error import DefinedExecutionError

from .controlloopservice_feature import ControlLoopServiceFeature


class InvalidChannelIndex(DefinedExecutionError):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The sent channel index is not known."
        super().__init__(ControlLoopServiceFeature.defined_execution_errors["InvalidChannelIndex"], message=message)
