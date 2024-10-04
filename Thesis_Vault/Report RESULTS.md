[[Report Planning 2]]
[[Report Planning]]
Configurations to run:
- Raspberry Pi
- Single Core
- Dual Core
- Quad Core

Each configuration will be tested on:
Basic tests:
- 1 client, 100mb file
- 10 clients, varying file sizes from [2,5,10,20]. Total transfer is approx. 65mb
- 20 clients, varying file sizes from [2,5,10,20]. Total transfer is approx. 130mb
Large scale tests:
- 1000 clients, varying varying file sizes from [2,5,10,20]. Total transfer is approx. 650mb

For varying file sizes, the files were chosen randomly from a list, with weights: [0.5, 0.3, 0.2, 0.1], meaning with 10 clients, 2mb will be chosen 5 times, 5mb is 3 times, 10mb is 2 times and 20mb once.

Each configuration also has benchmarks to test the capabilities of each configuration.
These include:
- Iperf3 overall ethernet throughput. 
`iperf3 -c 192.168.1.50 -t 30 -i 1 -w 8K -P 1 -R`
- Coremark, for processing power
`stress-ng --cpu 4 --io 2 --vm 1 --vm-bytes 128M --timeout 60s --metrics-brief`

# Entire native setup on MacOS

# Raspberry Pi Server

# Single Core
### Benchmarks:
Stress-ng:
```shell
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.11  sec  31.5 MBytes  8.78 Mbits/sec    0   sender
[  5]   0.00-30.00  sec  31.4 MBytes  8.77 Mbits/sec        receiver
```
Iperf3:
```shell
stress-ng --cpu 1 --io 2 --vm 1 --vm-bytes 128M --timeout 60s --metrics-brief
stress-ng: info:  [78] setting to a 60 second run per stressor
stress-ng: info:  [78] dispatching hogs: 1 cpu, 2 io, 1 vm
stress-ng: info:  [78] successful run completed in 125.45s (2 mins, 5.45 secs)
stress-ng: info:  [78] stressor       bogo ops real time  usr time  sys time   bogo ops/s     bogo ops/s
stress-ng: info:  [78]                           (secs)    (secs)    (secs)   (real time) (usr+sys time)
stress-ng: info:  [78] cpu                   6    125.34     78.32      0.01         0.05           0.08
stress-ng: info:  [78] io                21794     60.00      2.74     25.71       363.22         766.05
stress-ng: info:  [78] vm                 2280     61.92      7.57      7.60        36.82         150.30
```
# Dual Core
### Benchmarks:
Iperf3:
```shell
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.09  sec  35.5 MBytes  9.90 Mbits/sec    0   sender
[  5]   0.00-30.00  sec  35.4 MBytes  9.89 Mbits/sec        receiver
```
stress-ng:
```shell
stress-ng --cpu 2 --io 2 --vm 1 --vm-bytes 128M --timeout 60s --metrics-brief
stress-ng: info:  [112] setting to a 60 second run per stressor
stress-ng: info:  [112] dispatching hogs: 2 cpu, 2 io, 1 vm
stress-ng: info:  [112] successful run completed in 120.31s (2 mins, 0.31 secs)
stress-ng: info:  [112] stressor       bogo ops real time  usr time  sys time   bogo ops/s     bogo ops/s
stress-ng: info:  [112]                           (secs)    (secs)    (secs)   (real time) (usr+sys time)
stress-ng: info:  [112] cpu                  12    119.09    164.00      0.12         0.10           0.07
stress-ng: info:  [112] io                31190     60.01      3.56     44.44       519.76         649.79
stress-ng: info:  [112] vm                 3053     62.54     10.72     14.93        48.82         119.03
```
# Quad Core
### Benchmarks:
Iperf3:
```shell
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.03  sec  42.0 MBytes  11.7 Mbits/sec    1   sender
[  5]   0.00-30.00  sec  41.9 MBytes  11.7 Mbits/sec        receiver
```
stress-ng:
```shell
stress-ng --cpu 4 --io 2 --vm 1 --vm-bytes 128M --timeout 60s --metrics-brief
stress-ng: info:  [115] setting to a 60 second run per stressor
stress-ng: info:  [115] dispatching hogs: 4 cpu, 2 io, 1 vm
stress-ng: info:  [115] successful run completed in 122.76s (2 mins, 2.76 secs)
stress-ng: info:  [115] stressor       bogo ops real time  usr time  sys time   bogo ops/s     bogo ops/s
stress-ng: info:  [115]                           (secs)    (secs)    (secs)   (real time) (usr+sys time)
stress-ng: info:  [115] cpu                  24    121.30    378.16      0.09         0.20           0.06
stress-ng: info:  [115] io                27819     60.00      3.42     66.44       463.65         398.21
stress-ng: info:  [115] vm                 2464     61.54     18.10     18.32        40.04          67.66
```
### Tests: