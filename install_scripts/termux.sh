#!/bin/bash
TOOL=$1

case $TOOL in
    "git")
        pkg install git ;;
    "docker")
        pkg install docker ;;
    "python")
        pkg install python ;;
    *)
        echo "Tool not supported in Termux" ;;
esac
