#### Cluster Network Jobs:
- Set up private repository to distribute container images

- Research and add config files, making clients configurable (helm)

- Run multiple containers per pod instead of 1 container per pod
    - Probably make pods be able to run multiple processor clients

- Figure out how to get performance metrics
    - Do completely software-based test (server-image)
    - Then hardware FPGA test

#### SCNP Jobs:
- Still need to figure out how to "add" my board to zephyr
	- include reboot.c in soc
	- fix Kconfig warnings

- Zephyr software:
    - Add multicore utilisation
    - Interface with AES instruction plugin
    - Interface with Ethernet
    - Create Shell

- Figure out how to load gateware+software permanently

- Figure out how to get performance metrics

- 4 core Vexriscv SMP

- Rest of peripherals
	- gpio
	- leds
	- rbg leds
	- buttons
	- switches
