import socket, argparse, sys


class TestClient(object):
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.settimeout(20)
        self._client_socket = None

    def run(self):
        print('This is a small program to test your client. '
              'Please start your client now.')

        if self._wait_for_connection():
            print('Connection to client established')
        else:
            return

        if not self._wait_for_hello():
            return
        self._send_welcome()
        print('Handshake passed')

    def _wait_for_connection(self):
        try:
            print('Waiting for connection. IP: %s, Port: %i' % (self._ip, self._port))
            self._socket.bind((self._ip, self._port))
            self._socket.listen(1)
            self._client_socket, addr = self._socket.accept()
            return True
        except socket.timeout:
            print('The client did not connect to the teamserver')
            return False

    def _wait_for_hello(self):
        print('Trying to receive the HELLO message')
        message = self._recv()
        if not message:
            return False
        message = message.split(' ')
        if message[0] != 'HELLO':
            print('Did not receive the HELLO command. Received %s instead' % message[0])
            return False
        elif len(message) != 3:
            print('Argument number must be two (name, features). '
                  'But %i arguments have been passed with HELLO command' % (len(message) - 1))
            return False
        else:
            print('Received HELLO command. Your name is %s. Your client features are: %s'
                  % (message[1], message[2]))
            return True

    def _send_welcome(self):
        print('Sending WELCOME command')
        message = 'WELCOME BASIC,DIMS,800,600,10,40,5'
        self._send(message)

    def _send(self, message):
        message += '\0'
        self._client_socket.sendall(message.encode('ASCII'))

    def _recv(self):
        self._client_socket.settimeout(1)
        message = ''
        while True:
            try:
                message += self._client_socket.recv_udp(1024).decode('ASCII')
                if '\0' in message:
                    message = message[:-1]
                    return message
            except socket.timeout:
                print('Did not receive anything or missing \\0')
                return False


if __name__ == "__main__":

    if sys.version_info[0] is not 3:
        print("ERROR: Please use Python version 3 !! (Your version: %s)"
              % sys.version)
        exit(1)


    def type_port(x):
        x = int(x)
        if x < 1 or x > 65535:
            raise argparse.ArgumentTypeError(
                "Port number has to be greater than 1 and less"
                "than 65535.")
        return x


    description = 'A program to test your teamserver'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i",
                        "--ip",
                        help="IP your client is going to connect to",
                        default='localhost')
    parser.add_argument("-p",
                        "--port",
                        help="Port your client is going to connect to",
                        type=type_port,
                        default=5050)

    args = parser.parse_args()

    TestClient(ip=args.ip, port=args.port).run()
