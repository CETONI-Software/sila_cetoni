from __future__ import annotations

from typing import TYPE_CHECKING

from sila2.client import SilaClient

from .valvepositioncontroller import ValveNotToggleable, ValvePositionControllerFeature, ValvePositionNotAvailable

if TYPE_CHECKING:

    from .valvegatewayservice import ValveGatewayServiceClient
    from .valvepositioncontroller import ValvePositionControllerClient


class Client(SilaClient):

    ValveGatewayService: ValveGatewayServiceClient

    ValvePositionController: ValvePositionControllerClient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_defined_execution_error_class(
            ValvePositionControllerFeature.defined_execution_errors["ValveNotToggleable"], ValveNotToggleable
        )

        self._register_defined_execution_error_class(
            ValvePositionControllerFeature.defined_execution_errors["ValvePositionNotAvailable"],
            ValvePositionNotAvailable,
        )
