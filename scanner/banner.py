# scanner/banner.py

import socket

# Common ports that need us to send a request first before they respond
PROBE_PAYLOADS = {
    80:   b"GET / HTTP/1.1\r\nHost: target\r\n\r\n",
    443:  b"GET / HTTP/1.1\r\nHost: target\r\n\r\n",
    8080: b"GET / HTTP/1.1\r\nHost: target\r\n\r\n",
    21:   None,   # FTP sends banner immediately
    22:   None,   # SSH sends banner immediately
    25:   None,   # SMTP sends banner immediately
    110:  None,   # POP3 sends banner immediately
    143:  None,   # IMAP sends banner immediately
}

def grab_banner(target: str, port: int, timeout: float = 2.0) -> str:
    """
    Connects to an open port and attempts to read the service banner.
    Returns the banner string, or empty string if nothing received.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target, port))

        # Send a probe if needed (HTTP etc. won't respond until we do)
        payload = PROBE_PAYLOADS.get(port, None)
        if payload:
            sock.send(payload)

        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        sock.close()

        # Clean it up — take only the first meaningful line
        first_line = banner.splitlines()[0] if banner else ""
        return first_line[:100]  # cap at 100 chars

    except Exception:
        return ""
