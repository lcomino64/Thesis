The gap between theoretical 100Mbits/s and achieved 22Mbits/s can be attributed to several factors:
1. Software Stack Overhead:

- Linux networking stack adds significant processing overhead
- IPerf3 itself has overhead for measurement and reporting
- TCP/IP protocol overhead (headers, acknowledgments, etc.)

2. Hardware Limitations:

- 150MHz is still only 1/3 of the maximum theoretical clock rate
- Single shared memory bus becomes a bottleneck
- DMA (Direct Memory Access) not implemented for ethernet transfers
- CPU must handle all packet processing

3. Buffer Size Impact:

- Even with 32KB buffers, still requires frequent CPU intervention
- Not using jumbo frames (larger MTU sizes)

The 100Mbits/s rating is the PHY's raw physical layer capability. To achieve anywhere near this in practice would require:

- Higher clock rates (closer to 450MHz)
- DMA implementation
- Zero-copy networking optimizations
- Reduced protocol overhead (using raw frames instead of TCP/IP)
- Dedicated hardware for packet processing
  
Due to the inherent timing constraints of FPGA fabric (routing delays, logic propagation), RISC-V softcores typically can't exceed ~250MHz reliably. This creates a fundamental performance ceiling for single-interface designs. There are a few potential approaches to scale beyond this:

1. Multiple Ethernet Interfaces:

- Advantages:
    - Linear throughput scaling with interface count
    - Each interface could have dedicated DMA/buffers
    - Natural parallelisation across cores
- Challenges:
    - Complex memory architecture needed (multi-port RAM or multiple RAM banks)
    - Sophisticated DMA controller for multiple channels
    - More complex routing/switching logic in software
    - Significant FPGA resource overhead

2. Hybrid Approach:

- Dedicated hardware acceleration for network processing
- Custom network offload engines
- Keep CPU focused on higher-level operations
- Similar to how modern NICs work

3. Hard IP Integration:

- Use FPGA's built-in hard MAC/PHY if available
- Some newer FPGAs have integrated multi-gigabit transceivers
- Reduces reliance on softcore performance