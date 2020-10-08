@echo off
REM Wrapper script for all python scripts that use the QmixSDK Python Integration
REM It sets the PATH, PYTHONPATH and LD_LIBRARY_PATH environment variables so that
REM python and ctypes find the necessary files and shared libraries.


REM change this path to point to your QmixSDK installation
set QMIXSDK_PATH=C:\QmixSDK

set PATH=%QMIXSDK_PATH%;%PATH%
set PYTHONPATH=%QMIXSDK_PATH%\lib\python;%PYTHONPATH%

PUSHD
for %%F in (%1) do set basename=%%~nxF
for %%F in (%1) do set dirname=%%~dpF
for /f "tokens=1,* delims= " %%a in ("%*") do set PARAMS=%%b
cd %dirname%
python %basename% %PARAMS%
POPD
