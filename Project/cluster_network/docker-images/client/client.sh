#!/bin/bash

SERVER_HOST=server-service
SERVER_PORT=8080

while true; do
    MESSAGE="With PID: $$"

    ENCRYPTED_MESSAGE=$(echo "$MESSAGE" | openssl enc -aes-128-cbc -a -salt -pbkdf2 -pass pass:secretpassword)

    echo "$ENCRYPTED_MESSAGE" | ncat --send-only $SERVER_HOST $SERVER_PORT

    sleep 1 
done
