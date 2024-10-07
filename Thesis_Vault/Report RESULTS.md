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
	time=30s, sample_interval=1s, window_size=8k, streams=1, reverse=true (server sends, client receives)
- Stress-ng, for processing power
`stress-ng --cpu 4 --io 2 --vm 1 --vm-bytes 128M --timeout 60s --metrics-brief`
# OpenSSL Benchmarks
Via:
```shell
openssl speed -elapsed -evp aes-128-cbc aes-256-cbc
```
100MHz w/out AES Instructions:
```
root@buildroot:~# openssl speed -elapsed -evp aes-128-cbc
You have chosen to measure elapsed time instead of user CPU time.
Doing aes-256 cbc for 3s on 16 size blocks: 163425 aes-256 cbc's in 3.00s
Doing aes-256 cbc for 3s on 64 size blocks: 95105 aes-256 cbc's in 3.01s
Doing aes-256 cbc for 3s on 256 size blocks: 35125 aes-256 cbc's in 3.01s
Doing aes-256 cbc for 3s on 1024 size blocks: 9271 aes-256 cbc's in 3.01s
Doing aes-256 cbc for 3s on 8192 size blocks: 1244 aes-256 cbc's in 3.01s
Doing aes-128-cbc for 3s on 16 size blocks: 115261 aes-128-cbc's in 3.01s
Doing aes-128-cbc for 3s on 64 size blocks: 70326 aes-128-cbc's in 3.01s
Doing aes-128-cbc for 3s on 256 size blocks: 37964 aes-128-cbc's in 3.01s
Doing aes-128-cbc for 3s on 1024 size blocks: 11975 aes-128-cbc's in 3.01s
Doing aes-128-cbc for 3s on 8192 size blocks: 1545 aes-128-cbc's in 3.01s

The 'numbers' are in 1000s of bytes per second processed.
type             16 bytes     64 bytes    256 bytes   1024 bytes   8192 bytes
aes-256-cbc        492.58k      700.22k      796.41k      831.49k      830.09k
aes-128-cbc        569.82k      879.49k     1035.23k     1096.36k     1091.36k
```
100MHz w/ AES Instructions:
```
root@buildroot:~# openssl speed -elapsed -evp aes-128-cbc aes-256-cbc
You have chosen to measure elapsed time instead of user CPU time.
Doing aes-256 cbc for 3s on 16 size blocks: 200027 aes-256 cbc's in 3.00s
Doing aes-256 cbc for 3s on 64 size blocks: 105349 aes-256 cbc's in 3.01s
Doing aes-256 cbc for 3s on 256 size blocks: 36417 aes-256 cbc's in 3.01s
Doing aes-256 cbc for 3s on 1024 size blocks: 9297 aes-256 cbc's in 3.01s
Doing aes-256 cbc for 3s on 8192 size blocks: 1245 aes-256 cbc's in 3.01s
Doing aes-128-cbc for 3s on 16 size blocks: 141145 aes-128-cbc's in 3.01s
Doing aes-128-cbc for 3s on 64 size blocks: 73749 aes-128-cbc's in 3.01s
Doing aes-128-cbc for 3s on 256 size blocks: 40348 aes-128-cbc's in 3.01s
Doing aes-128-cbc for 3s on 1024 size blocks: 12176 aes-128-cbc's in 3.01s
Doing aes-128-cbc for 3s on 8192 size blocks: 1559 aes-128-cbc's in 3.01s

The 'numbers' are in 1000s of bytes per second processed.
type             16 bytes     64 bytes    256 bytes   1024 bytes   8192 bytes
aes-256 cbc       1065.34k     2242.60k     3100.24k     3165.50k     3391.24k
aes-128-cbc        751.23k     1569.70k     3435.13k     4146.81k     4246.01k
```
1.8GHz Raspberry Pi:
```
user@raspberrypi1:~$ openssl speed -elapsed -evp aes-128-cbc aes-256-cbc
You have chosen to measure elapsed time instead of user CPU time.
Doing aes-256-cbc for 3s on 16 size blocks: 5117073 aes-256-cbc's in 3.00s
Doing aes-256-cbc for 3s on 64 size blocks: 1362362 aes-256-cbc's in 3.00s
Doing aes-256-cbc for 3s on 256 size blocks: 347621 aes-256-cbc's in 3.00s
Doing aes-256-cbc for 3s on 1024 size blocks: 87586 aes-256-cbc's in 3.00s
Doing aes-256-cbc for 3s on 8192 size blocks: 10974 aes-256-cbc's in 3.00s
Doing aes-256-cbc for 3s on 16384 size blocks: 5486 aes-256-cbc's in 3.00s
Doing AES-128-CBC for 3s on 16 size blocks: 6916540 AES-128-CBC's in 3.00s
Doing AES-128-CBC for 3s on 64 size blocks: 1888832 AES-128-CBC's in 3.00s
Doing AES-128-CBC for 3s on 256 size blocks: 485954 AES-128-CBC's in 3.00s
Doing AES-128-CBC for 3s on 1024 size blocks: 122371 AES-128-CBC's in 3.00s
Doing AES-128-CBC for 3s on 8192 size blocks: 15328 AES-128-CBC's in 3.00s
Doing AES-128-CBC for 3s on 16384 size blocks: 7667 AES-128-CBC's in 3.00s

The 'numbers' are in 1000s of bytes per second processed.
type             16 bytes     64 bytes    256 bytes   1024 bytes   8192 bytes  16384 bytes
aes-256-cbc      27291.06k    29063.72k    29663.66k    29896.02k    29966.34k    29960.87k
AES-128-CBC      36888.21k    40295.08k    41468.07k    41769.30k    41855.66k    41872.04k
```

# Entire native setup on MacOS

# Raspberry Pi Server
### Benchmarks:
Iperf3:
```shell
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.00  sec  1.13 GBytes   323 Mbits/sec    0             sender
[  5]   0.00-30.00  sec  1.13 GBytes   323 Mbits/sec                  receiver
```
Stress-ng:
```shell
stress-ng --cpu 4 --io 2 --vm 1 --vm-bytes 128M --timeout 60s --metrics-brief
stress-ng: info:  [4516] setting to a 1 min, 0 secs run per stressor
stress-ng: info:  [4516] dispatching hogs: 4 cpu, 2 io, 1 vm
stress-ng: info:  [4521] io: this is a legacy I/O sync stressor, consider using iomix instead
stress-ng: metrc: [4516] stressor       bogo ops real time  usr time  sys time   bogo ops/s     bogo ops/s
stress-ng: metrc: [4516]                           (secs)    (secs)    (secs)   (real time) (usr+sys time)
stress-ng: metrc: [4516] cpu               12483     60.03    146.85      0.03       207.94          84.99
stress-ng: metrc: [4516] io               440066     60.00     10.34     48.56      7334.31        7472.11
stress-ng: metrc: [4516] vm               617668     60.16     27.27      6.78     10266.29       18143.58
```
# Single Core
### Benchmarks:
Iperf3 :
```shell
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.11  sec  31.5 MBytes  8.78 Mbits/sec    0   sender
[  5]   0.00-30.00  sec  31.4 MBytes  8.77 Mbits/sec        receiver
```
Stress-ng:
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
Stress-ng:
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
Stress-ng:
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

# Dual Core Improved
Increased max clock rate, 100MHz -> 150MHz
Changed power input to barrel jack, 5v 900mA -> 12v 2A
Ethernet buffers:
```
ETHMAC     0x80000000 0x2000 
ETHMAC_RX  0x80000000 0x1000 
ETHMAC_TX  0x80001000 0x1000
```
were increased to:
```shell
ETHMAC     0x80000000 0x10000 
ETHMAC_RX  0x80000000 0x8000 
ETHMAC_TX  0x80008000 0x8000
```
This allowed us to use a 32K TCP window size as opposed to 8k, significantly increasing our throughput

openSSL:
```shell
openssl speed -elapsed -evp aes-128-cbc aes-256-cbc
The 'numbers' are in 1000s of bytes per second processed.
type             16 bytes     64 bytes    256 bytes   1024 bytes   8192 bytes
aes-256 cbc       1800.05k     4142.59k     6147.52k     6448.09k     6926.90k
aes-128-cbc       1361.11k     3354.34k     6875.47k     8386.73k     8660.50k
```
iperf3:
```shell
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.03  sec  77.4 MBytes  21.6 Mbits/sec    0             sender
[  5]   0.00-30.00  sec  77.2 MBytes  21.6 Mbits/sec                  receiver
```
stress-ng:
```shell
stress-ng: info:  [94] setting to a 60 second run per stressor
stress-ng: info:  [94] dispatching hogs: 2 cpu, 2 io, 1 vm
stress-ng: info:  [94] successful run completed in 80.73s (1 min, 20.73 secs)
stress-ng: info:  [94] stressor       bogo ops real time  usr time  sys time   bogo ops/s     bogo ops/s
stress-ng: info:  [94]                           (secs)    (secs)    (secs)   (real time) (usr+sys time)
stress-ng: info:  [94] cpu                  12     80.60     87.37      0.01         0.15           0.14
stress-ng: info:  [94] io                60868     59.99      3.65     44.52      1014.65        1263.61
stress-ng: info:  [94] vm                 9552     62.53     13.79     11.66       152.75         375.32
```