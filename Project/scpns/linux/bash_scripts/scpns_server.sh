#!/bin/bash

PORT=8080

while true; do
    ncat -l -k -p $PORT -c '
        op=$(dd bs=1 count=1 2>/dev/null)
        if [ "$op" = "0" ]; then
            openssl enc -aes-256-cbc -base64 -k mysecretkey -pbkdf2 2>/dev/null
        elif [ "$op" = "1" ]; then
            openssl enc -d -aes-256-cbc -base64 -k mysecretkey -pbkdf2 2>/dev/null
        else
            echo "Invalid operation" >&2
        fi
        echo "DONE"
    '
done