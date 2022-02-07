from __future__ import annotations

from typing import TYPE_CHECKING

from sila2.client import SilaClient

from .controlloopservice import ControlLoopServiceFeature, InvalidChannelIndex

if TYPE_CHECKING:

    from .controlloopservice import ControlLoopServiceClient


class Client(SilaClient):

    ControlLoopService: ControlLoopServiceClient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_defined_execution_error_class(
            ControlLoopServiceFeature.defined_execution_errors["InvalidChannelIndex"], InvalidChannelIndex
        )
