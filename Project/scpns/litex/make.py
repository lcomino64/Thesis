#!/usr/bin/env python3

import os

from litex.soc.integration.builder import Builder

from soc_linux import SoCLinux
from litex.soc.cores.cpu.vexriscv_smp import VexRiscvSMP

class Board:
    soc_kwargs = {
        "integrated_rom_size"  : 0x10000,
        "integrated_sram_size" : 0x4000,
        "l2_size"              : 0
    }
    def __init__(self, soc_cls=None, soc_capabilities={}, soc_constants={}):
        self.soc_cls          = soc_cls
        self.soc_capabilities = soc_capabilities
        self.soc_constants    = soc_constants

# Board Definition -------------------------------------
class ArtyA7(Board):
    soc_capabilities = {
        # Communication
        "serial",
        "ethernet",
        # Storage
        "spiflash",
        # GPIOs
        "leds",
        "rgb_led",
        "switches",
        # Buses
        "spi",
        "i2c",
        # Monitoring
        "xadc",
        # 7-Series specific  
        "mmcm",
    }
    soc_kwargs = {
        "variant": "a7-35", 
        "sys_clk_freq": int(100e6), 
        "with_ethernet" : True,
        "with_led_chaser" : False,
        "with_spi_flash" : False,
        "with_spi_sdcard" : False,
        "with_sdcard" : False,
        "timer_uptime" : True,
    }

    def __init__(self):
        from litex_boards.targets import digilent_arty
        Board.__init__(self, digilent_arty.BaseSoC)

# Build configuration constants ------------------------
UART_BAUDRATE  = 115200
TOOLCHAIN      = "vivado"
CPU_COUNT      = 2
AES_INSTRUCTION = False

# Peripheral configuration -----------------------------
SPI_DATA_WIDTH = 8
SPI_CLK_FREQ   = 1e6 

def main():
    board = ArtyA7()
    soc_kwargs = Board.soc_kwargs
    soc_kwargs.update(board.soc_kwargs)
    soc_kwargs.update(l2_size=8192)

    # CPU parameters  
    VexRiscvSMP.cpu_count = CPU_COUNT
    VexRiscvSMP.aes_instruction = AES_INSTRUCTION

    # SoC creation
    soc = SoCLinux(board.soc_cls, **soc_kwargs)
    board.platform = soc.platform

    # SoC peripherals
    # soc.add_mmcm(2)
    # soc.add_rgb_led()
    # soc.add_switches()
    soc.add_spi(SPI_DATA_WIDTH, SPI_CLK_FREQ)
    soc.add_i2c()
    # soc.add_xadc()

    soc.configure_ethernet(remote_ip="192.168.1.100")

    # Build
    builder = Builder(soc, 
        output_dir = os.path.join("build", "arty_a7"),
        csr_json   = os.path.join("build", "arty_a7", "csr.json"),
        csr_csv    = os.path.join("build", "arty_a7", "csr.csv")
    )  
    builder.build(build_name="arty_a7")

    soc.generate_dts("arty_a7")
    soc.compile_dts("arty_a7")

    # DTB --------------------------------------------------------------------------------------
    # soc.combine_dtb("arty_a7")

    # Generate SoC documentation
    # soc.generate_doc("arty_a7")


if __name__ == "__main__":
    main()
