# scanner/utils.py

def parse_ports(port_str: str) -> list[int]:
    """
    Parses port input into a list of integers.
    Accepts:  "80"  |  "1-1024"  |  "80,443,8080"  |  "-" (all ports)
    """
    ports = []

    if port_str.strip() == "-":
        return list(range(1, 65536))

    for part in port_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))

    return sorted(set(ports))  # deduplicate and sort


def print_banner():
    print("""
    ╔═══════════════════════════════╗
    ║        PyPortScanner          ║
    ║   For authorized use only     ║
    ╚═══════════════════════════════╝
    """)


def format_result(port: int, status: str, service: str = "") -> str:
    service_str = f"  ({service})" if service else ""
    return f"  {port:<6} {status:<10}{service_str}"
