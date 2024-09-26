TEST_DIR_PATH="."
TEST_DIR="test_files"
mkdir $TEST_DIR

# Random Text
dd if=/dev/urandom of=$TEST_DIR_PATH/$TEST_DIR/1gb.txt bs=1M count=1024
dd if=/dev/urandom of=$TEST_DIR_PATH/$TEST_DIR/2mb.txt bs=1M count=2


# Repeating Text
yes "This is a test line." | head -c 512M > $TEST_DIR_PATH/$TEST_DIR/512mb.txt

# Sequential Numbers
seq 1 256 > $TEST_DIR_PATH/$TEST_DIR/256b.txt