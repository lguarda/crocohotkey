#!/usr/bin/env bash

# This script can kill instance of already running script launched by ./over.sh

pid_path="/run/user/$UID/${1}.toggle.pid"

pid=$(cat ${pid_path})

if [ -e ${pid_path} ] && kill -0 ${pid}; then
    kill -9 ${pid}
fi
