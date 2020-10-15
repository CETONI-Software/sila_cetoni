# SiLA2 Driver for Qmix Control Devices

## Running:
Make sure to have `sila2lib` installed (`pip install sila2lib`) and activated the correct virtualenv (if applicable).

### Windows:
```cmd
> python sila_qmix.py <path-to-qmix-config>
```

### Linux:
```console
$ ./sila_qmix.sh <path-to-qmix-config>
```

## Features:
- setting a SetPoint for the Control Channel
- starting the Control Loop
- observing the current value of the Loop Output
- stopping the Control Loop
