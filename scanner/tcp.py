# scanner/tcp.py

import socket
import threading
from scanner.utils import format_result
from scanner.banner import grab_banner

open_ports = []
lock = threading.Lock()


def tcp_connect_scan(target: str, port: int, timeout: float, verbose: bool):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()

        if result == 0:
            banner = grab_banner(target, port, timeout)
            with lock:
                open_ports.append((port, banner))
            if verbose:
                print(format_result(port, "OPEN", banner))

    except socket.error:
        pass


def scan_ports(target: str, ports: list, threads: int, timeout: float, verbose: bool):
    open_ports.clear()
    thread_list = []

    for port in ports:
        t = threading.Thread(
            target=tcp_connect_scan,
            args=(target, port, timeout, verbose)
        )
        thread_list.append(t)
        t.start()

        if len(thread_list) >= threads:
            for t in thread_list:
                t.join()
            thread_list = []

    for t in thread_list:
        t.join()

    return sorted(open_ports, key=lambda x: x[0])
