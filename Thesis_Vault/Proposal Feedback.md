
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
# Marks and feedback
```
Interesting report. Good implementation and background details were included. It might be good to include a simulation section to the project plan.

---
  
The following includes the mark breakdown for the assessment item:  
  
Topic Definition: **18/20**  
There is no doubt about the intended coverage and contribution of the thesis. Includes a project outline and clear statement of purpose. Substantial evidence of initiative.  
  
Background: **28/30**  
Demonstrated mastery of the material in the topic area. Judicious selection of source material. Most helpful in understanding the rest of the document  
  
Project Plan: **19/25**  
A justified, comprehensive, and feasible list of milestones (with resources and duration) and a mostly complete risk and/or ethics assessment. Evidence of initiative and self-reliance.  
  
Presentation: **24/25**  
Excellent structure, so a pleasure to read. Neat, professional presentation. A correctly formatted bibliography appropriately referenced. No spelling grammar or punctuation errors.

Total 89/100
```

TODO: Include a 'simulation' section in project plan going forth

For thesis report, include:
- condensed, updated literature review
- updated introduction - motivation, aims & objectives & scope