#!/bin/bash
TOOL=$1

case $TOOL in
    "docker")
        sudo apt-get update && sudo apt-get install -y docker.io ;;
    "terraform")
        sudo apt-get install -y terraform ;;
    *)
        echo "AutoDev: Tool not recognized." ;;
esac
