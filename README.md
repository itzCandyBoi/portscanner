# PyPortScanner

A Python-based port scanner built as a cybersecurity portfolio project.
Supports TCP connect scanning and SYN (half-open) scanning with
service banner grabbing and OS fingerprinting.

---

## Features

- TCP connect scan — reliable, works without admin privileges
- SYN (half-open) scan — stealthier, requires Administrator + Npcap
- Service banner grabbing — identifies what is running on open ports
- OS fingerprinting — guesses the target OS from TTL values
- Multithreaded scanning — fast concurrent TCP scanning
- Output to file — save results as a report
- Verbose mode — see results in real time as ports are discovered

---

## Project Structure

    portscanner/
    ├── portscanner.py       # Entry point and CLI
    ├── scanner/
    │   ├── tcp.py           # Multithreaded TCP connect scan
    │   ├── syn.py           # SYN scan with Scapy + OS fingerprinting
    │   ├── banner.py        # Service banner grabbing
    │   └── utils.py         # Port parsing, formatting, helpers
    └── README.md

---

## Requirements

    pip install scapy

For SYN scanning on Windows, also install
[Npcap](https://npcap.com) with WinPcap API-compatible mode enabled.

---

## Usage

### TCP Scan (default)

    python portscanner.py <target> -p <ports> [options]

### SYN Scan (requires Administrator)

    python portscanner.py <target> -p <ports> --scan-type syn

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `-p` | Port range: `80`, `1-1024`, `80,443`, `-` (all) | `1-1024` |
| `-t` | Number of threads | `100` |
| `--timeout` | Connection timeout in seconds | `1.0` |
| `--scan-type` | `tcp` or `syn` | `tcp` |
| `-o` | Save results to file | None |
| `-v` | Verbose — print results in real time | Off |

---

## Examples

    # Scan common ports on a target
    python portscanner.py scanme.nmap.org -p 1-1024 -v

    # Scan specific ports
    python portscanner.py 192.168.1.1 -p 22,80,443,8080 -v

    # SYN scan with output saved (run as Administrator)
    python portscanner.py 192.168.1.1 -p 1-1024 --scan-type syn -o results.txt

    # Scan all 65535 ports
    python portscanner.py 192.168.1.1 -p - -t 500

---

## How It Works

### TCP Connect Scan
Attempts a full 3-way TCP handshake (SYN → SYN-ACK → ACK) on each
port. If the connection succeeds the port is open. Fast and reliable
but easily logged by the target since a full connection is made.

### SYN Scan
Sends only a SYN packet and waits for a response. A SYN-ACK means
the port is open — a RST is sent immediately to avoid completing the
handshake. Stealthier than TCP connect but requires raw socket access
(Administrator + Npcap on Windows).

### Banner Grabbing
After finding an open port, connects and reads the first bytes the
service sends. Reveals the service name and version — for example
SSH-2.0-OpenSSH_6.6.1p1 or HTTP/1.1 200 OK.

### OS Fingerprinting
Reads the TTL value from responses. TTL around 64 suggests Linux/Unix,
TTL around 128 suggests Windows. This is a hint only — TTL decrements
at each network hop so results may vary.

---

## Legal Notice

This tool is intended for use only on systems you own or have explicit
written permission to test. Unauthorised port scanning may be illegal
in your jurisdiction. The author takes no responsibility for misuse.

---

## Known Limitations

- SYN scan on Windows may not detect open ports on external internet
  hosts due to the Windows network stack intercepting responses before
  Scapy can read them. Use TCP scan for external targets.
- UDP scanning is not yet implemented.
- Banner grabbing may return empty for services that do not send a
  greeting automatically.
