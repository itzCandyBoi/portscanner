# PyPortScanner

A command-line port scanner built in Python, inspired by Nmap.
Built as a portfolio project to demonstrate network programming and cybersecurity fundamentals.

## Features

- **TCP Connect Scan** — full 3-way handshake, works without admin privileges
- **SYN Scan** — half-open stealth scan using raw packets via Scapy (requires Administrator)
- **Banner Grabbing** — identifies services and versions running on open ports
- **OS Fingerprinting** — estimates target OS from TTL values in responses
- **Multithreaded** — scans hundreds of ports concurrently for speed
- **Flexible port input** — single ports, ranges, comma-separated, or all 65535 ports
- **Output to file** — save results for reporting

## Requirements

- Python 3.10+
- Scapy (`pip install scapy`)
- [Npcap](https://npcap.com) (Windows only, required for SYN scan)

## Installation
```bash
git clone https://github.com/yourusername/portscanner.git
cd portscanner
pip install scapy
```

## Usage
```bash
# Basic TCP scan
python portscanner.py scanme.nmap.org -p 1-1024

# TCP scan with verbose output and save results
python portscanner.py scanme.nmap.org -p 1-1024 -v -o results.txt

# SYN scan (run as Administrator)
python portscanner.py 192.168.1.1 -p 1-1024 --scan-type syn -v

# Scan specific ports
python portscanner.py 192.168.1.1 -p 22,80,443,3306

# Scan all 65535 ports
python portscanner.py 192.168.1.1 -p -
```

## Arguments

| Argument | Description | Default |
|---|---|---|
| `target` | IP address or hostname | required |
| `-p, --ports` | Port range (e.g. 1-1024, 80,443, -) | 1-1024 |
| `-t, --threads` | Number of concurrent threads | 100 |
| `--timeout` | Connection timeout in seconds | 1.0 |
| `--scan-type` | tcp or syn | tcp |
| `-v, --verbose` | Print results in real time | off |
| `-o, --output` | Save results to file | off |

## Example Output
