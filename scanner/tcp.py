# scanner/tcp.py

import socket
import threading
from scanner.utils import format_result

open_ports = []
lock = threading.Lock()


def tcp_connect_scan(target: str, port: int, timeout: float, verbose: bool):
    """
    Attempts a full TCP connection to target:port.
    If it connects, the port is open.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))  # returns 0 if open
        sock.close()

        if result == 0:
            with lock:
                open_ports.append(port)
            if verbose:
                print(format_result(port, "OPEN"))

    except socket.error:
        pass


def scan_ports(target: str, ports: list, threads: int, timeout: float, verbose: bool):
    """
    Spawns threads to scan ports concurrently.
    Splits ports into chunks and scans in batches.
    """
    open_ports.clear()
    thread_list = []

    for port in ports:
        t = threading.Thread(
            target=tcp_connect_scan,
            args=(target, port, timeout, verbose)
        )
        thread_list.append(t)
        t.start()

        # Once we hit the thread limit, wait for that batch to finish
        if len(thread_list) >= threads:
            for t in thread_list:
                t.join()
            thread_list = []

    # Wait for any remaining threads
    for t in thread_list:
        t.join()

    return sorted(open_ports)
