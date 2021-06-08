![SiLA CETONI Logo](doc/sila_header.png)

<!-- omit in toc -->
# SiLA Qmix
This repository contains the official [SiLA 2](https://sila-standard.com/) drivers for a variety of [CETONI devices](https://www.cetoni.com/products/).
These SiLA 2 drivers are based on the [CETONI SDK for Python](https://github.com/CETONI-Software/qmixsdk-for-python) in order to control the devices.

- [Getting Started](#getting-started)
  - [Installation](#installation)
    - [Python dependencies](#python-dependencies)
    - [CETONI SDK](#cetoni-sdk)
  - [Running SiLA 2 CETONI servers](#running-sila-2-cetoni-servers)
    - [Windows](#windows)
    - [Linux](#linux)
- [Modifying the drivers](#modifying-the-drivers)
  - [Repository layout](#repository-layout)
  - [Generate the prototype code from the FDL](#generate-the-prototype-code-from-the-fdl)
- [Contributing](#contributing)

## Getting Started
> ##### Note:
> These SiLA 2 drivers were developed and tested under Windows and Linux (Ubuntu 19.04 and Raspbian Buster on a Raspi 3B+) and are therefore expected to work on these systems.
> Other operating system should work as well, but have not been tested yet!

### Installation
#### Python dependencies
Install the requirements for SiLA CETONI from PyPI with
```console
$ pip install -r requirements.txt
```
It is recommended to install these things in a virtual environment to not interfere with anything in your system's environment.  
This will install all Python dependencies for SiLA CETONI most notably `sila_python` and its codegenerator (`sila2codegenerator`).

#### CETONI SDK
Additionally you'll of course need the CETONI SDK with the Python Integration.

For instructions on how to install the CETONI SDK for Python on your system and get a valid configuration for your devices see the [CETONI SDK Documentation](https://www.cetoni.de/fileadmin/user_upload/Documents/Manuals/QmixSDK/index.html).  
On Linux be sure to also install the correct SocketCAN driver (either [SysTec](https://www.systec-electronic.com/en/company/support/device-driver/) or [IXXAT](https://www.ixxat.com/support/file-and-documents-download/drivers/socketcan-driver) depending on your CETONI base module).

### Running SiLA 2 CETONI servers
> ##### Note:
> You always need a valid device configuration created with the [CETONI Elements software](https://www.cetoni.com/products/qmixelements/) in order to use SiLA CETONI.

Running any valid device configuration to get the corresponding SiLA 2 servers is always done through the `sila_cetoni.py` wrapper script located in the root of this repository.

#### Windows
On Windows you can simply run the script through Python giving it the path to the Qmix configuration folder as its argument:
```cmd
> python .\sila_cetoni.py <path\to\your\device_config>
```

#### Linux
On Linux this is not as easy, unfortunately.  
This is due to how Python loads shared object files.
You need to specify the dynamic library search path *before* running the `python` executable in order for the CETONI SDK to find all necessary libraries.
This can be done by manually specifying the `PATH`, `PYTHONPATH` and `LD_LIBRARY_PATH` environment variables before running `sila_cetoni.py`.  
To make this a bit easier you can use the provided shell script `sila_cetoni.sh`.
You only need to edit the path to the CETONI SDK installation folder in this file.  
After that you can run this script giving it only the path to your configuration folder as its argument:
```console
$ ./sila_cetoni.sh <path/to/your/device_config>
```
The script will set the necessary variables and run the python script for you.

You can play around with the server's and their features by using the freely available [SiLA Browser](https://unitelabs.ch/technology/plug-and-play/sila-browser/), for example.  
Or you can also write your own SiLA Client software using the Python or any other of the [reference implementations](https://gitlab.com/SiLA2/) of SiLA 2.

## Modifying the drivers
You are of course free to play around with the code inside this repository.
Especially when modifying the feature definitions you need to bear in mind a few things.
The following is meant to be some kind of guidance for your first steps modifying the code.

### Repository layout
The repository is structured in the following way:
```
sila_cetoni
|- features/de/cetoni/        # folder structure according to SiLA 2 Part A
|  |- controllers/            # contains all feature definitions grouped by category
|  |  `- ControlLoopService.sila.xml
|  |- core/
|  `- ...
|- impl/
|  |- common/                 # common functionality required by all feature implementations
|  `- de/cetoni/              # folder structure as in features/ (above)
|     |- controllers/         # contains all feature implementations grouped by category
|     |  |- gRPC/             # contains the gRPC generated code (must not be edited!)
|     |  |- ControlLoopService_servicer.py    # serves as a bridge between the server and the actual implementations
|     |  |- ControlLoopService_real.py        # the real implementation of this feature
|     |  |- ControlLoopService_simulation.py  # the simulated implementation of this feature
|     |  `- ...
|     |- core/
|     `- ...
|- serv/                            # contains server and client implementations of all services
|  |- controllers/
|  |  |- QmixControl_server.py      # server implementation of the QmixControl service
|  |  |- QmixControl_client.py      # client implementation of the QmixControl service
|  |  `- service_description.json   # service description defines the features to use for this service
|  |- io/
|  `- ...
|- templates/                       # template files for developing new features
|  |- Feature.sila.xml              # FDL template file
|  `- service_description.json      # service description template
|- sila_cetoni.py                   # standalone python wrapper script to run arbitrary servers
`- sila_cetoni.sh                   # standalone shell wrapper script for Linux
```

### Generate the prototype code from the FDL
If you modify a feature definition (`.sila.xml` file) you need to regenerate the gRPC Python code and the SiLA implementation prototypes.
This is done using the `sila2codegenerator` from the `sila_python` reference implementation.
The code generator has been automatically installed if you followed the step in [Installation](#installation).

To show you the code generation process we're going to use the `PumpFluidDosingService` syringe pump feature as an example.
In this case the feature definition resides in the file `sila_cetoni/features/de/cetoni/pumps/syringepumps/PumpFluidDosingService.sila.xml`.  
Let's say you've added anew command to this feature.
The code regeneration process is now as follows:

1. Our target directory is the `serv/pumps/syringepumps/` folder. 
   This folder already contains the `service_description.json` file that tells the code generator which feature we want our syringe pump server to have.
   If you added a new feature you need to add it to the `SiLA_feature_list` in the service description.
2. Then run the code generator from the root directory (i.e. `sila_cetoni/`) with the following command
   ```console
   $ silacodegenerator -b -o <target_dir> --service-description ../<target_dir>/service_description features/
   ```
   
   E.g. to generate the code for the 'pumps/syringepumps' category you'd need to run
   ```console
   $ silacodegenerator -b -o serv/pumps/syringepumps --service-description ../serv/pumps/syringepumps/service_description features/
   ```
3. This will create the folders with prototype implementations for each feature.
   You'll also be asked if you want to overwrite the existing `_server.py` and `_client.py` files.
   Answer this with `n`.
4. After that delete all directories you don't need and only move the `gRPC/` directory of th current feature into the correct directory in `impl/de/cetoni/` (i.e. in our case into `impl/de/cetoni/pumps/syringepumps/PumpFluidDosingService/`).
5. Finally, inspect each of the `_servicer.py`, `_real.py` and `_simulation.py` files of te feature to find the prototype definition(s) of the functions for your new command and copy them into the correct file in the `impl/` folder.
   Then simply add your implementation in the `_real.py` file (the `_simulation.py` files have not been implemented because Qmix configurations support simulated devices already hence we don't need to use the simulation functionality of `sila_python`).

## Contributing

You can change and improve the current implementations, create new Commands, Properties, or even whole new SiLA 2 Features.
If you think your changes might be interesting for us and other users as well, feel free to [open a pull request](https://github.com/CETONI-Software/sila_qmix/compare) on the GitHub project page.
Also, if you have any questions or problems with the drivers, just open an issue and we'll try to help you.
