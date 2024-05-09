
[[Draft Proposal Notes]]

Meeting minutes from 27/03/2024
Discussed proposal.
- Need to add references and literature review
- Use of 'soft core processor' instead of FPGA processor
- Have network testbed section with cluster network instead of microcomputers
- Need to have an OHS table - I'll do this later
~~- Come up with Acryonm - RPNS - RISC-V Processor for Network Security~~
- Specify the use of encryption as a network security application
- Think about how to evaluate it (how to measure performance).
- Add Wishbone Bus section

Queries:
- Shared memory for both SCPNS cores isn't strictly necessary. Maybe just direct comms is better
- Does the design actually need to be multicore? Zephyr RTOS may be able to just handle multitasking everything on a single faster core, however, a multicore design has the advantage of being able to read/write to long-term storage uninterrupted. Think about how a multicore design can be emphasised.
- Multicore has potential but think of ways how to prove it is actually better.
- Show how encryption can be verified. Ensure that the AES SoC is working properly.
- Simulate and model the FPGA architecture.