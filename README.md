#### Cluster Network Jobs:
- Set up private repository to distribute container images

- Research and add config files, making clients configurable (helm)

- Run multiple containers per pod instead of 1 container per pod
    - Probably make pods be able to run multiple processor clients

- Figure out how to get performance metrics
    - Do completely software-based test (server-image)
    - Then hardware FPGA test

#### SCNP Jobs:
- Zephyr software:
    - Add multicore utilisation
    - Interface with AES instruction plugin
    - Interface with Ethernet
    - Interface with xadc
    - Create Shell

- Figure out how to load gateware+software into ROM so FPGA doesn't lose everything

- Figure out how to get performance metrics

- REMEMBER BSD-2-Clause license for using linux-on-litex-vexriscv
