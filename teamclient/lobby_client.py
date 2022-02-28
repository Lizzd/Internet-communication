import argparse
import sys

sys.path.append('./teamclient')
import socket
from game_client import GameClient
from client_utils import list_to_str, recv_decorator
import pygame
from pygame.locals import *
import pygame.freetype


class LobbyClient(object):
    """
    Client side of the Lobby
    """

    def __init__(self, name="Gamer", server_ip='localhost', server_port=54000):
        """
        all global variables
        """
        self.server_ip = server_ip  # "127.0.0.1" #"10.149.123.255" #'129.187.223.130'#
        self.server_port = server_port

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.local_features = ['BASIC', '4_players_mode', 'gravity', 'higher_ballSpeed',
                               'half_racket', 'invisibility']
        self.server_features = []
        self.available_features = []
        self.name = name  # "player1"
        self.dims = [0, 0, 0, 0]
        self.game = "Pong"
        self.player_id = 0
        self.open_matches = 0
        self.games = 0
        self.result = [0, 0, 0, 0]
        self.rectColour = (0, 0, 0)
        self.match_features = 'BASIC'

    def discover_lobby(self):
        """
        broadcast with udp to get teamserver address=(ip,port)
        """
        udp_lobby_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_lobby_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        lobby_server_address = (self.server_ip, self.server_port)
        message = "DISCOVER_LOBBY"
        udp_lobby_client.sendto(bytes(message, "ascii"), lobby_server_address)
        print("waiting for broadcast ...")
        try:
            udp_lobby_client.settimeout(1)
            msg, address = udp_lobby_client.recvfrom(2048)
            answer = recv_decorator(msg)
            self.server_ip = address[0]
            self.server_port = int(answer[1])
        except socket.timeout:
            answer = 0
            print('broadcast timeout')
        finally:
            udp_lobby_client.close()

        # multiprocessing.Process(target=start_pinger, args=((self.server_ip, 54500),) ).start()
        return answer

    def hello(self):
        """
        send hello, client handshake, receive teamserver game features
        """
        self.tcp_socket.connect((self.server_ip, self.server_port))
        message = "HELLO " + self.name + " " + list_to_str(self.local_features) + "\0"
        self.tcp_socket.sendall(message.encode("ascii"))
        answer = self.tcp_socket.recv(1024 ** 2)
        answer = recv_decorator(answer)
        # answer = answer[1].split(",")
        self.get_server_features(answer[1])
        self.server_features = answer[
            1]  # Frage: Warum nur feature answer[0]. Weil wir nur BASIC wollen?
        print('local features: ', self.local_features)
        print('server features: ', self.server_features)
        print('available features: ', self.available_features)
        # self.match_features = self.server_features
        # for i in range(4):
        #   self.dims[i] = int(answer[i + 2])
        return answer

    def get_server_features(self, server_feature_string):
        server_feature_list = server_feature_string.split(',')
        for feature in self.local_features:
            if feature in server_feature_list:
                index = server_feature_list.index(feature)
                sub_features_list = server_feature_list[index:]
                if len(sub_features_list) >= 2:
                    if 'DIMS' in sub_features_list[:2]:
                        dimension_infos = sub_features_list[2:6]
                        self.available_features.append(feature + ',' + list_to_str(dimension_infos))
                    else:
                        self.available_features.append(feature)
                else:
                    self.available_features.append(feature)

    def send_list_games(self):
        """
        list all available games
        """
        message = "LIST_GAMES " + "\0"
        self.tcp_socket.sendall(message.encode("ascii"))
        answer = self.tcp_socket.recv(1024 ** 2)
        answer = recv_decorator(answer)
        self.games = answer[1]
        print("Games: " + self.games)
        return answer

    def send_create_match(self, match_name, features='BASIC'):
        """
        create a new match
        """
        is_all_features_avaiable = True
        for feature in features.split(','):
            if any(feature in substring for substring in self.available_features):
                pass
            else:
                is_all_features_avaiable = False
                print(
                    f'feature {feature} is not avilable on server ip: {self.server_ip} port: {self.server_port}. available features {self.available_features}')
        if is_all_features_avaiable:
            message = "CREATE_MATCH " + self.game + " " + match_name + " " + list_to_str(
                features) + "\0"
            self.tcp_socket.sendall(message.encode("ascii"))
            answer = self.tcp_socket.recv(1024 ** 2)
            answer = recv_decorator(answer)
            print("Match created")
            return answer
        return 0

    def send_list_match(self):
        """
        request a list with all open matches
        """
        message = "LIST_MATCHES " + self.game + "\0"
        self.tcp_socket.sendall(message.encode("ascii"))
        answer = self.tcp_socket.recv(1024 ** 2)
        answer = recv_decorator(answer)
        self.open_matches = answer[2]
        print("Open matches: " + self.open_matches)
        return answer

    def send_match_features(self, match_name):
        """
        get match_features and print them
        """
        message = "MATCH_FEATURES " + match_name + "\0"
        self.tcp_socket.sendall(message.encode("ascii"))
        answer = self.tcp_socket.recv(1024 ** 2)
        answer = recv_decorator(answer)
        self.match_features = answer[3].split(',')
        is_all_features_avaiable = True
        for feature in self.match_features:
            if any(feature in substring for substring in self.available_features):
                pass
            else:
                is_all_features_avaiable = False
                print(
                    f'feature {feature} is not avilable on server ip: {self.server_ip} port: {self.server_port}. available features {self.available_features}')
        if is_all_features_avaiable:

            if '4_players_mode' in self.match_features:
                self.dims = [1, 1, 800, 800]
            else:
                self.dims = [1, 1, 800, 600]
        print("Match features: " + list_to_str(self.match_features))
        return answer

    def send_join_match(self, match_name, colour):
        """
        send picked match_name to teamserver
        """
        self.send_match_features(match_name)
        message = "JOIN_MATCH " + match_name + " " + ','.join([str(x) for x in colour]) + "\0"
        self.tcp_socket.sendall(message.encode("ascii"))
        answer = self.tcp_socket.recv(1024 ** 2)
        answer = recv_decorator(answer)
        self.player_id = answer[1]
        return answer

    def wait_for_game(self):
        """
        wait for the match to start
        """
        self.tcp_socket.settimeout(0.1)
        print("waiting for game to start")
        waiting_animation = self.animate_waiting()
        while True:
            try:
                answer = self.tcp_socket.recv(1024 ** 2)
                answer = recv_decorator(answer)
                if answer[0] == "MATCH_STARTED":
                    port = int(answer[1])
                    colour_list = [int(float(x)) for x in answer[2].split(',')]
                    self.play_pong(port, colour_list)
                    self.tcp_socket.settimeout(4)
                    # sys.exit()
                    return 0
            except socket.timeout:
                waiting_animation.update()
                exiting = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exiting = True

                if self.space_was_pressed() or exiting:
                    print("waiting interrupted")
                    pygame.quit()
                    self.send_leave()
                    return 0

    def play_pong(self, port, colour_list):
        """start the game client

        Arguments:
            port {int} -- udp port the server is binded to
            colour_list {int-list} -- colour values
        """
        print("game starts")
        player = GameClient(self.server_ip, port, self.dims, colour_list, self.player_id,
                            self.tcp_socket,
                            self.match_features)
        player.play()

        if player.nr_of_player == 2:
            self.result = [1, int(player.score_1), int(player.score_2), int(self.player_id)]
        else:
            self.result = [1, int(player.score_1), int(player.score_2), int(player.score_3),
                           int(player.score_4), int(self.player_id)]
        print("game ended")

    def send_leave(self):
        message = "LEAVING_MATCH no more waiting\0"
        self.tcp_socket.sendall(message.encode("ascii"))

    def space_was_pressed(self):
        pygame.event.get()
        key_list = pygame.key.get_pressed()
        if key_list[K_SPACE]:
            return True
        return False

    def animate_waiting(self):
        pygame.init()
        display_surface = pygame.display.set_mode(
            (self.dims[0] * self.dims[2], self.dims[1] * self.dims[3]))
        pygame.display.set_caption('waiting...')
        display_surface.fill((0, 0, 0))

        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render('Pong', True, (255, 255, 255), (
            0, 0,
            0))  # \n waiting for game \n press [SPACE] to return to menu', True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (400, 200)
        display_surface.blit(text, textRect)

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('waiting for game to start ...', True, (255, 255, 255), (
            0, 0,
            0))  # \n waiting for game \n press [SPACE] to return to menu', True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (400, 300)
        display_surface.blit(text, textRect)

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('press [SPACE] to return to menu', True, (255, 255, 255), (
            0, 0,
            0))  # \n waiting for game \n press [SPACE] to return to menu', True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (400, 350)
        display_surface.blit(text, textRect)

        return pygame.display


if __name__ == "__main__":
    description = ("port")

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-p",
                        "--port",
                        help="port option",
                        default=54000)
    parser.add_argument("-ip",
                        "--ip_address",
                        help="ip_address",
                        default='localhost')
    parser.add_argument("-b",
                        "--broadcast",
                        help="broadcast?",
                        default=1)

    args = parser.parse_args()

    lobby_client = LobbyClient(server_ip=args.ip_address, server_port=int(args.port))
    if int(args.broadcast):
        lobby_client.discover_lobby()

    lobby_client.hello()
    while True:
        argument = input(
            'Options: \n LIST_GAMES [g] \n LIST_MATCH [l] \n JOIN_MATCH [j] + match name + color \n '
            'CREATE_MATCH [c] + match name + features (higher_ballSpeed / invisibility / multiple_balls '
            '/ half_racket / gravity) \n MATCH_FEATURES [m] + match name \n Please enter your command:')
        argument = argument.split(' ')
        print(argument)
        if argument[0] == "LIST_GAMES" or argument[0] == "g":
            lobby_client.send_list_games()
        if argument[0] == "LIST_MATCH" or argument[0] == "l":
            lobby_client.send_list_match()
        if argument[0] == "JOIN_MATCH" or argument[0] == "j":
            _ = lobby_client.send_join_match(argument[1], (225, 225, 225))
            lobby_client.wait_for_game()
        if argument[0] == "CREATE_MATCH" or argument[0] == "c":
            _ = lobby_client.send_create_match(argument[1], argument[2])
        if argument[0] == "MATCH_FEATURES" or argument[0] == "m":
            _ = lobby_client.send_match_features(argument[1])
        if argument[0] == "EXIT":
            break
