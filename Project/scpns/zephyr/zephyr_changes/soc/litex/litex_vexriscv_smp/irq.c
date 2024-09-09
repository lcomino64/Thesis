/*
 * Copyright (c) 2017 Jean-Paul Etienne <fractalclone@gmail.com>
 *
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief interrupt management code for riscv SOCs supporting the riscv
	  privileged architecture specification
 */
#include <zephyr/irq_multilevel.h>
#include <zephyr/irq.h>
#include <zephyr/drivers/interrupt_controller/riscv_plic.h>

void arch_irq_enable(unsigned int irq)
{
	uint32_t mie;
	
	/*
	 * CSR mie register is updated using atomic instruction csrrs
	 * (atomic read and set bits in CSR register)
	 */
	__asm__ volatile ("csrrs %0, mie, %1\n"
			  : "=r" (mie)
			  : "r" (1 << irq));    
	riscv_plic_irq_enable(irq);
}

int arch_irq_is_enabled(unsigned int irq)
{
	uint32_t mie;

#if defined(CONFIG_RISCV_HAS_PLIC)
	unsigned int level = irq_get_level(irq);

	if (level == 2) {
		irq = irq_from_level_2(irq);
		return riscv_plic_irq_is_enabled(irq);
	}
#endif

	mie = csr_read(mie);
	return !!(mie & (1 << irq));
}

void arch_irq_disable(unsigned int irq)
{
	uint32_t mie;

#if defined(CONFIG_RISCV_HAS_PLIC)
	unsigned int level = irq_get_level(irq);

	if (level == 2) {
		irq = irq_from_level_2(irq);
		riscv_plic_irq_disable(irq);
		return;
	}
#endif

	/*
	 * Use atomic instruction csrrc to disable device interrupt in mie CSR.
	 * (atomic read and clear bits in CSR register)
	 */
	mie = csr_read_clear(mie, 1 << irq);
	riscv_plic_irq_disable(irq);
}

#if defined(CONFIG_RISCV_HAS_PLIC)
void z_riscv_irq_priority_set(unsigned int irq, unsigned int prio, uint32_t flags)
{
	unsigned int level = irq_get_level(irq);
	if (level == 2) {
		// printf("irq = %d, level = %d, prio=%d\n", irq, level, prio);
		irq = irq_from_level_2(irq);
		riscv_plic_set_priority(irq, prio);
		return;
	}
	riscv_plic_set_priority(irq, prio);
}
#endif /* CONFIG_RISCV_HAS_PLIC */