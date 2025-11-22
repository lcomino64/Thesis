## Building Litex SoC for Arty
Build for arty-s7 35T using F4PGA toolchain. Make sure you are in conda environment:
```shell
conda activate xc7
```

Now build a Vexriscv processor for the arty s7
```shell
python3 ~/repos/litex-boards/litex_boards/targets/digilent_arty.py --toolchain=f4pga --cpu-type=vexriscv --sys-clk-freq 100e6 --output-dir build/vexriscv/arty_35 --variant a7-35 --build --timer-uptime --csr-json csr.json
```

Send bitstream to FPGA
```shell
openFPGALoader -b arty_a7_35t build/arty_a7/gateware/arty_a7.bit
```

Screen Litex (using picocom):
```shell
picocom -b 115200 /dev/ttyUSB1 --imap lfcrlf
```

Build overlay config and dts for zephyr to use:
```shell
python3 ~/repos/litex/litex/tools/litex_json2dts_zephyr.py --dts litex_vexriscv_smp.dts --config overlay.config csr.json
```

## Booting a Zephyr Application

First, build the zephyr application for litex_vexriscv: 
```shell
west build -p always -b litex_vexriscv path/to/a/zephyr/project -DDTC_OVERLAY_FILE=~/Thesis/Project/scpns/litex/build/arty_a7/arty_a7.dts
```

Then boot from serial port:
```shell
litex_term /dev/ttyUSB1 --speed 115200 --kernel ~/zephyrproject/zephyr/build/zephyr/zephyr.bin
```

## Latest FPGA build command
```shell
./make.py --board=arty_a7 --toolchain=vivado --cpu-count=2 --aes-instruction=True --build
```
## CPU build command
```shell
cd /home/lachlancomino/repos/pythondata-cpu-vexriscv-smp/pythondata_cpu_vexriscv_smp/verilog/ext/VexRiscv && sbt "runMain vexriscv.demo.smp.VexRiscvLitexSmpClusterCmdGen --cpu-count=2 --reset-vector=0 --ibus-width=32 --dbus-width=32 --dcache-size=4096 --icache-size=4096 --dcache-ways=1 --icache-ways=1 --litedram-width=128 --aes-instruction=True --expose-time=True --out-of-order-decoder=True --privileged-debug=False --hardware-breakpoints=0 --wishbone-memory=True --fpu=False --cpu-per-fpu=4 --rvc=True --netlist-name=VexRiscvLitexSmpCluster_Cc2_Iw32Is4096Iy1_Dw32Ds4096Dy1_ITs4DTs4_Ldw128_Aes_Ood --netlist-directory=/home/lachlancomino/repos/pythondata-cpu-vexriscv-smp/pythondata_cpu_vexriscv_smp/verilog --dtlb-size=4 --itlb-size=4 --jtag-tap=False"
```
## Debugging in Litex Sim
Run litex_sim (Terminal 1)
```shell
litex_sim --cpu-type=vexriscv_smp --cpu-count=1 --with-sdram --sdram-init ~/zephyrproject/zephyr/build/zephyr/zephyr.bin --trace --trace-fst --with-rvc --with-privileged-debug --hardware-breakpoints 4 --jtag-tap --with-jtagremote
```
Run OpenOCD (Terminal 2)
```shell
openocd -f jtag_remote.cfg -f riscv_jtag_tunneled.tcl 
```
Open gdb-multiarch with zephyr.elf
```shell
gdb-multiarch ~/zephyrproject/zephyr/build/zephyr/zephyr.elf
```
Now open gdb port on openocd with gdb-multiarch (in gdb)
```shell
target extended-remote localhost:3333
```
## Debugging onboard with JTAG USB
Make sure LiteX SoC is built with hardware-breakpoints=4 and with-privileged-debug=True
```shell
openocd -f ~/Thesis/Project/scpns/litex/debug/digilent_arty.cfg -c "set TAP_NAME xc7.tap" -f ~/Thesis/Project/scpns/litex/debug/riscv_jtag_tunneled.tcl
```
Connecting GDB
```shell
gdb-multiarch -q ~/zephyrproject/zephyr/build/zephyr/zephyr.elf -ex "target extended-remote localhost:3333"
```

## General Debugging
Thread analyser stuff (add to end of west build):
```shell
-DCONFIG_THREAD_ANALYZER=y \
-DCONFIG_THREAD_ANALYZER_USE_PRINTK=y -DCONFIG_THREAD_ANALYZER_AUTO=y \
-DCONFIG_THREAD_ANALYZER_AUTO_INTERVAL=5
```
Logging
```shell
-DCONFIG_LOG=y -DCONFIG_LOG_PRINTK=y 
```
Led
```c
void led_ping(unsigned int conf) {
	volatile unsigned int *led = (unsigned int *)0xf0002000;
	*led += conf;
}
led_ping(0b0001);
```
## Seeing ports and killing them
See ports being used
```shell
sudo lsof -i -P -n | grep LISTEN
```
Kill process using port
```shell
kill -9 $(lsof -ti tcp:port)
```

## Booting ethernet
Start TFTP Server
```shell
sudo systemctl restart tftpd-hpa
```
Check status
```shell
sudo systemctl status tftpd-hpa
```
Get file from tftp server
```
tftp -g -r server.py 192.168.1.100
tftp -g -r run_benchmarks.sh 192.168.1.100
```
Remember to configure ethernet on the board's startup:
```shell
ifconfig eth0 192.168.1.50
```