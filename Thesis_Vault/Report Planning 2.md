Title page
Letter to dean
Acknowledgements
Abstract
List of Abbreviations
Contents
List of Figures & Tables

# Part I -Introduction-------------------------------
# Introduction
## Motivation:
Same as before, except:
- Introduce what RISC-V is used for, in industry and research
- When mentioning IoT security, mention the 2024 story about the Dyn attack
## Project Goal
Same as before

# Part 2 -Research---------------------------------
# Background

# Literature Review
## Related Works
## Similar Projects with LiteX
## Preexisting Solutions


# Part 3 -Complete Stack Overview----------------
# SCPNS Hardware Configuration

# SCPNS Software Configuration
Different Boot methods time taken chart
# Network Cluster Testbed

# Debugging Configuration

# Part 4-Evaluation--------------------------------
# Results & Discussion

## Power Analysis

# Part 5-Conclusion--------------------------------

# Conclusion
## Summary

## Limitations & Security Vulnerabilities

## Sustainability

## Future Improvements


# Tests to Run
### Pi Cluster Full Kubernetes & SCPNS: 1 core, 2 core, 4 core
For each of these do:

Basic tests - 1 client, 10 clients, 50 clients - This one can all be made into single table.

1000 clients - how fast can each handle 100 clients with different file sizes?
File sizes vary from 1 to 100mb. 

Clients spawn at a fixed rate for 60mins - how many clients can be handled in 60min?

#### In Appendix, MacOS virtual stats will be added (Virtual doesn't have to contend with network latency)