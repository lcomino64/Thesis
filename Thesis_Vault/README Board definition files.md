In ./boards/enjoydigital/litex_vexriscv_smp/

board.yml
```c
board:
  name: litex_vexriscv_smp
  vendor: litex
  socs:
  - name: litex_vexriscv_smp
```
Kconfig.defconfig
```c
if BOARD_LITEX_VEXRISCV_SMP 

config BOARD
        default "litex_vexrisc_smp"

if NETWORKING

config NET_L2_ETHERNET
        default y

endif # NETWORKING

config SPI
        default y

config RISCV_HAS_PLIC
        default y

endif # BOARD_LITEX_VEXRISCV_SMP
```
Kconfig.litex_vexriscv_smp
```c
config BOARD_LITEX_VEXRISCV_SMP 
        select SOC_RISCV32_LITEX_SMP
        # select RISCV_ISA_EXT_C
```
litex_vexriscv_smp_defconfig
```c
CONFIG_CONSOLE=y
CONFIG_SERIAL=y
CONFIG_UART_CONSOLE=y
CONFIG_GPIO=y
CONFIG_XIP=n
CONFIG_CLOCK_CONTROL=n
CONFIG_HEAP_MEM_POOL_SIZE=4096
CONFIG_SYS_CLOCK_HW_CYCLES_PER_SEC=100000000   
CONFIG_MP_MAX_NUM_CPUS=2
CONFIG_SMP=y
```
litex_vexriscv_smp.dts
```c
/dts-v1/;

#include<riscv32-litex-vexriscv-smp.dtsi>

/ {
        model = "LiteX VexRiscV SMP";
        compatible = "litex,vexriscv";
        chosen {
                zephyr,console = &uart0;
                zephyr,shell-uart = &uart0;
                zephyr,sram = &ram0;
        };

        ram0: memory@40000000 {
                device_type = "memory";
                reg = <0x40000000 0x10000000>;
        };
};
&ctrl0 {
    reg = <0xf0000000 0x4
        0xf0000004 0x4
        0xf0000008 0x4>;
    reg-names = "reset",
        "scratch",
        "bus_errors";
};
&uart0 {
    reg = <0xf0001000 0x4
        0xf0001004 0x4
        0xf0001008 0x4
        0xf000100c 0x4
        0xf0001010 0x4
        0xf0001014 0x4
        0xf0001018 0x4
        0xf000101c 0x4>;
    reg-names = "rxtx",
        "txfull",
        "rxempty",
        "ev_status",
        "ev_pending",
        "ev_enable",
        "txempty",
        "rxfull";
    interrupts = <0x1 0>;
};
&timer0 {
    reg = <0xf0001800 0x4
        0xf0001804 0x4
        0xf0001808 0x4
        0xf000180c 0x4
        0xf0001810 0x4
        0xf0001814 0x4
        0xf0001818 0x4
        0xf000181c 0x4
        0xf0001820 0x4
        0xf0001824 0x8>;
    reg-names = "load",
        "reload",
        "en",
        "update_value",
        "value",
        "ev_status",
        "ev_pending",
        "ev_enable",
        "uptime_latch",
        "uptime_cycles";
    interrupts = <0x2 0>;
};
&eth0 {
    reg = <0xf0002000 0x4
        0xf0002004 0x4
        0xf0002008 0x4
        0xf000200c 0x4
        0xf0002010 0x4
        0xf0002014 0x4
        0xf0002018 0x4
        0xf000201c 0x4
        0xf0002020 0x4
        0xf0002024 0x4
        0xf0002028 0x4
        0xf000202c 0x4
        0xf0002030 0x4
        0xf0002034 0x4
        0x80000000 0x2000>;
    reg-names = "rx_slot",
        "rx_length",
        "rx_errors",
        "rx_ev_status",
        "rx_ev_pending",
        "rx_ev_enable",
        "tx_start",
        "tx_ready",
        "tx_level",
        "tx_slot",
        "tx_length",
        "tx_ev_status",
        "tx_ev_pending",
        "tx_ev_enable",
        "buffers";
    interrupts = <0x3 0>;
};
&spi0 {
    status = "okay";
};
&i2c0 {
    reg = <0xf0003000 0x4
        0xf0003004 0x4>;
    reg-names = "write",
        "read";
};
&ram0 {
    reg = <0x40000000 0x10000000>;
};
```
litex_vexriscv_smp.yaml
```c
identifier: litex_vexriscv_smp
name: LiteX SoC with VexRiscV SMP dual-core softcore CPU
type: mcu
arch: riscv
toolchain:
  - zephyr
ram: 256000000 
supported:
  - spi
  - i2s
testing:
  ignore_tags:
    - bluetooth
    - xip
vendor: litex
```

In ./dts/riscv/litex_vexriscv_smp.dtsi
```c
/dts-v1/;

/ {
        compatible = "litex,digilent_arty", "litex,soc";
        model = "digilent_arty";
        #address-cells = <1>;
        #size-cells    = <1>;


        chosen {
            bootargs = "console=liteuart earlycon=liteuart,0xf0001000 rootwait root=/dev/ram0 ip=192.168.1.50:192.168.1.100:192.168.1.100:255.255.255.0::eth0:off:::";
            linux,initrd-start = <0x41000000>;
            linux,initrd-end   = <0x41800000>;
        };

        sys_clk: clock-100000000 {
            compatible = "fixed-clock";
            #clock-cells = <0>;
            clock-frequency  = <100000000>;
        };

        cpus {
            #address-cells = <1>;
            #size-cells    = <0>;
            timebase-frequency = <100000000>;

            CPU0: cpu@0 {
                device_type = "cpu";
                compatible = "riscv";
                riscv,isa = "rv32i2p0_ma";
                riscv,isa-base = "rv32i";
                riscv,isa-extensions = "a", "i", "m";
                mmu-type = "riscv,sv32";
                reg = <0>;
                clock-frequency = <100000000>;
                status = "okay";

                d-cache-size = <4096>;
                d-cache-sets = <1>;
                d-cache-block-size = <64>;

                i-cache-size = <4096>;
                i-cache-sets = <1>;
                i-cache-block-size = <64>;


                tlb-split;
                d-tlb-size = <4>;
                d-tlb-sets = <4>;

                i-tlb-size = <4>;
                i-tlb-sets = <4>;


                L0: interrupt-controller {
                    #address-cells = <0>;
                    #interrupt-cells = <0x00000001>;
                    interrupt-controller;
                    compatible = "riscv,cpu-intc";
                };
            };
            
            CPU1: cpu@1 {
                device_type = "cpu";
                compatible = "riscv";
                riscv,isa = "rv32i2p0_ma";
                riscv,isa-base = "rv32i";
                riscv,isa-extensions = "a", "i", "m";
                mmu-type = "riscv,sv32";
                reg = <1>;
                clock-frequency = <100000000>;
                status = "okay";

                d-cache-size = <4096>;
                d-cache-sets = <1>;
                d-cache-block-size = <64>;

                i-cache-size = <4096>;
                i-cache-sets = <1>;
                i-cache-block-size = <64>;


                tlb-split;
                d-tlb-size = <4>;
                d-tlb-sets = <4>;

                i-tlb-size = <4>;
                i-tlb-sets = <4>;


                L1: interrupt-controller {
                    #address-cells = <0>;
                    #interrupt-cells = <0x00000001>;
                    interrupt-controller;
                    compatible = "riscv,cpu-intc";
                };
            };


            cpu-map {
                cluster0 {
                    core0 {
                        cpu = <&CPU0>;
                    };
                    core1 {
                        cpu = <&CPU1>;
                    };
                };
            };
        };

        memory: memory@40000000 {
            device_type = "memory";
            reg = <0x40000000 0x10000000>;
        };

        reserved-memory {
            #address-cells = <1>;
            #size-cells    = <1>;
            ranges;

            opensbi@40f00000 {
                reg = <0x40f00000 0x80000>;
            };
		};

        soc {
            #address-cells = <1>;
            #size-cells    = <1>;
            compatible = "simple-bus";
            interrupt-parent = <&intc0>;
            ranges;

            soc_ctrl0: soc_controller@f0000000 {
                compatible = "litex,soc-controller";
                reg = <0xf0000000 0xc>;
                status = "okay";
            };

            intc0: interrupt-controller@f0c00000 {
                compatible = "sifive,fu540-c000-plic", "sifive,plic-1.0.0";
                reg = <0xf0c00000 0x400000>;
                #address-cells = <0>;
                #interrupt-cells = <2>;
                interrupt-controller;
                interrupts-extended = <
                    &L0 11 &L0 9
                    &L1 11 &L1 9>;
                riscv,ndev = <32>;

            };

            liteuart0: serial@f0001000 {
                compatible = "litex,liteuart";
                reg = <0xf0001000 0x100>;
                interrupts = <1>;
                status = "okay";
            };

            mac0: mac@f0002000 {
                compatible = "litex,liteeth";
                reg = <0xf0002000 0x7c>,
                      <0xf0002800 0x0a>,
                      <0x80000000 0x2000>;
                reg-names = "mac", "mdio", "buffer";
                litex,rx-slots = <2>;
                litex,tx-slots = <2>;
                litex,slot-size = <2048>;
                interrupts = <3>;
                status = "okay";
            };

            litespi0: spi@f0004800 {
                compatible = "litex,litespi";
                reg = <0xf0004800 0x100>;
                status = "okay";

                litespi,max-bpw = <8>;
                litespi,sck-frequency = <1000000>;
                litespi,num-cs = <1>;

                #address-cells = <1>;
                #size-cells    = <0>;

				spidev0: spidev@0 {
                    compatible = "linux,spidev";
                    reg = <0>;
                    spi-max-frequency = <1000000>;
                    status = "okay";
                };
            };

            i2c0: i2c@f0003000 {
                compatible = "litex,i2c";
                reg = <0xf0003000 0x5>;
                #address-cells = <1>;
                #size-cells = <0>;
                status = "okay";
            };

        };

        aliases {

                serial0 = &liteuart0;

                spi0 = &litespi0;

        };

};
```