#!/bin/bash

SERVER="localhost"
PORT=8080

encrypt_file() {
    local file=$1
    echo -n "0$(cat "$file")" | nc $SERVER $PORT
}

decrypt_file() {
    local file=$1
    echo -n "1$(cat "$file")" | nc $SERVER $PORT
}

# Test encryption
echo "Testing encryption:"
echo "Hello, World!" > plaintext.txt
encrypt_file plaintext.txt > encrypted.txt
cat encrypted.txt

# Test decryption
echo -e "\nTesting decryption:"
decrypt_file encrypted.txt

# Clean up
# rm plaintext.txt encrypted.txt
