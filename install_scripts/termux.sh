#!/bin/bash
TOOL=$1

case $TOOL in
    "git")
        pkg install git ;;
    "docker")
        pkg install docker ;;
    *)
        echo "AutoDev: Tool not supported in Termux" ;;
esac
