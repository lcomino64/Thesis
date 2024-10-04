CORE_COUNT=$1
echo "Running benchmarks for core_count=$CORE_COUNT"

coremark 0x0 $CORE_COUNT 0 0 > coremark_results.txt
iperf3 -s
# In another terminal, run:
# iperf3 -c 192.168.1.50