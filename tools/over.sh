#!/usr/bin/env bash

# This script will run single instance of anything passed into arguments
# in order to quick swap it for example you can use this
# to run mpv with any mp3 then re-ran it with another file
# it will kill the previous mpv instance and run the new one with new arguments

pid_path="/run/user/$UID/${1}.toggle.pid"

pid=$(cat ${pid_path})

if [ -e ${pid_path} ] && kill -0 ${pid}; then
    kill -9 ${pid}
fi

$@ 2>&1 &
pid=$!
echo ${pid} > ${pid_path}
wait ${pid} && rm ${pid_path}
