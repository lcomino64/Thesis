#!/bin/bash
TEST_DIR="test_files"
rm -rf $TEST_DIR
mkdir -p $TEST_DIR

generate_file_with_sha() {
    local file="$1"
    local size="$2"
    dd if=/dev/urandom of="$TEST_DIR/$file" bs=1M count=$size
}

generate_file_with_sha "100mb.txt" 100
generate_file_with_sha "50mb.txt" 50
generate_file_with_sha "10mb.txt" 10
generate_file_with_sha "1gb.txt" 1000