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
openFPGALoader -b arty_a7_35t build/vexriscv/arty_35/gateware/digilent_arty.bit
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