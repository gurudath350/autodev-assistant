#!/bin/bash
TOOL=$1

case $TOOL in
    "docker")
        sudo apt install -y docker.io ;;
    "kubectl")
        sudo snap install kubectl --classic ;;
    "terraform")
        sudo apt install -y terraform ;;
    "java")
        sudo apt install -y openjdk-17-jdk ;;
    "nodejs")
        sudo apt install -y nodejs npm ;;
    *)
        echo "Tool not supported" ;;
esac
