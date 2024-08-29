#
# Copyright (c) 2018 - 2019 Antmicro <www.antmicro.com>
#
# SPDX-License-Identifier: Apache-2.0
#

# zephyr_sources(
# 	${ZEPHYR_BASE}/soc/common/riscv-privileged/soc_irq.S
# 	${ZEPHYR_BASE}/soc/common/riscv-privileged/vector.S
# 	${ZEPHYR_BASE}/soc/common/riscv-privileged/soc_common_irq.c
# )

zephyr_include_directories(.)
#zephyr_sources_ifdef(CONFIG_BOARD_LITEX_VEXRISCV_SMP irq.c)

set(SOC_LINKER_SCRIPT ${ZEPHYR_BASE}/include/zephyr/arch/riscv/common/linker.ld CACHE INTERNAL "")
