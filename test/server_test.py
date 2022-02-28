import socket, argparse, sys


class TestServer(object):
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(5)

    def run(self):
        print('This is a small program to test your teamserver. '
              'Please start your teamserver now and press ENTER after the teamserver is running')
        input()
        if self._connect_to_server():
            print('Connection to teamserver established')
        else:
            print('Failed to connect to the Server.')
            return

        self._send_hello()

        if not self._get_welcome():
            return
        else:
            print('Handshake passed')

    def _connect_to_server(self):
        while True:
            try:
                print('Trying to connect to the teamserver')
                self._socket.connect((self._ip, self._port))
                return True
            except socket.timeout:
                print('Was not able to connect to the teamserver. Do you want to retry? yes/no')
                answer = input("> ")
                if answer == "YES" or answer == "yes" or answer == "Yes" or answer == "y":
                    pass
                else:
                    return False

    def _send_hello(self):
        print('Sending HELLO message')
        message = 'HELLO Server_Tester BASIC'
        self._send(message)
        print('HELLO message sent')

    def _get_welcome(self):
        print('Trying to receive the WELCOME message')
        message = self._recv()
        if not message:
            return False
        message = message.split(' ')
        print(message)
        features = message[1].split(',')
        print(len(features))
        if message[0] != 'WELCOME':
            print('Did not receive the WELCOME command. Received %s instead' % message[0])
            return False
        elif len(message) != 2:
            print(message)
            print('Argument number must be one [features,dimensions(optional)].'
                  'But %i arguments have been passed with WELCOME command' % (len(message) - 1))
            return False
        else:
            if len(features) < 2:
                print(
                    'Received WELCOME command. Your teamserver features are: %s. The dimensions are not specified.'
                    % (features[0]))
            else:
                print(
                    'Received WELCOME command. Your teamserver features are: %s. The dimensions are %s'
                    % (features[0], ','.join(features[2:])))
            return True

    def _send(self, message):
        message += '\0'
        self._socket.sendall(message.encode('ASCII'))

    def _recv(self):
        self._socket.settimeout(1)
        message = ''
        while True:
            try:
                message += self._socket.recv(1024).decode('ASCII')
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
                        help="IP your teamserver is listening on",
                        default='localhost')
    parser.add_argument("-p",
                        "--port",
                        help="Port your teamserver is listening on",
                        type=type_port,
                        default=54001)

    args = parser.parse_args()

    TestServer(ip=args.ip, port=args.port).run()
