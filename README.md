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
    ╔═══════════════════════════════╗
    ║        PyPortScanner          ║
    ║   For authorized use only     ║
    ╚═══════════════════════════════╝

  Target    : scanme.nmap.org (45.33.32.156)
  Ports     : 1024 ports to scan
  Scan type : TCP
  Threads   : 100
  Timeout   : 1.0s
----------------------------------------
[*] Starting TCP scan...

  80     OPEN        (HTTP/1.1 200 OK)
  22     OPEN        (SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13)

----------------------------------------
[+] Scan complete. 2 open port(s) found:

  22     OPEN        (SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13)
  80     OPEN        (HTTP/1.1 200 OK)

## Legal Disclaimer

This tool is intended for use on systems you own or have explicit permission
to test. Unauthorized port scanning may be illegal in your jurisdiction.
The author assumes no liability for misuse.

## How It Works

- **TCP scan** uses Python's `socket` library to attempt a full connection.
  A successful connection means the port is open.
- **SYN scan** uses Scapy to craft raw TCP packets with the SYN flag set.
  A SYN-ACK response indicates an open port; the scanner immediately sends
  RST to avoid completing the handshake.
- **Banner grabbing** reads the first bytes a service sends after connection,
  revealing what software is running.
- **OS fingerprinting** reads the TTL field from responses — Linux systems
  typically use TTL 64, Windows uses TTL 128.
