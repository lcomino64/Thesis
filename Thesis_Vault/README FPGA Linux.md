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
openssl speed -elapsed -evp aes-128-cbc aes-256-cbc
```
OpenSSL Results:
100MHz w/out AES Instructions:
```
rroot@buildroot:~# openssl speed -elapsed -evp aes-128-cbc
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
aes-256 cbc        870.81k     2023.99k     2989.93k     3156.62k     3388.60k
aes-128-cbc        613.31k     1496.89k     3231.90k     4078.06k     4206.62k
```

