#!/usr/bin/env bash

pid_path="/run/user/$UID/${1}.toggle.pid"
if [ -f ${pid_path} ]; then
    echo "kill $(cat ${pid_path})"
    kill "$(cat ${pid_path})"
    rm ${pid_path}
else
    nohup ${1} >/dev/null 2>&1 &
    pid=$!
    echo ${pid} > ${pid_path}
    echo create ${pid_path}
fi
