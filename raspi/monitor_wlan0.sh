#!/bin/bash
#
# Helper script to monitor WLAN activity (e.g. signal strength) and write the
# results in a to be processed CSV file
#
#set -x

FILENAME="$HOME/sila_cetoni/log/wlan0-`date +%Y-%m-%d.%H:%M:%S`.csv"

echo "time; rx bitrate; tx bitrate; signal" > $FILENAME

while true; do
    bit_rate=`iw dev wlan0 link | grep bitrate | awk -F: ' BEGIN { ORS=";" } { print $2 } '`
    signal_strength=`iw dev wlan0 link | grep signal | awk -F: ' { print $2 } '`
    time=`date +%Y-%m-%d.%H:%M:%S`
    echo "$time;$bit_rate$signal_strength" >> $FILENAME

    sleep 10
done
