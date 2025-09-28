# Memory Forensics Challenges

This document provides a series of exercises on memory forensics for both Windows and Linux systems. The challenges are designed for use with the Volatility 3 framework.

**A Note for the Instructor:** Generating realistic memory dumps is complex. Instead of providing scripts for generation, these exercises use publicly available, well-documented memory samples from the Volatility Foundation and other sources. This ensures students work with standard, high-quality artifacts. Please download the required files from the links provided.

**Setup:**
Before starting, install Volatility 3 and its dependencies:
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip
pip3 install volatility3
```

## Stuxnet Memory Dump Analysis

Follow the instructions [here](https://medium.com/@neerajcysec/memory-analysis-of-stuxnet-with-volatility-57369ca29b1c) and use Volatility to analyze the [Stuxnet attack](https://en.wikipedia.org/wiki/Stuxnet) memory dump.

## Zeus Memory Dump Analysis

Follow the instructions [here](https://medium.com/@neerajcysec/memory-analysis-of-zeus-with-volatility-c6d140a0691a) and use Volatility to analyze the [Zeus attack](https://en.wikipedia.org/wiki/Zeus_(malware)) memory dump.
