#!/bin/bash

# Function to generate a 1MB random file
generate_test_file() {
    dd if=/dev/urandom of=test_file.bin bs=1M count=1 2>/dev/null
}

# Function to perform AES encryption
encrypt_file() {
    openssl enc -aes-128-cbc -salt -in test_file.bin -out test_file.enc -k password
}

# Function to perform AES decryption (for verification)
decrypt_file() {
    openssl enc -d -aes-128-cbc -in test_file.enc -out test_file.dec -k password
}

# Main profiling function
profile_aes() {
    echo "Generating 1MB test file..."
    generate_test_file

    echo "Performing AES encryption..."
    # Use 'time' command for basic profiling
    TIME_OUTPUT=$(TIMEFORMAT='%R %U %S'; { time encrypt_file; } 2>&1)
    
    # Parse time output
    read REAL USER SYS <<< "$TIME_OUTPUT"
    
    # Get file sizes
    ORIGINAL_SIZE=$(wc -c < test_file.bin)
    ENCRYPTED_SIZE=$(wc -c < test_file.enc)

    echo "Verifying decryption..."
    decrypt_file

    # Check if decryption was successful
    if cmp -s "test_file.bin" "test_file.dec"; then
        DECRYPTION_STATUS="Successful"
    else
        DECRYPTION_STATUS="Failed"
    fi

    # Print results
    echo "-------- AES Encryption Profiling Results --------"
    echo "Original file size: $ORIGINAL_SIZE bytes"
    echo "Encrypted file size: $ENCRYPTED_SIZE bytes"
    echo "Real time: $REAL seconds"
    echo "User time: $USER seconds"
    echo "System time: $SYS seconds"
    echo "Decryption verification: $DECRYPTION_STATUS"
    echo "---------------------------------------------------"

    # Clean up
    rm test_file.bin test_file.enc test_file.dec
}

# Run the profiling
profile_aes