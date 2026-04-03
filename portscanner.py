# portscanner.py

import argparse
import socket
import sys
from scanner.utils import parse_ports, print_banner

def resolve_target(target: str) -> str:
    """Resolves hostname to IP address."""
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print(f"[!] Could not resolve host: {target}")
        sys.exit(1)


def get_args():
    parser = argparse.ArgumentParser(
        description="PyPortScanner - A simple port scanner",
        epilog="Example: python portscanner.py 192.168.1.1 -p 1-1024 -t 200"
    )
    parser.add_argument("target",
                        help="IP address or hostname to scan")
    parser.add_argument("-p", "--ports",
                        default="1-1024",
                        help="Port range: 80 | 1-1024 | 80,443 | - (all)")
    parser.add_argument("-t", "--threads",
                        type=int, default=100,
                        help="Number of threads (default: 100)")
    parser.add_argument("--timeout",
                        type=float, default=1.0,
                        help="Connection timeout in seconds (default: 1.0)")
    parser.add_argument("-o", "--output",
                        help="Save results to a file")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Print results as they are found")
    return parser.parse_args()


def main():
    print_banner()
    args = get_args()

    target_ip = resolve_target(args.target)
    ports = parse_ports(args.ports)

    print(f"  Target : {args.target} ({target_ip})")
    print(f"  Ports  : {len(ports)} ports to scan")
    print(f"  Threads: {args.threads}")
    print(f"  Timeout: {args.timeout}s")
    print("-" * 40)

    # Scanning logic will plug in here in Stage 2
    print("[*] Scanner logic coming in Stage 2...")


if __name__ == "__main__":
    main()
