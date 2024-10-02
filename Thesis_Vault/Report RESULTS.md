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
- Coremark, for processing power
- stress-ng, tests CPUs, I/O and memory
# Entire native setup on MacOS

# Raspberry Pi Server

# Single Core

# Dual Core

# Quad Core
### Benchmarks:
Iperf3:
```shell

```
Coremark:
```shell
```
### Tests:
Basic 100mb, 1 client:
Max Temp: 66C
