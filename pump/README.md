![neMESYS SiLA2 Logo](doc/sila_nemesys_logo.png) 

# neMESYS SiLA2 driver
This repository contains the official [SiLA2](https://sila-standard.com/) driver for the [neMESYS High Precision Syringe Pumps](https://www.cetoni.com/products/pumps). This SiLA2 driver is based on the [Qmix SDK for Python](https://github.com/CETONI-Software/qmixsdk-for-python) for device control of the neMESYS pumps.

# Getting Started
> ### Note:
> These SiLA2 drivers were developed and tested under Linux (Ubuntu 19.04 and Raspbian Buster on a Raspi 3B+) and are therefore expected to work on Linux systems, other operating system should work as well, but have not been tested yet!

## Install required dependencies
The SiLA2 driver in this repository needs the following dependencies to work correctly:
* SocketCAN driver (either [SysTec](https://www.systec-electronic.com/en/company/support/device-driver/) or [IXXAT](https://www.ixxat.com/support/file-and-documents-download/drivers/socketcan-driver) depending on your CETONI base module)
* QmixSDK for Python
* SiLA2 Python Library
* (gRPC Library + protobuf compiler `protoc`)

### QmixSDK installation
For instructions on how to install the QmixSDK for Python on your system and get a valid Qmix configuration for your pumps see the [QmixSDK Documentation](https://www.cetoni.de/fileadmin/user_upload/Documents/Manuals/QmixSDK/index.html).

### SiLA2 Python Library installation
> ### Note:
> SiLA Python needs **Python 3.6 or greater** to run properly.  
> See https://gitlab.com/SiLA2/sila_python for more information on this.

Installing the SiLA 2 Python library is now as simple as running 
```shell
$ pip3 install sila2lib
```
You can use a python virtual environment if you like. Be sure to activate the virtualenv **before** you install `sila2lib`.

This automatically installs the gRPC library and the protobuf compiler `protoc`, as well. Now you are ready to *use* the driver in the `impl` directory.
Skip ahead to the [Running SiLA2 neMESYS servers](#running-sila2-nemesys-servers) section if you just want to use the driver.
Keep reading if you also want to modify or extend the driver and rebuild it yourself.  

### SiLA2 Python code generator installation
If you want to build the driver yourself, you need the SiLA 2 Python code generator, as well.  
Installing the code generator is similarly simple:
```shell
$ pip3 install sila2codegenerator
```
Now you are also ready to build the driver in the `impl` directory yourself (See [Building the driver](#building-the-driver) for more details on how to build the driver yourself).

## Running SiLA2 neMESYS servers
As described above, the `impl` directory already contains a fully functioning SiLA2 driver. The fastest way to get something up and running is by just running the `SiLA_neMESYS.py` script giving it a path to a valid Qmix configuration folder:
```shell
$ python3 SiLA_neMESYS.py ~/Documents/my_qmix_config
```
This requires you to have all necessary environment variables set (i.e. `$PATH`, `$PYTHON_PATH` and `$LD_LIBRARY_PATH`) to point to the correct paths of your QmixSDK's root directory, python directory and lib directory, respectively. See the [QmixSDK for Python Documentation](https://www.cetoni.de/fileadmin/user_upload/Documents/Manuals/QmixSDK/QmixSDK_Python.html) for more information on this.  
If you don't have these variables set yet, you can also use the provided wrapper shell script in this repository. Before you use it, make sure the script uses the correct path to your QmixSDK installation. Simply edit the `$QMIXSDK_PATH` variable to point to the correct directory. Then you can simply run the SiLA neMESYS server like this:
```shell
$ ../qmixsdk-py_wrapper.sh SiLA_neMESYS.py ~/Documents/my_qmix_config
```

You can test and play around with the currently implemented SiLA2 Features by running the `impl/neMESYS_Client.py` in a different terminal or you can use UniteLabs' SiLA Browser. You can download SiLA Browser from [here](http://www.unitelabs.ch/technology/plug-and-play/try-it-out). It runs as a web application in the browser (usually on port 8080) and should discover running SiLA2 neMESYS servers itself. If not, you can also manually enter the IP address (127.0.0.1) and ports the SiLA2 neMESYS servers are running on (by default it's port 50051 and up, depending on the number of pumps you have).

# Building the driver
If, however, you want to change the implementation or if you want to add new SiLA Features, you can rebuild the driver yourself.
To use the code generator you need to run the following command from the root directory of this repository:
```shell
$ silacodegenerator -o build --ignore-overwrite-warning -b .
```
This generates the protobuf files and sample implementations for the server/client and puts them in the `build` directory. If you added a new SiLA2 Feature just copy the new files into the `impl` directory and add your own implementations.  
If you just changed or added a property or a command to a Feature, you only need to copy the corresponding lines that changed in the server/client implementations. This means, if you change something in the Feature Definition of the `PumpDriveControlService`, you need to copy the modified lines of the following files:
* `build/neMESYS_server.py`
* `build/neMESYS_client.py`
* `build/PumpDriveControlService/PumpDriveControlService_servicer.py`
* `build/PumpDriveControlService/PumpDriveControlService_simulation.py`
* `build/PumpDriveControlService/PumpDriveControlService_real.py`

Further, you need to copy the following files/directories entirely:
* `build/meta/PumpDriveControlService.pickle`
* `build/PumpDriveControlService/grpc/`
* `build/PumpDriveControlService/PumpDriveControlService_default_arguments.py`

To simplify this process you can use a tool like [Meld](https://meldmerge.org/), for example, which lets you compare whole directories and highlights the changes for you.

Then add your implementations for the new properties or commands.

# Contributing
You can change and improve the current implementations, create new commands, properties, or even whole new SiLA2 Features.
If you think your changes might be interesting for other us and users as well, feel free to open a pull request.  
Also, if you have any questions or problems with the drivers, just open an issue and we'll try to help you.
