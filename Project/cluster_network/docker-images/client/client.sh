#!/bin/bash

SERVER_HOST=server-service
SERVER_PORT=8080

while true; do
    if [[ "$MESSAGING_ENABLED" == "true" ]]; then
        MESSAGE="${MESSAGE:-Default message}"

        if [[ "$ENCRYPTION_ENABLED" == "true" ]]; then
            ENCRYPTED_MESSAGE=$(echo "$MESSAGE" | openssl enc -aes-128-cbc -a -salt -pbkdf2 -pass pass:secretpassword)
            echo "$ENCRYPTED_MESSAGE" | ncat --send-only $SERVER_HOST $SERVER_PORT
        else
            echo "$MESSAGE" | ncat --send-only $SERVER_HOST $SERVER_PORT
        fi
    fi

    sleep "${MESSAGE_FREQUENCY:-1}"
done
