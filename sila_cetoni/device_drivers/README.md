****<!-- omit in toc -->
# SiLA CETONI Device Drivers

This directory contains additional driver implementations for non-CETONI devices that are supported by the SiLA CETONI SDK.

- [SiLA CETONI Device Drivers](#sila-cetoni-device-drivers)
  - [Overview](#overview)
  - [Supported Devices](#supported-devices)
  - [Directory Structure](#directory-structure)
  - [Example: Balances](#example-balances)
    - [The Feature Definition](#the-feature-definition)
    - [The Device Driver Interface](#the-device-driver-interface)
    - [The Feature Implementation](#the-feature-implementation)
    - [The Device Driver](#the-device-driver)
    - [Serial Device Driver Interface](#serial-device-driver-interface)
    - [Main Script](#main-script)
  - [Supplying your own Device Driver](#supplying-your-own-device-driver)
    - [Adding a new balance driver](#adding-a-new-balance-driver)
    - [Adding a new device type driver](#adding-a-new-device-type-driver)
      - [New `Device` subclass](#new-device-subclass)
      - [Extend `ApplicationSystem`](#extend-applicationsystem)
      - [Extend `Application`](#extend-application)

## Overview
The SiLA CETONI SDK cannot only be used in combination with a CETONI device configuration to expose your CETONI system as SiLA 2 Servers.
You can also use devices from other vendors with this SDK.

## Supported Devices
- Sartorius Balances (with a serial (USB) connection to a PC)

## Directory Structure
This directory contains two things:
the driver interface classes for each device type and the actual implementations for each device.  
This allows for the feature implementations to be agnostic of the specific device driver they should use.
The feature implementations access the device driver only through the common driver interface and not through the specific device driver.

## Example: Balances
Let's look at this using balances as an example.

### The Feature Definition
The first thing we're going to look at is the Feature Definition of a `BalanceService` Feature.
This Feature provides the simplest interface to communicate with a balance:
it has one Observable Property called `Value` which provides the current value of the balance in grams and an Unobservable Command to tare the balance called `Tare` (see [features/de/cetoni/balance/BalanceService.sila.xml]).

Using the sila_python code generator we can generate the corresponding SiLA Server and Client as well as the Feature implementation skeleton (refer to the [README.md] in the main directory for instructions on how to do this).  
To implement the Feature we're going to need our balance driver which is what we'll look at next.

### The Device Driver Interface
The device driver interface is the bare minimum that each specific device driver has to implement.
According to our Feature Definition we need two things: a value and a tare function.  
Thus, the interface could look like this
```py
from abc import ABC, abstractmethod

class BalanceInterface(ABC):
    """
    Interface for a balance device driver
    """

    __value: float

    def __init__(self):
        super().__init__()

    @property
    def value(self) -> float:
        """
        Returns the current value of the balance
        """
        return self.__value

    @value.setter
    def value(self, value: float):
        """
        Sets the value of the balance to `value`
        """
        self.__value = value

    @abstractmethod
    def tare(self):
        """
        Tare the balance
        """
        raise NotImplementedError()
```

We're using a Python property for the value of the balance and an abstract method for the tare function.
This function has to be implemented later by the specific device driver because the interface does not know how the specific device can be tared.

This `BalanceInterface` class is defined in the [balance/abc.py] file.

### The Feature Implementation
Now we can already implement our Feature since it will only be using the `BalanceInterface` and not the specific driver classes.  
We're going to start in the `balance.balance_service.Server` class which creates the `BalanceServiceImpl` Feature implementation.
```py
from sila_cetoni.device_drivers.balance import BalanceInterface
from .feature_implementations.balanceservice_impl import BalanceServiceImpl

class Server(SilaServer):
    def __init__(self, balance: BalanceInterface, ...):
        super().__init__(...)

        self.balanceservice = BalanceServiceImpl(balance, self.child_task_executor)
        self.set_feature_implementation(BalanceServiceFeature, self.balanceservice)
```

As you can see here the `Server` receives the balance driver as an argument to it's `__init__` function (we're going to see [later](#main-script) how the Server gets the specific balance driver).
The balance driver is then passed on to the `BalanceServiceImpl` class that contains the actual Feature implementation.

```py
from sila_cetoni.device_drivers.balance import BalanceInterface
from ..generated.balanceservice import BalanceServiceBase, Tare_Responses


class BalanceServiceImpl(BalanceServiceBase):
    __balance: BalanceInterface
    __stop_event: Event

    def __init__(self, balance: BalanceInterface, executor: Executor):
        super().__init__()
        self.__balance = balance
        self.__stop_event = Event()

        def update_value(stop_event: Event):
            new_value = value = self.__balance.value
            while not stop_event.is_set():
                self.update_Value(self.__balance.value)
                time.sleep(0.1)

        # initial value
        self.update_Value(self.__balance.value)

        executor.submit(update_value, self.__stop_event)

    def Tare(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Tare_Responses:
        self.__balance.tare()

    def stop(self) -> None:
        self.__stop_event.set()
```

The Feature implementation saves the balance driver in a member variable.

The implementation of the `Tare` Command is as easy as it gets:
it simply calls `tare()` on the balance driver and returns an empty Response.  
The `Value` Property is implemented as a loop that continuously updates the current value.
The sila_python implementation handles sending the values to the Clients.
The loop will eventually stop when the server is stopped (then `stop` will be called on all Feature implementation classes).  
If you want to decrease the amount of values sent you can change the loop to only send a new value when it is different from the value before.
See the complete Feature implementation in [balanceservice_impl.py] for a possible implementation.

### The Device Driver
The only thing missing now is the specific driver implementation.

For this example we're going to use a Sartorius balance.
This balance can be connected to a PC via a USB cable and supports a fairly easy serial protocol.

To implement the serial protocol we use the [`pySerial`] library.
```py
import serial
import threading

class SartoriusBalance(BalanceInterface):
    __serial: serial.Serial
    __read_thread: threading.Thread
    
    def __init__(self, port: str = ""):
        super().__init__()

        self.__serial = serial.Serial()
        if port:
            self.__serial.port = port

    def __autodetect_serial_port(self):
        #...

    def open(self, port: str = ""):
        if self.__serial.is_open:
            return
        if not port
            self.__autodetect_serial_port()
        else:
            self.__serial.port = port
        self.__serial.open()

        self.__read_thread = threading.Thread(target=self.__read_value)
        self.__read_thread.start()

    def __read_value(self):
        # data = 'G     +   0.0006 !  '
        #               ^~~~~~~~~~ match this (and remove spaces later)
        value_regex = re.compile('[+-]?\s+\d+\.\d+')

        while self.__serial.is_open:
            data = self.__serial.read_until()
            self.value = float(value_regex.findall(data)[0].replace(' ', ''))

    def tare(self):
        self.__serial.write('T\r\n')

    def close(self):
        self.__serial.close()
        self.__read_thread.join()
```

Our custom `SartoriusBalance` driver class has to derive from the common `BalanceInterface`, of course.
It has two member variables:
one for the serial communication to the device and one for the thread where we continuously read the current value from the balance.

In the `__init__` function it initializes the member for the serial communication and sets the port if available.  
If the port was not given in `__init__` it can also be specified when calling the `open` function.
This function will open the serial communication on the given port.
It also immediately creates and starts another thread that will continuously read all data from the balance.  
If still no port was provided the `__autodetect_serial_port` function will try all available serial ports and pick the first one that responds as a Sartorius balance.
The actual implementation doesn't really matter here; refer to [balance/abc.py] for this.  
Onto the `__read_value` function.
This function is responsible for reading all data that comes from the balance.
These Sartorius balances that we're using in this example send their current value continuously via the serial protocol.
This data is read by this function and converted into a floating point value (using a regular expression, as you can see).  
The `tare` function does nothing more than writing the string `'T\r\n'` to the serial port.  
When the communication should be stopped the `close` function needs to be called which closes the serial communication and waits for the `__read_thread` to finish.  

And that's already it.
Now we have a fully functioning device driver for a Sartorius balance.

### Serial Device Driver Interface
Reading the value from the balance in a loop is not really the best solution, however.
It's better to use `pySerial`'s [Threading API] for these things which handles of the asynchronous stuff for us.  
One drawback of this method is, however, that we have to implement two more classes for our specific case:
a reader class that reads from and writes to the device and a reader thread class that implements the read loop.

Fortunately, both classes are not that difficult to implement.  
Let's start with the reader thread class.
This class has to inherit the `serial.threaded.ReaderThread` class.
We only need to provide the `__init__` function in our case which just passes some arguments to the base class and stores the actual device driver instance.
This device driver instance will later be used by the reader to be able to set a new value that was read from the serial connection.  
The reader class needs to inherit the `serial.threaded.Protocol` or any of its subclasses (in our case we'll use the `serial.threaded.LineReader` class because we're reading and writing whole lines).
An instance of this class will be created for us by the reader thread class.
We need to implement 3 methods in this class:
- `connection_made`: this function is called with the reader thread instance that created this reader class and is called after the serial communication has been opened successfully
- `handle_line` (actually, if we were inheriting `serial.threaded.Protocol` this would be called `data_received` but `serial.threaded.LineReader` already converts the raw data into lines): this function is continuously called when new data is available and we simply do the conversion of the data to a floating point value in this function
- `connection_lost`: this function is called with an optional `Exception` as an argument when the serial connection was closed; the exception optionally contains a traceback of what went wrong

Refer to [balance/abc.py] for the actual implementation of these classes.  
You'll se another class called `SerialBalanceInterface` there which already contains the boilerplate code for the serial communication as just described.
So, if you want to implement a device driver for a balance from a different vendor that also uses a serial protocol then you can derive your driver class from this interface instead of deriving from `BalanceInterface` and doing the serial communication completely from scratch.

### Main Script
The main script is responsible for passing the specific balance driver that should be used to the `BalanceServer`.
In our case we create a `SartoriusBalance` instance and use its ability to automatically detect the serial port of a balance.
```py
from sila_cetoni.device_drivers.balance import sartorius_balance
from sila_cetoni.balance.balance_service.server import Server
# ...
balance = sartorius_balance.SartoriusBalance()
balance.open() # automatically detects a connected balance
server = Server(balance=balance, ...)
server.start(...)
```

## Supplying your own Device Driver
### Adding a new balance driver
If you also happen to have a balance that you just need to write a (serial) driver for then all you need to do is derive your own class from `BalanceInterface` or `SerialBalanceInterface` and implement all abstract methods.  
Additionally, you'll need to modify `application.ApplicationSystem.get_available_balances` to use your specific balance driver class instead of the `SartoriusBalance` class.

### Adding a new device type driver
If you want to add a device driver and a Feature for a completely new type of device just follow the description of the [Example].  
To have the main script spin up a SiLA Server for this device you'll need to do some more adjustments in the `application` module.

#### New `Device` subclass
The SiLA CETONI SDK uses a simple `Device` class and its subclasses to represent the physical devices that make up a SiLA Server.
That means if you want to have a new SiLA Server spun up you need to define a corresponding `Device` subclass in `application.device`:
```py
# in application/device.py
from sila_cetoni.device_drivers import my_driver # the common interface for your device type
#...
class MyDevice(Device):
    device: my_driver.MyDriverInterface

    def __init__(self, name: str, device: my_driver.MyDriverInterface = None):
        super().__init__(name)
        self.device = device
```

#### Extend `ApplicationSystem`
The `application.ApplicationSystem` class is the main class that contains all devices that represent your physical application system.

First, add a new member variable that is a list of all devices of your device type.
Then, in the `__init__` function fill that list.
```py
# in application/system.py
from .device import ..., MyDevice
from device_drivers.my_device_type import my_device # the specific device driver

class ApplicationSystem(metaclass=Singleton):
    #...
    my_devices: List[my_device.MyDevice] = []

    def __init__(self, ...):
        #...
        self.my_devices = self.get_available_my_devices()

    def get_available_my_devices(self) -> List[my_device.MyDevice]:
        devices = []
        my_devices_count = ...
        for i in range(my_devices_count):
            dev = my_device.MyDevice()
            # dev.open() or something similar to start the communication
            device = my_device.MyDevice(f"My_Device_{i}", dev)
            devices += [device]
        return devices
```
As you can see, we offloaded the detection of available devices into a separate function called `get_available_my_devices`.

#### Extend `Application`
The main application logic (like creating and starting the SiLA 2 Servers) is handled by the `application.Application` class.

Here, you only need to adjust the `create_servers` function.
Simply add another loop that goes through all of your devices and creates the corresponding SiLA 2 Server:
```py
class Application(metaclass=Singleton):
    #...
    def create_servers(self):
        #...
        #---------------------------------------------------------------------
        # my_device
        for my_device in self.system.my_devices:
            server_name = my_device.name.replace("_", " ")

            from ..my_device_type.my_device_type_service.server import Server
            server = Server(my_device=my_device.device, server_name=server_name)
            servers += [server]
```

The `Application` class will now automatically take care of starting and stopping the Servers for you.


[features/de/cetoni/balance/BalanceService.sila.xml]: ../features/de/cetoni/balance/BalanceService.sila.xml
[README.md]: ../README.md
[balance/abc.py]: balance/abc.py
[balanceservice_impl.py]: ../balance/balance_service/feature_implementations/balanceservice_impl.py
[`pySerial`]: https://pyserial.readthedocs.io/en/latest/pyserial.html
[Threading API]: https://pyserial.readthedocs.io/en/latest/pyserial_api.html#module-serial.threaded
[Example]: #example-balances
