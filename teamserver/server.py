import argparse
import logging
import socket
import sys
import threading
import time

sys.path.append('./teamserver')
from lobbyroom import Lobbyroom
from utils.messages import is_discover_lobby, send_lobby
from utils.server_utils import recv_decorator
from client_object import ClientObject
from ping_server import start_ping_server
from utils.server_utils import get_log_file_name


class Server(object):
    def __init__(self, server_port=54000, log_on=0):
        start_ping_server(54500)
        self.s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.ip = "0.0.0.0"
        self.port_udp = server_port  # 54000
        self.port_tcp = server_port + 1  # 54001
        if log_on:
            self.logger = logging
            self.logger.basicConfig(level=logging.DEBUG, filename=get_log_file_name(),
                                    filemode="a+",
                                    format="%(asctime)-15s %(levelname)-8s %(message)s")
        else:
            self.logger = None
        # self.address = (ip, port)
        self.udp_client_list = []
        self.tcp_client_list = []

        # TODO take the feature from client instead this hardcoded features

        self.lobby = Lobbyroom()
        self.number_generator = self.thread_nummer_generator()

        self.server_features_list = ['BASIC,DIMS,1,1,800,600', '4_players_mode,DIMS,1,1,800,800',
                                     'gravity', 'higher_ballSpeed', 'half_racket', 'invisibility']

    def run_server(self):
        self.s_udp.bind((self.ip, self.port_udp))
        self.s_tcp.bind((self.ip, self.port_tcp))
        self.s_tcp.listen(10)

        thread_udp = threading.Thread(target=self.udp_broadcasting)
        thread_udp.start()

        self.main_tcp_communication()

    def udp_broadcasting(self):
        while True:
            try:
                print("waiting for broadcast ...")
                message, addr = self.s_udp.recvfrom(2048)
                self.udp_client_list.append(addr)
                message = recv_decorator(message, 0, 0, logger=self.logger)
                time.sleep(0.01)
                if is_discover_lobby(message):
                    send_lobby(self.s_udp, addr, self.port_tcp, logger=self.logger)
            except socket.error:
                print(socket.error)

    def main_tcp_communication(self):
        lock = threading.Lock()
        while True:
            time.sleep(0.01)
            client, addr = self.s_tcp.accept()
            if client not in self.tcp_client_list:
                self.tcp_client_list.append(client)
                thread_nr = self.number_generator.__next__()
                print(f'=== thread nr: {thread_nr} client: {client} addr: {addr} ===')
                thread = threading.Thread(target=self.tcp_threading_process,
                                          args=(client, addr, thread_nr, lock,))
                thread.start()
                self.tcp_client_list.remove(client)

    def tcp_threading_process(self, tcp_client_object, addr, thread_id, lock):
        client_object = ClientObject(self.lobby, tcp_client_object, addr, self.server_features_list,
                                     thread_id, lock, self.logger)
        client_object.run_thread_communication()

    def thread_nummer_generator(self):
        thread_number = 0
        while True:
            yield thread_number
            thread_number += 1


if __name__ == '__main__':
    description = ("port")

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-p",
                        "--port",
                        help="port option",
                        default=54000)
    parser.add_argument("-l",
                        "--log",
                        help="log info",
                        default=0)
    args = parser.parse_args()

    server = Server(int(args.port), int(args.log))
    server.run_server()
