import socket
import threading


def start_ping_server(port):
    thread = threading.Thread(target=ping_server, args=[port], daemon=True)
    thread.start()


def ping_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    sock.bind(("0.0.0.0", port))
    while True:
        try:
            data, addr = sock.recvfrom(999)
            sock.sendto(data, addr)
        except:
            pass
