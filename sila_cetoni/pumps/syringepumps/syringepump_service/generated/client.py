from __future__ import annotations

from typing import TYPE_CHECKING

from sila2.client import SilaClient

from .pumpdrivecontrolservice import (
    InitializationFailed,
    InitializationNotFinished,
    NotSupported,
    PumpDriveControlServiceFeature,
)

if TYPE_CHECKING:

    from .forcemonitoringservice import ForceMonitoringServiceClient
    from .pumpdrivecontrolservice import PumpDriveControlServiceClient
    from .pumpfluiddosingservice import PumpFluidDosingServiceClient
    from .pumpunitcontroller import PumpUnitControllerClient
    from .syringeconfigurationcontroller import SyringeConfigurationControllerClient


class Client(SilaClient):

    ForceMonitoringService: ForceMonitoringServiceClient

    PumpDriveControlService: PumpDriveControlServiceClient

    PumpFluidDosingService: PumpFluidDosingServiceClient

    PumpUnitController: PumpUnitControllerClient

    SyringeConfigurationController: SyringeConfigurationControllerClient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_defined_execution_error_class(
            PumpDriveControlServiceFeature.defined_execution_errors["InitializationFailed"], InitializationFailed
        )

        self._register_defined_execution_error_class(
            PumpDriveControlServiceFeature.defined_execution_errors["InitializationNotFinished"],
            InitializationNotFinished,
        )

        self._register_defined_execution_error_class(
            PumpDriveControlServiceFeature.defined_execution_errors["NotSupported"], NotSupported
        )
