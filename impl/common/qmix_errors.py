"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Qmix Error*

:details: Qmix Error:
    Provides a bridge from a DeviceError from QmixSDK to a SiLA Execution Error

:file:    qmix_error.py
:authors: Florian Meinicke
:date (creation)          2020-10-09
:date (last modification) 2020-10-09
________________________________________________________________________
"""

from sila2lib.error_handling.server_err import *

from qmixsdk.qmixbus import DeviceError


#-----------------------------------------------------------------------------
# Common
class QmixSDKSiLAError(SiLAExecutionError):
    """
    An unexpected error that was thrown by the QmixSDK during the execution of a command.
    Basically maps an error from QmixSDK to a SiLA Undefined Execution Error.
    """

    def __init__(self, qmixsdk_error: DeviceError = None):
        msg = f"The QmixSDK threw an unexpected error {qmixsdk_error}"

        super().__init__(msg=msg, error_identifier=None)

#-----------------------------------------------------------------------------
# Pumps
class FlowRateOutOfRangeError(SiLAValidationError):
    """
    The requested flow rate is not in a valid range for this pump.
    """

    def __init__(self, command: str, msg: str):
        """
        :param command: The command where the error occurred
        :param msg: The description of the error and possible actions to resolve it
        """
        super().__init__(
            parameter=f"de.cetoni/pumps.syringepumps/PumpFluidDosingService/v1/Command/{command}/FlowRate",
            msg=msg
        )

class FillLevelOutOfRangeError(SiLAValidationError):
    """
    The requested fill level is not in a valid range for this pump.
    """

    def __init__(self, command: str, msg: str):
        """
        :param command: The command where the error occurred
        :param msg: The description of the error and possible actions to resolve it
        """
        super().__init__(
            parameter=f"de.cetoni/pumps.syringepumps/PumpFluidDosingService/v1/Command/{command}/Filllevel",
            msg=msg
        )

class VolumeOutOfRangeError(SiLAValidationError):
    """
    The requested volume is not in a valid range for this pump.
    """

    def __init__(self, command: str, msg: str):
        """
        :param command: The command where the error occurred
        :param msg: The description of the error and possible actions to resolve it
        """
        super().__init__(
            parameter=f"de.cetoni/pumps.syringepumps/PumpFluidDosingService/v1/Command/{command}/Volume",
            msg=msg
        )

class DosageFinishedUnexpectedlyError(SiLAExecutionError):
    """
    The dosage could not be finished properly due to an error.
    """

    def __init__(self, error_identifier: str = None, msg: str = None):
        super().__init__(msg=msg, error_identifier=None)

#-----------------------------------------------------------------------------
# Units
class UnitConversionError(SiLAValidationError):
    """
    The given unit could not be converted properly due to malformed input.
    """

    def __init__(self, command: str, parameter: str, msg: str):
        """
        :param command: The command where the error occurred
        :param parameter: The parameter which is invalid
        :param msg: The description of the error and possible actions to resolve it
        """
        super().__init__(
            parameter=f"de.cetoni/pumps.syringepumps/PumpUnitController/v1/Command/{command}/Parameter/{parameter}",
            msg=msg
        )

#-----------------------------------------------------------------------------
# Valves
class ValvePositionOutOfRangeError(SiLAValidationError):
    """
    The requested valve position is not in the valid range for this valve.
    """

    def __init__(self, msg: str = None):
        super().__init__(
            parameter="de.cetoni/valves/ValvePositionController/v1/Command/SwitchToPosition/Parameter/Position",
            msg=msg
        )
