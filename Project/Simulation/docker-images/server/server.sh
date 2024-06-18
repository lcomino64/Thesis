#!/bin/bash

SERVER_PORT=8080

decrypt_message() {
    message=$1
    decrypted_message=$(echo "$message" | openssl enc -d -aes-128-cbc -a -pbkdf2 -pass pass:secretpassword 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "Decrypted message: $decrypted_message"
    else
        echo "Failed to decrypt message: $message"
    fi
}

echo "Server is listening on port $SERVER_PORT..."

while true; do
    if read -t 1 message; then
        decrypt_message "$message" &
    fi
done < <(ncat -lkp $SERVER_PORT)
