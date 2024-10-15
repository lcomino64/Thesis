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
- Introduce what RISC-V is used for, in industry and research
- When mentioning IoT security, mention the 2024 story about the Dyn attack
## Project Overview
## Scope


# Part 2 -Research------------------------------------
# Background
## Computer Networks, TCP/IP
#### Network Layer
#### Link Layer and Ethernet PHY
#### Ethernet Interfaces
## Network Security Methods for Embedded Systems
#### AES Encryption
## RISC-V ISA
#### Overview of RISC-V
#### ISA Extensions
## FPGAs
#### VexRiscv & SpinalHDL
#### Wishbone
#### LiteX Overview
#### Litex BIOS
## Operating Systems
#### Buildroot Linux


# Part 3 -Complete Stack Overview-------------------
## Hardware Setup
#### Network Overview
#### SCPNS
#### Liteeth
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
Specs of the Pi,
## Software Setup
Different Boot methods time taken chart
#### Buildroot Linux Configuration

## Debugging Configuration*


# Part 4-Evaluation-----------------------------------
## Raw Performance Benchmarks & Theoretical Results

## Results & Analysis

## Utilisation, Resources and Timing

## Ethernet Throughput Analysis
## Power Analysis*


# Part 5-Conclusion----------------------------------
## Summary

## Limitations & Security Vulnerabilities

## Future Improvements

## Issues and Reductions in Scope During Development


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
## AES sections
## LiteX and Vexriscv sections
## Results
## Utilisation and Timing
## Ethernet Sections
## Stack overview
## Do Poster First
