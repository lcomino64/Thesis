#!/bin/bash

SERVER_IP="192.168.1.50"
SERVER_PORT="8443"
TEST_SIZES=(64 128 256 512 1024)  # Test sizes in MB

echo "Starting TLS throughput test to ${SERVER_IP}:${SERVER_PORT}"
echo "=================================================="

for size in "${TEST_SIZES[@]}"; do
    echo "Testing ${size}KB transfer..."
    
    # Run test 3 times for average
    for i in {1..3}; do
        echo "Run $i:"
        START=$(date +%s.%N)
        
        dd if=/dev/zero bs=1K count=$size 2>/dev/null | \
        openssl s_client -connect ${SERVER_IP}:${SERVER_PORT} \
        -cipher AES128-GCM-SHA256 2>/dev/null | \
        dd of=/dev/null 2>/dev/null
        
        END=$(date +%s.%N)
        DURATION=$(echo "$END - $START" | bc)
        THROUGHPUT=$(echo "scale=2; $size / $DURATION" | bc)
        
        echo "Duration: ${DURATION}s"
        echo "Throughput: ${THROUGHPUT} KB/s"
        echo "------------------------"
    done
done
