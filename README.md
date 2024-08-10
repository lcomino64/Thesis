#### Cluster Network Jobs:
- Set up private repository to distribute container images

- Research and add config files, making clients configurable (helm)

- Run multiple containers per pod instead of 1 container per pod
    - Probably make pods be able to run multiple processor clients

- Figure out how to get performance metrics
    - Do completely software-based test (server-image)
    - Then hardware FPGA test

#### SCNP Jobs:
- Download Vivado, use vivado toolchain instead from now on

- Build linux-on-litex to see hopefully if switching to Vivado fixed everything

- Figure out why the json2dts generates extra unfounded node labels??

- Make a dual-core VexRiscV SMP processor with these features:
    - 100MHz sys-clk
    - Ethernet
    - xadc (for reading temps)
    - AES Instruction Plugin 

- Generate Zephyr DTS overlay + config

- Make a single custom LiteX target file with all of this ^^

- Zephyr software:
    - Add multicore utilisation
    - Interface with AES instruction plugin
    - Interface with Ethernet
    - Interface with xadc
    - Create Shell

- Figure out how to get performance metrics
