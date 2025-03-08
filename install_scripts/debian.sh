#!/bin/bash
TOOL=$1

case $TOOL in
    "docker")
        sudo apt install -y docker.io ;;
    "terraform")
        sudo apt install -y terraform ;;
    *)
        echo "Tool not supported" ;;
esac
