from __future__ import annotations

from typing import Optional

from sila2.framework.errors.defined_execution_error import DefinedExecutionError

from .valvegatewayservice_feature import ValveGatewayServiceFeature


class InvalidValveIndex(DefinedExecutionError):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The sent Valve Index is not known"
        super().__init__(ValveGatewayServiceFeature.defined_execution_errors["InvalidValveIndex"], message=message)
