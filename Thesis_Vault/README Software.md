Board name: litex_vexriscv_smp
Variants: LITEX VEXRISCV SMP, Litex Vexriscv SMP

Zephyr SDK version 0.16.8
Zephyr Repo version 3.7
## Affected Zephyr Files For Adding New Board&SoC (litex_vexriscv_smp)
[[README Board definition files]]
```shell
./dts/bindings/pwm/litex,pwm.yaml
./dts/bindings/mdio/litex,liteeth-mdio.yaml
./dts/bindings/spi/litex,spi.yaml
./dts/bindings/spi/litex,spi-litespi.yaml
./dts/bindings/i2c/litex,i2c.yaml
./dts/bindings/hwinfo/litex,dna0.yaml
./dts/bindings/i2s/litex,i2s.yaml
./dts/bindings/interrupt-controller/litex,vexriscv-intc0.yaml
./dts/bindings/serial/litex,uart.yaml
./dts/bindings/cpu/litex,vexriscv-standard.yaml
./dts/bindings/gpio/litex,gpio.yaml
./dts/bindings/riscv/litex,soc-controller.yaml
./dts/bindings/ethernet/litex,liteeth.yaml
./dts/bindings/timer/litex,timer0.yaml
./dts/bindings/clock/litex,clk.yaml
./dts/bindings/clock/litex,clkout.yaml
./dts/bindings/rng/litex,prbs.yaml
./dts/riscv/riscv32-litex-vexriscv.dtsi


./drivers/pwm/Kconfig.litex
./drivers/pwm/pwm_litex.c
./drivers/mdio/mdio_litex_liteeth.c
./drivers/mdio/Kconfig.litex
./drivers/spi/spi_litex.c
./drivers/spi/Kconfig.litex
./drivers/spi/spi_litex_common.h
./drivers/spi/spi_litex_litespi.c
./drivers/entropy/Kconfig.litex
./drivers/entropy/entropy_litex.c
./drivers/i2c/Kconfig.litex
./drivers/i2c/i2c_litex.c
./drivers/hwinfo/hwinfo_litex.c
./drivers/i2s/i2s_litex.c
./drivers/i2s/Kconfig.litex
./drivers/i2s/i2s_litex.h
./drivers/serial/uart_litex.c
./drivers/serial/Kconfig.litex
./drivers/interrupt_controller/intc_vexriscv_litex.c
./drivers/gpio/Kconfig.litex
./drivers/gpio/gpio_litex.c
./drivers/ethernet/eth_litex_liteeth.c
./drivers/ethernet/Kconfig.litex
./drivers/timer/Kconfig.litex
./drivers/timer/litex_timer.c


./boards/enjoydigital/litex_vexriscv
./boards/enjoydigital/litex_vexriscv/litex_vexriscv_defconfig
./boards/enjoydigital/litex_vexriscv/Kconfig.defconfig
./boards/enjoydigital/litex_vexriscv/Kconfig.litex_vexriscv
./boards/enjoydigital/litex_vexriscv/litex_vexriscv.yaml


./boards/enjoydigital/litex_vexriscv/doc
./boards/enjoydigital/litex_vexriscv/doc/img
./boards/enjoydigital/litex_vexriscv/doc/img/litex_vexriscv.jpg
./boards/enjoydigital/litex_vexriscv/doc/img/symbiflow.svg
./boards/enjoydigital/litex_vexriscv/doc/index.rst


./boards/enjoydigital/litex_vexriscv/board.yml
./boards/enjoydigital/litex_vexriscv/litex_vexriscv.dts


./include/zephyr/drivers/clock_control/clock_control_litex.h


./soc/litex
./soc/litex/litex_vexriscv
./soc/litex/litex_vexriscv/CMakeLists.txt
./soc/litex/litex_vexriscv/Kconfig
./soc/litex/litex_vexriscv/Kconfig.soc
./soc/litex/litex_vexriscv/soc.yml
./soc/litex/litex_vexriscv/Kconfig.defconfig
./soc/litex/litex_vexriscv/soc.h
./soc/litex/litex_vexriscv/reboot.c


./tests/drivers/i2s/i2s_speed/boards/litex_vexriscv.overlay
./tests/drivers/i2s/i2s_api/boards/litex_vexriscv.overlay
```

#### May need attention:
boards/enjoydigital/litex_vexriscv_smp/Kconfig.litex_vexriscv_smp
	`This is presumably where riscv instruction set can be chosen. May need to be explicitly chosen since we have additional riscv instructions`

boards/enjoydigital/litex_vexriscv_smp/litex_vexriscv_smp_defconfig
	`This is where multicore attributes get configured`

boards/enjoydigital/litex_vexriscv_smp/litex_vexriscv_smp.dts
	`This is where device's hardware structure gets defined`

soc/litex/litex_vexriscv_smp/soc.h
	`There's some weird extra code here around line 13`

dts/riscv/riscv32-litex-vexriscv.dtsi
	`Slightly different interrupt controller, intc0`

#### Mem_list
First number is location, second is size
```shell
Available memory regions:
OPENSBI    0x40f00000 0x80000 
PLIC       0xf0c00000 0x400000
CLINT      0xf0010000 0x10000 
ROM        0x00000000 0x10000 
SRAM       0x10000000 0x4000 
MAIN_RAM   0x40000000 0x10000000
ETHMAC     0x80000000 0x2000 
ETHMAC_RX  0x80000000 0x1000 
ETHMAC_TX  0x80001000 0x1000 
CSR        0xf0000000 0x10000  
```

## New Zephyr Board Creation Instructions