#!/usr/bin/env bash
#
# Installs sila_cetoni
#
#set -x

function fail() {
    echo "ERROR: $@"
    exit 1
}

HERE=`realpath ${0%/*}`
SILA_VENV_PATH=$HERE/.sila_cetoni_venv

echo Installing...

for i in "python" "python3"; do
    python=`which $i`
    [ $? -eq 0 ] && (`$python --version | grep -qi 'python 3'`) > /dev/null 2>&1
    [ $? -eq 0 ] && break;
done

[ -z $python ] && fail "Could not find a python executable! Either install Python 3 or adjust your PATH environment variable to point to the directory where python is located."

$python -m pip install virtualenv
$python -m virtualenv $SILA_VENV_PATH

cd $HERE
$SILA_VENV_PATH/bin/${python##*/} -m pip install .

echo Done
exit 0
