#!/bin/bash

TEST_DIR_PATH="."
TEST_DIR="test_files"
SERVER="localhost"
PORT=8080

send_file() {
    op=$1
    file=$2
    output_file="${file}_$(if [ "$op" = "0" ]; then echo "encrypted"; else echo "decrypted"; fi).txt"
    
    echo "Processing $file..."
    
    { echo -n "$op"; cat "$file"; } | ncat $SERVER $PORT > "$output_file"
    
    sed -i '/DONE/d' "$output_file"
    
    if [ -s "$output_file" ]; then
        echo "Output saved to $output_file"
        echo "Content of output file:"
        cat "$output_file"
    else
        echo "Error: Output file is empty"
        rm -f "$output_file"
    fi
}

# Usage
send_file 0 "$TEST_DIR_PATH/$TEST_DIR/256b.txt" # Encrypt
# send_file 1 "$TEST_DIR_PATH/$TEST_DIR/256b.txt_encrypted.txt" # Decrypt