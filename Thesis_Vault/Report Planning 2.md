# Prologue ---------------------------------------
Title page
Letter to Dean
Acknowledgements
Abstract
List of Abbreviations
Contents
List of Figures & Tables

# Part I -Introduction---------------------------------
# Introduction
## Motivation
Same as before, except:
- When mentioning IoT security, mention the 2024 story about the Dyn attack
- Overview of RISC-V, it's current state in the market.
## Project Overview and Scope

# Part 2 -Research------------------------------------
# Background
## Computer Networks, TCP/IP
#### Network Layer
#### Link Layer and Ethernet PHY
#### Ethernet Interfaces
## Network Security Methods for Embedded Systems
#### AES Encryption
## RISC-V Architecture
ISA structure compared to other ISAs

![[Pasted image 20241027173506.png]]
ISA Extensions
ISA modes: User, Supervisor, machine etc.
## FPGAs and Softcore CPUs
What are FPGAs and what are softcore CPUs? What is the current fastest softcore CPU?
#### VexRiscv & SpinalHDL
#### CPU Buses and Wishbone
#### VexRiscvSMP Linux
Si-Five PLIC/CLINT. How do cores synchronise?
## LiteX Overview
#### Cores, Liteeth
#### Litex BIOS
## Operating Systems
#### Buildroot Linux

# Part 3 -Complete Stack Overview-------------------
## Hardware Setup
#### FPGA Board: Digilent Arty A7-35T
#### Custom AES Instructions
OpenSSL Benchmarks (Put full output in the Appendix)
Diagram of RTL
Explanation of how it works and how the CPU "uses" it
Instruction count with custom instructions vs without
Discuss total footprint (FPGA utilisation) of custom instructions
#### Proof of Encryption
[[Report Proof of Encryption Section]]
Methodology:
Show that the device is actually encryption/decryption capable
1. Create test text file.
2. Take sha256sum of test file.
3. Encrypt the test file via the board.
4. Check that test file is encrypted.
5. Decrypt the file via the board.
6. Check if sha256sum is the same. 
#### Raspberry Pi
Specs of the Pi, but especially mention the gigabit ethernet
#### Network Overview
## Software Setup
Different Boot methods time taken chart
#### Buildroot Linux Configuration
Show linux compilation graphs
## Developer Setup


# Part 4-Evaluation-----------------------------------
## Raw Performance Benchmarks & Theoretical Results

## Results & Analysis

## Utilisation, Resources and Timing

## Improved Dual Core
## Power Analysis*


# Part 5-Conclusion----------------------------------
## Summary

## Limitations & Security Vulnerabilities

## Future Improvements
Different boards for more ethernet throughput and extra RAM dimensions/Ethernet Ports
Use a board with hardcore CPUs attached, i.e. Zynq for ARM, PolarFire for RISC-V
## Issues and Reductions in Scope During Development
Zephyr not working
Socat not working in buildroot linux, "File Descriptor error", had to use python instead
Not enough RPi RAM for containers running python, therefore, python was just run natively.

# Tests to Run
### Pi Cluster Full Kubernetes & SCPNS: 1 core, 2 core, 4 core
For each of these do:
Collect server metrics every 1 second: "timestamp, cpu_usage, memory_usage, active_clients, total_bytes_processed, bytes_processed_per_second"
- After a session, we can infer: max clients handled at once, max cpu/mem_usage, total_bytes_processed and average bytes_per_second

Collect client metrics at the end of each file sent: "file_size, operation, start_time, end_time, total_time, queue_time, network_time, processing_time, total_bytes_sent, total_received, operation_completed?"
- After a number of clients have been processed, the following can be inferred: average network/processing/queue time, number of successful operations/failures.


Basic tests - 1 client, 10 clients, 50 clients - This one can all be made into single table.
Where there are multiple clients, we will pick a random file size from 10mb to 100mb

1000 clients - how fast can each handle a 1000 client count with different file sizes?
File sizes should vary from 1 to 100mb. 

Clients spawn at a drowning rate for 60mins - how many clients can be handled in 60min?

#### In Appendix, MacOS virtual stats will be added to the appendix (Virtual doesn't have to contend with network latency)

Challenges:
- Storage may be a concern for the files of many clients. We may need to just throw out the result of an encryption/decryption, if the file already exists. That way all client threads on the same pod, can reference the same file. 

# Demo Sections of priority:
## Introduction
## RISC-V Overview
## AES sections
Be able to explain how AES encryption works. 
"Where" do the AES instructions exist on the board?
Get an RTL schematic of the added instructions

## LiteX and Vexriscv sections
Find example of SpinalHDL vs Verilog vs VHDL
## Results
Do a graphical plot of all the final metrics for the tests
## Utilisation and Timing
Utilisation and timing for each FPGA processor
Briefly mention timing constraints, whether or not they were met, failing endpoints etc.
## Power Analysis
What it says in Vivado vs. Real-life on multimeter
## Ethernet Sections
Entire ethernet throughput overview diagram displaying bottlenecks. This diagram will show the complete process for receiving/sending on the FPGA end.
TCP Vs. UDP - i.e. why didn't I use UDP?
## Stack overview
