@echo off
REM Installs sila_cetoni

set SILA_VENV_PATH=%~dp0\.sila_cetoni_venv

echo Installing...

set python=
for /f %%i in ("python python3") do (
    for /f "usebackq tokens=*" %%j in (`where %%i`) do (set python="%%j" & goto :next)
)
:next

if %python% == "" (
    echo "Could not find a python executable! Either install python 3 or adjust your PATH environment variable to point to the directory where python is located."
    exit /b 1
)

%python% -m pip install virtualenv
%python% -m virtualenv "%SILA_VENV_PATH%"

setlocal EnableDelayedExpansion
for /f "delims=" %%i in (%python%) do set python="%SILA_VENV_PATH%\Scripts\%%~nxi"
cd %~dp0
!python! -m pip install .

echo Done

exit /b
