# portscanner.py

import argparse
import socket
import sys
from scanner.utils import parse_ports, print_banner, format_result
from scanner.tcp import scan_ports


def resolve_target(target: str) -> str:
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

    print("[*] Starting TCP scan...\n")
    open_ports = scan_ports(target_ip, ports, args.threads, args.timeout, args.verbose)

    # Summary
    print("\n" + "-" * 40)
    print(f"[+] Scan complete. {len(open_ports)} open port(s) found:\n")
    for port in open_ports:
        print(format_result(port, "OPEN"))

    # Save to file if requested
    if args.output:
        with open(args.output, "w") as f:
            f.write(f"Scan results for {args.target} ({target_ip})\n")
            f.write("-" * 40 + "\n")
            for port in open_ports:
                f.write(f"{port} OPEN\n")
        print(f"\n[+] Results saved to {args.output}")


if __name__ == "__main__":
    main()
