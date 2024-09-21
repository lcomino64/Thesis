Completely describe the layout and each section here.
### Introduction & Motivation
Make it better by using real-world examples of cyber attacks on 
More real-world detail on what cyber-attacks are actually like.
### New Background Sections
ISAs and RISCV. Mention the basics of RISCV compared to x86_64 or ARM. Mention ISA Extentions. In the project, only "I" and "M" are being used.
AES-instruction plugin does and how it works.
More about CPU Architecture and what is unique about Vexriscv.

More can be said about the complete developer environment, since most of it is with open-source tools in a CLI (just a quick section).

Add a section on ISAs, more specifically, RISCV and RISCV ISA extensions

### Additional Literature Review
Get better suite of pre-existing solutions for comparison
### Networking Testbed
Full description of apparatus, photos and diagrams
![[example network overview.png]]
From Matt Giplin's report
Make sure to list raspberrypi specs and describe the OS (debian-slim) & client script that will be executed.
Describe Kubernetes & microk8s
##### Pure Software Approach
Same set up but with the Debian server image performing AES calcs instead of the SCPNS. 
### Initial Hardware Model
#### Specifications
dual-core
100e6 sysclk
Utilisation of FPGA resources will go here
#### Results

#### New Specifications

#### Results

### Conclusion

#### Summarise All Experiments and Results

### Experimentation Metrics and Plots to Make:
- Temperature of FPGA (from XADC)
- Zephyr stats - performance, utilisation of cores, packet flow rate.

Plot these two ^ with a *smooth* increase in input size from idle to average to max loads
- Heat camera photos of SCPNS and heat
- Will need to refer to CSSE4010 for FPGA design evaluation. Sections like these will need to be included:
	- Timing Summary
	- Hardware Utilisation
iPerf3 -  measure ethernet capabilities


## Meeting Notes
SCPNS:
- Reduction of scope from Zephyr RTOS-driven SMP processor to single core bare-metal
- Because its single core, only single clients can be served, first come first serve
- AES instructions work on bare-metal
- Bare-metal uses a UDP stack, so Kubernetes cluster will need to adapt.
- Problems with using external litex libraries - fix by just doing project in BIOS

- Kubernetes cluster - needs work but can send encrypted messages to an IP. Needs a private repo and Helm to make configurable for experimentation.
- Throughout execution, client images will save data on timings to a csv. Python scripts will then plot from these csv's.