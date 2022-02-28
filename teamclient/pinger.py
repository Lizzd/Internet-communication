import multiprocessing
import socket
import time

import matplotlib.pyplot as plt


def start_pinger(addr):
    simulate = multiprocessing.Process(None, pinger, args=[addr])
    simulate.start()


def pinger(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    message = "ping123".encode("ascii")
    t0 = time.time()

    plt.figure(figsize=(5, 2), num="Ping")
    plt.title("Ping")
    plt.ylabel("RTT in ms")
    plt.xlabel("time in s")
    x = []
    y = []

    while True:
        time.sleep(1)
        t1 = time.time()
        sock.sendto(message, addr)
        try:
            data, addr = sock.recvfrom(999)
        except:
            pass
        t2 = time.time()
        rtt = (t2 - t1) * 1000
        x.append(t2)
        y.append(rtt)
        plt.plot(x, y, color='blue', linewidth=0.1)
        plt.pause(0.05)
        print("RTT: " + str(int(rtt)) + "ms")


if __name__ == "__main__":
    start_pinger(("127.0.0.1", 54000))
