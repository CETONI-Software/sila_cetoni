"""
________________________________________________________________________

:PROJECT: SiLA2_python

*neMESYS*

:details: neMESYS:
    This is a test service for neMESYS syringe pumps via SiLA2

:file:    neMESYS_errors.py
:authors: Florian Meinicke
:date (creation)          2019-08-26
:date (last modification) 2020-10-09
________________________________________________________________________
"""

from sila2lib.error_handling.server_err import SiLAExecutionError, \
SiLAValidationError, SiLAFrameworkError, SiLAFrameworkErrorType

from qmix_error import QmixSDKError, DeviceError


class FlowRateOutOfRangeError(SiLAValidationError):
    """
    The requested flow rate is not in a valid range for this pump.
    """

    def __init__(self, msg: str):
        super().__init__(
            parameter="sila2.de.cetoni.pumps.syringepumps.pumpfluiddosingservice.v1.FlowRate",
            msg=msg
        )


class FillLevelOutOfRangeError(SiLAValidationError):
    """
    The requested fill level is not in a valid range for this pump.
    """

    def __init__(self, msg: str):
        super().__init__(
            parameter="sila2.de.cetoni.pumps.syringepumps.pumpfluiddosingservice.v1.Filllevel",
            msg=msg
        )


class VolumeOutOfRangeError(SiLAValidationError):
    """
    The requested volume is not in a valid range for this pump.
    """

    def __init__(self, msg: str):
        super().__init__(
            parameter="sila2.de.cetoni.pumps.syringepumps.pumpfluiddosingservice.v1.Volume",
            msg=msg
        )


class DosageFinishedUnexpectedlyError(SiLAExecutionError):
    """
    The dosage could not be finished properly due to an error.
    """

    def __init__(self, error_identifier: str = None, msg: str = None):
        super().__init__(msg=msg, error_identifier=None)



class UnitConversionError(SiLAValidationError):
    """
    The given unit could not be converted properly due to malformed input.
    """

    def __init__(self, parameter, msg: str):
        super().__init__(
            parameter=f"sila2.de.cetoni.pumps.syringepumps.pumpunitcontroller.v1.{parameter}",
            msg=msg
        )



class ValvePositionOutOfRangeError(SiLAValidationError):
    """
    The requested valve position is not in the valid range for this valve.
    """

    def __init__(self, msg: str = None):
        super().__init__(
            parameter="sila2.de.cetoni.pumps.syringepumps.valvepositioncontroller.v1.Position",
            msg=msg
        )


class ValveNotToggleableError(SiLAExecutionError):
    """
    The current valve does not support toggling because it has more than only two possible positions.
    """

    def __init__(self):
        msg = "The current valve does not support toggling because it has more than only two possible positions."
        super().__init__(error_identifier="ValveNotToggleable", msg=msg)

