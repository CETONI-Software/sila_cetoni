![SiLA CETONI Logo](doc/sila_header.png)

<!-- omit in toc -->
# sila_cetoni
This repository contains the official [SiLA 2](https://sila-standard.com/) drivers for a variety of [CETONI devices](https://www.cetoni.com/products/).
These SiLA 2 drivers are based on the [CETONI SDK for Python](https://github.com/CETONI-Software/qmixsdk-for-python) in order to control the devices.

- [Getting Started](#getting-started)
  - [Installation](#installation)
    - [sila_cetoni](#sila_cetoni)
    - [CETONI SDK](#cetoni-sdk)
  - [Running SiLA 2 CETONI servers](#running-sila-2-cetoni-servers)
- [Troubleshooting](#troubleshooting)
  - ['undefined symbol: __atomic_exchange_8' on Raspberry Pi](#undefined-symbol-__atomic_exchange_8-on-raspberry-pi)
- [Modifying the drivers](#modifying-the-drivers)
- [Contributing](#contributing)

## Getting Started
> ##### Note:
> These SiLA 2 drivers were developed and tested under Windows and Linux (Ubuntu 19.04 and Raspbian Buster on a Raspi 3B+) and are therefore expected to work on these systems.
> Other operating system should work as well, but have not been tested yet!

### Installation
#### sila_cetoni
Install the sila_cetoni package with
```console
$ pip install .
```
It is recommended to install these things in a virtual environment to not interfere with anything in your system's environment.  
This will install all Python dependencies for sila_cetoni most notably `sila_python` as well as sila_cetoni itself.
This means you can not only use the provided console script to run your CETONI device configurations but also build upon the SiLA 2 implementations and build you own applications.

#### CETONI SDK
Additionally, you'll of course need the CETONI SDK with the Python Integration.

For instructions on how to install the CETONI SDK for Python on your system and get a valid configuration for your devices see the [CETONI SDK Documentation].  
On Linux be sure to also install the correct SocketCAN driver (either [SysTec](https://www.systec-electronic.com/en/company/support/device-driver/) or [IXXAT](https://www.ixxat.com/support/file-and-documents-download/drivers/socketcan-driver) depending on your CETONI base module).

### Running SiLA 2 CETONI servers
> ##### Note:
> If your system contains any CETONI devices you always need a valid device configuration created with the [CETONI Elements] software in order to use sila_cetoni.  
> If you only want to control a Sartorius balance, for example, you don't need a device configuration.

Running the corresponding SiLA 2 servers for your system is always done through the `sila-cetoni` console script that gets installed by `pip`.

Simply run the script giving it the path to the CETONI device configuration folder as an argument (if necessary):
```shell
$ sila-cetoni -c <path/to/your/device_config>
```

To se a list of all available command line options run
```shell
$ sil-cetoni --help
```

> ##### Note:
> If you have problems running the `sila-cetoni` console script try running the application via the module syntax:
> ```shell
> $ python -m sila_cetoni.application <arguments...>
> ```
> Also, in case you get the error *ModuleNotFoundError: No module named 'qmixsdk'* 
> you have to point the script to the correct location of the CETONI SDK. This can
> easily be done by setting the `CETONI_SDK_PATH` environment variable before calling
> `sila-cetoni`.


You can play around with the server's and their features by using the freely available [SiLA Browser](https://unitelabs.ch/technology/plug-and-play/sila-browser/) or even [CETONI Elements], for example.  
Or you can also write your own SiLA Client software using the Python or any other of the [reference implementations](https://gitlab.com/SiLA2/) of SiLA 2.

## Troubleshooting
### 'undefined symbol: __atomic_exchange_8' on Raspberry Pi
You might get the following error when trying to run the driver on a Raspberry Pi:
```console
Traceback (most recent call last):
  File "/home/pi/sila_cetoni/sila_cetoni.py", line 43, in <module>
    from application.application import Application, DEFAULT_BASE_PORT
  File "/home/pi/sila_cetoni/application/application.py", line 35, in <module>
    from sila2lib.sila_server import SiLA2Server
  File "/home/pi/sila_python/sila_library/sila2lib/sila_server.py", line 36, in <module>
    import grpc
  File "/home/pi/.local/lib/python3.9/site-packages/grpc/__init__.py", line 22, in <module>
    from grpc import _compression
  File "/home/pi/.local/lib/python3.9/site-packages/grpc/_compression.py", line 15, in <module>
    from grpc._cython import cygrpc
ImportError: /home/pi/.local/lib/python3.9/site-packages/grpc/_cython/cygrpc.cpython-39-arm-linux-gnueabihf.so: undefined symbol: __atomic_exchange_8
```
This is a known bug in gRPC (https://github.com/grpc/grpc/issues/20400) and there exists a workaround, too (https://github.com/opencv/opencv/issues/15278#issuecomment-520893950):  
You just need to modify `sila_cetoni.sh` like this:
```shell
# ...
LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0 $curr_dir/sila-cetoni $@
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^-- add this
#...
```

## Modifying the drivers
You are, of course, free to play around with the code inside this repository.

The implementation files have been generated using the `sila-codegen` script that comes with `sila_python`.
Refer to [its documentation](https://gitlab.com/SiLA2/sila_python/-/blob/master/docs/add-and-update-features.md) to see how to add and update existing feature implementations.

This repository uses a separate python package for each Feature Category, e.g. all SiLA Features of the 'de.cetoni/pumps.syringepumps' category are implemented in the `sila_cetoni.pumps.syringepumps` package.

## Contributing
You can change and improve the current implementations, create new Commands, Properties, or even whole new SiLA 2 Features.
If you think your changes might be interesting for us and other users as well, feel free to [open a pull request](https://github.com/CETONI-Software/sila_qmix/compare) on the GitHub project page.
Also, if you have any questions or problems with the drivers, just open an issue and we'll try to help you.

[CETONI SDK Documentation]: https://cetoni.de/downloads/manuals/CETONI_SDK/index.html
[CETONI Elements]: https://cetoni.com/cetoni-elements/
