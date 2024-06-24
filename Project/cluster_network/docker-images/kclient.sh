#!/bin/bash

function set_message_frequency() {
    microk8s kubectl patch configmap client-config -p '{"data":{"MESSAGE_FREQUENCY":"'$1'"}}'
    echo "Message frequency set to $1 seconds."
}

function set_message() {
    microk8s kubectl patch configmap client-config -p '{"data":{"MESSAGE":"'"$1"'"}}'
    echo "Message set to: $1"
}

function toggle_messaging() {
    microk8s kubectl patch configmap client-config -p '{"data":{"MESSAGING_ENABLED":"'$1'"}}'
    echo "Messaging $1."
}

function toggle_encryption() {
    microk8s kubectl patch configmap client-config -p '{"data":{"ENCRYPTION_ENABLED":"'$1'"}}'
    echo "Encryption $1."
}

function scale_replicas() {
    replicas=$1
    kubectl scale deployment client --replicas=$replicas
    echo "Scaled client deployment to $replicas replicas."
}

function display_help() {
    echo "Usage: kclient [options]"
    echo
    echo "Options:"
    echo "  -f <seconds>  Set the message frequency (in seconds)"
    echo "  -m <text>     Set the message to send"
    echo "  -s <on|off>   Toggle messaging on or off"
    echo "  -e <on|off>   Toggle encryption on or off"
    echo "  -r <number>   Scale the number of client replicas"
    echo "  -h            Display this help message"
}

while getopts ":f:m:s:e:r:h" opt; do
    case $opt in
        f) set_message_frequency "$OPTARG" ;;
        m) set_message "$OPTARG" ;;
        s) toggle_messaging "$OPTARG" ;;
        e) toggle_encryption "$OPTARG" ;;
        r) scale_replicas "$OPTARG" ;;
        h) display_help; exit ;;
        \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
        :) echo "Option -$OPTARG requires an argument." >&2; exit 1 ;;
    esac
done

if [ $OPTIND -eq 1 ]; then
    echo "No options provided."
    display_help
    exit 1
fi


