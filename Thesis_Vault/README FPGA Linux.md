## Build Linux images
```shell
git clone http://github.com/buildroot/buildroot
cd buildroot
make BR2_EXTERNAL=../linux-on-litex-vexriscv/buildroot/ litex_vexriscv_defconfig
make
```
## Generate OpenSBI Binary
```shell
git clone https://github.com/litex-hub/opensbi --branch 1.3.1-linux-on-litex-vexriscv
cd opensbi
make CROSS_COMPILE=riscv-none-embed- PLATFORM=litex/vexriscv
```
## Load Images
Serial
```shell
litex_term --images=/home/lachlancomino/repos/linux-on-litex-vexriscv/images/boot.json /dev/ttyUSB1
```

## Test Openssl
```shell

```
OpenSSL Results:
100MHz w/out AES Instructions:
```

```

100MHz w/ AES Instructions:
```

```

But the enc speed test only tests the algorithm. It does not include general I/O or filesaving. Here are more realistic results using `time openssl enc -aes-128-cbc -in $filename -out ${filename}.enc -k password; } 2>&1`
```shell
type        1 MB     2 MB     4 MB     8 MB     16 MB 
aes-128-cbc 4194.30k 3815.09k 4812.80k 5458.92k 5185.64k
```

## iPerf3 results


## Build statistics

## Boot Times
Image size: 8.5mb
FS size: 32.8mb
openSBI: 263.7kB

SD card: 
Ethernet: 16.06s
Serial @ 115200: 43:38s