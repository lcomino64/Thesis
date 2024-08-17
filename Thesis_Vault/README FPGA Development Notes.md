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
python3 ~/repos/litex/litex/tools/litex_json2dts_zephyr.py --dts overlay.dts --config overlay.config csr.json
```

TODO: figure out why the overlay.dts hallucinates undefined node labels.

## Booting a Zephyr Application

First, build the zephyr application for litex_vexriscv: 
```shell
west build -p always -b litex_vexriscv path/to/a/zephyr/project -DDTC_OVERLAY_FILE=path/to/overlay.dts
```

Then boot from serial port:
```shell
litex_term /dev/ttyUSBX --speed 115200 --kernel path/to/zephyr.bin
```

## Latest FPGA build command
```shell
./make.py --board=arty_a7 --toolchain=vivado --cpu-count=2 --aes-instruction=True --build
```
## CPU build command
```shell
cd /home/lachlancomino/repos/pythondata-cpu-vexriscv-smp/pythondata_cpu_vexriscv_smp/verilog/ext/VexRiscv && sbt "runMain vexriscv.demo.smp.VexRiscvLitexSmpClusterCmdGen --cpu-count=2 --reset-vector=0 --ibus-width=32 --dbus-width=32 --dcache-size=4096 --icache-size=4096 --dcache-ways=1 --icache-ways=1 --litedram-width=128 --aes-instruction=True --expose-time=False --out-of-order-decoder=True --privileged-debug=False --hardware-breakpoints=0 --wishbone-memory=False --fpu=False --cpu-per-fpu=4 --rvc=False --netlist-name=VexRiscvLitexSmpCluster_Cc2_Iw32Is4096Iy1_Dw32Ds4096Dy1_ITs4DTs4_Ldw128_Aes_Ood --netlist-directory=/home/lachlancomino/repos/pythondata-cpu-vexriscv-smp/pythondata_cpu_vexriscv_smp/verilog --dtlb-size=4 --itlb-size=4 --jtag-tap=False"
```