#!/bin/bash
#
# Wrapper script for sila_cetoni.py script
# It sets the PATH, PYTHONPATH and LD_LIBRARY_PATH environment variables so that
# python and ctypes find the necessary files and shared libraries of CETONI SDK.
#
# Parameters to this script are passed right on to the sila_cetoni.py script
#
# By default this script creates a log file for each run in the sila_cetoni/log/
# directory. To prevent this (e.g. because logging to the systemd-journal is
# sufficient) you can set the SILA_CETONI_NO_LOG_FILE environment variable to a
# non-zero value.
#
#set -x

sleep 1 # prevent sporadically not working 2nd pump

# change this path to point to your CETONI SDK installation
grep -qi raspbian /etc/os-release 2>/dev/null && {
    # default directory for RaspberryPi
    export CETONI_SDK_PATH="$HOME/QmixSDK_Raspi"
} || {
    # default directory for generic Linux
    export CETONI_SDK_PATH="$HOME/CETONI_SDK_Linux"
}

export PATH="$CETONI_SDK_PATH":"$PATH"
export PYTHONPATH="$CETONI_SDK_PATH/python":"$PYTHONPATH"
export LD_LIBRARY_PATH="$CETONI_SDK_PATH/lib":"$LD_LIBRARY_PATH"

curr_dir=${0%/*}

DISABLE_LOG=${SILA_CETONI_NO_LOG_FILE:-0}
if [ "$DISABLE_LOG" = 0 ]; then
    # use runtime dir if available which is mounted as tmpfs to save some writes to the SD card
    ${RUNTIME_DIRECTORY:=$XDG_RUNTIME_DIR} 2>/dev/null # RUNTIME_DIRECTORY might come from systemd
    LOG_DIR="${RUNTIME_DIRECTORY:-$curr_dir}/log"
    LOG_FILE="$LOG_DIR/sila_cetoni-`date +%Y-%m-%d.%H:%M:%S`.log"
    mkdir -p $LOG_DIR
    # Redirect stdout into a named pipe
    exec > >( tee -i "$LOG_FILE" )
    # Also redirect stderr
    exec 2>&1
fi

python3 $curr_dir/sila_cetoni.py $@
cd $curr_dir

# write log to SD card if it's in RUNTIME_DIRECTORY
[ "$LOG_DIR" = "$RUNTIME_DIRECTORY/log" ] && cp "$LOG_FILE" "$curr_dir/log/${LOG_FILE##*/}"
