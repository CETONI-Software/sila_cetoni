# PumpFluidDosingService
Allows to dose a fluid by a given amount of volume or a given flow rate. There are commands for absolute dosing ([`SetFillLevel`](#SetFillLevel)) and relative dosing ([`DoseVolume`](#DoseVolume) and [`GenerateFlow`](#GenerateFlow)) available.

The flow rate can be negative. In this case the pump aspirates the fluid instead of dispensing. The flow rate has to be a value between [`MaxFlowRate`](#Properties) and [`MinFlowRate`](#Properties). If the value is not within this range (hence is invalid) a ValidationError will be thrown.  
At any time the property [`SyringeFillLevel`](#Properties) can be queried to see how much fluid is left in the syringe.
Similarly the property [`FlowRate`](#Properties) can be queried to get the current flow rate at which the pump is dosing.

## Commands
### `SetFillLevel`
Pumps fluid with the given flow rate until the requested fill level is reached. Depending on the requested fill level given in the `FillLevel` parameter this function may cause aspiration or dispension of fluid.

Parameters:
- `FillLevel`: The requested fill level. A level of 0 indicates a completely empty syringe. The value has to be between 0 and [`MaxSyringeFillLevel`](#Properties) or else a ValidationError will be thrown.
- `FlowRate`: The flow rate at which the pump should dose the fluid. This value can be negative. In that case the pump aspirates the fluid.

Response:
- `Success`: A boolean value where `false` means that the dosage failed and `true` meaning the dosage was finished properly.

observable: yes

### `DoseVolume`
Dose a certain amount of volume with the given flow rate.  

Parameters:
- `Volume`: The amount of volume to dose.
- `FlowRate`: The flow rate at which the pump should dose the fluid. This value can be negative. In that case the pump aspirates the fluid.

Response:
- `Success`: A boolean value where `false` means that the dosage failed and `true` meaning the dosage was finished properly.

observable: yes

### `GenerateFlow`
Generate a continous flow with the given flow rate. Dosing continues until it gets stopped manually by calling [`StopDosage`](#StopDosage) or until the pusher reached one of its limits.

Parameters:
- `FlowRate`: The flow rate at which the pump should dose the fluid. This value can be negative. In that case the pump aspirates the fluid.

Response:
- `Success`: A boolean value where `false` means that the dosage failed and `true` meaning the dosage was finished properly.

observable: yes

### `StopDosage`
Stops a currently running dosage immediately. 

Parameters:
- none

Response:
- `Success`: A boolean value where `false` means that stopping the dosage failed and `true` meaning the dosage was stopped properly.

observable: no

## Properties
- `MaxSyringeFillLevel`: The maximum amount of fluid that the syringe can hold.
    * observable: no
- `SyringeFillLevel`: The current amount of fluid left in the syringe.
    * observable: yes
- `MaxFlowRate`: The maximum value of the flow rate at which this pump can dose a fluid.
    * observable: no
- `MinFlowRate`: The minimum value of the flow rate at which this pump can dose a fluid.
    * observable: no
- `FlowRate`: The current value of the flow rate. It is 0 if the pump does not dose any fluid.
    * observable: yes

## Errors
### DefinedExecutionErrors
- `DosageFinishedUnexpectedly`: The dosage could not be finished properly due to an error.

### UndefinedExecutionErrors
- none





# PumpUnitController
Allows to control the currently used units for passing and retrieving flow rates and volumes to and from a pump.

## Commands
### `SetFlowUnit`
Sets the flow unit for the pump.
The flow unit defines the unit to be used for all flow values passed to or retrieved from the pump.

Parameters:
- `Prefix`: The prefix for the velocity unit.
- `VolumeUnit`: The volume unit (numerator) of the velocity unit.
- `TimeUnit`: The time unit (denominator) of the velocity unit.

Response:
- none

observable: no

### `SetVolumeUnit`
Sets the default volume unit.
The volume unit defines the unit to be used for all volume values passed to or retrieved from the pump.

Parameters:
- `Prefix`: The prefix of the SI unit.
- `VolumeUnit`: The volume unit identifier.

Response:
- none

observable: no

## Properties
- `FlowUnit`: The currently used flow unit.
    * observable: yes
- `VolumeUnit`: The currently used volume unit.
    * observable: yes

## Errors
### DefinedExecutionErrors
- none

### UndefinedExecutionErrors
- none

# PumpDriveControlService
Functionality to control and maintain the drive that drives the pump.  
Allows to initialize a pump (e.g. by executing a reference move) and obtain status information about the pump drive's current state (i.e. enabled/disabled).

## Commands
### `InitializePumpDrive`
Initialize the pump drive (e.g. by executing a reference move).

Parameters:
- none

Response:
- `Success`: A boolean value where `false` represents a failed initialisation and `true` represents a successful initialisation.

observable: no

### `EnablePumpDrive`
Set the pump into enabled state.

Parameters:
- none

Response:
- none

observable: no

### `DisablePumpDrive`
Set the pump into disabled state.

Parameters:
- none

Response:
- none

observable: no

## Properties
- `PumpDriveState`: The current state of the pump. This is either enabled or disabled. Only if the sate is enabled, the pump can dose fluids.
    * observable: yes
- `FaultState`: Returns if the pump is in fault state. If the value is true (i.e. the pump is in fault state), it can be cleared by calling [`EnablePumpDrive`](#EnablePumpDrive).
    * observable: yes

## Errors
### DefinedExecutionErrors
- `InitializationFailed`: The initialization did not end properly.

### UndefinedExecutionErrors
- none

# SyringeConfigurationController
Syringe pump specific functions for configuration.

## Commands
### `SetSyringeParameters`
Set syringe parameters.  
If you change the syringe in one device, you need to setup the new syringe parameters to get proper conversion of flow rate und volume units. 

Parameters:
- `InnerDiameter`: Inner diameter of the syringe tube in millimetres. 
- `MaxPistonStroke`: The maximum piston stroke defines the maximum position the piston can be moved to before it slips out of the syringe tube. The maximum piston stroke limits the maximum travel range of the syringe pump pusher. 

Response:
- none

observable: no


## Properties
- `InnerDiameter`: Inner diameter of the syringe tube in millimetres.
    * observable: Yes
- `MaxPistonStroke`: The maximum piston stroke defines the maximum position the piston can be moved to before it slips out of the syringe tube.
    * observable: Yes

## Errors
### DefinedExecutionErrors
- none

### UndefinedExecutionErrors
- none

# ValvePositionController
Allows to specify a certain logical position for a valve. The [`CurrentPosition`](#Properties-2) property can be querried at any time to obtain the current valve position.  

## Commands
### `SwitchToPosition`
Switches the valve to the specified position. The given position has to be less than the [`NumberOfPositions`](#NumberOfPositions) or else a ValidationError will be thrown.

Parameters:
- `Position`: The target position that the valve should be switched to.

Response:
- `Success`: A boolean value where `false` represents a failed command execution and `true` represents a successful command execution.

observable: no

### `TooglePosition`
This command only applies for 2-way valves to toggle between its two different positions. If the command is called for any other valve type a `ValveNotToggleable` error is thrown.

Parameters:
- none

Response:
- `Success`: A boolean value where `false` represents a failed command execution and `true` represents a successful command execution.

observable: no

## Properties
- `NumberOfPositions`: The number of valve positions available.
    * observable: no
- `CurrentPosition`: The current logic valve position. This is a value between 0 and `NumberOfPositions` - 1.
    * observable: yes

## Errors
### DefinedExecutionErrors
- `ValveNotToggleable`: The current valve does not support toggling because it has more than only two possible positions.

### UndefinedExecutionErrors
- none

