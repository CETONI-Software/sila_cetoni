#!/bin/bash
#
# Wrapper script for sila_qmix.py script
# It sets the PATH, PYTHONPATH and LD_LIBRARY_PATH environment variables so that
# python and ctypes find the necessary files and shared libraries of QmixSDK.
#
# Parameters to this script are passed right on to the sila_qmix.py script
#
#set -x

# change this path to point to your QmixSDK installation
export QMIXSDK_PATH="$HOME/QmixSDK_Linux"

export PATH="$QMIXSDK_PATH":"$PATH"
export PYTHONPATH="$QMIXSDK_PATH/python":"$PYTHONPATH"
export LD_LIBRARY_PATH="$QMIXSDK_PATH/lib":"$LD_LIBRARY_PATH"

curr_dir=$(pwd)
python3 sila_qmix.py $@
cd $curr_dir
