import socket

import pygame
from pygame.locals import *

from client_utils import recv_decorator_multi
from gui import Gui


class GameClient(object):
    """
    Client side of the game
    """

    def __init__(self, ip, port, dims, colour_list, id, tcp_sock, match_features_list):
        """
        """

        self.tcp_socket = tcp_sock
        self.tcp_socket.settimeout(1.5)
        self.server_address = (str(ip), int(port))
        self.players_colours_list = []
        self.gui = Gui(dims[0] * dims[2], dims[1] * dims[3])

        if '4_players_mode' in match_features_list:
            self.four_players = True
            self.nr_of_player = 4
        else:
            self.four_players = False
            self.nr_of_player = 2

        self.players_position = [[0, 0] for _ in range(self.nr_of_player)]

        for id, _ in enumerate(self.players_position):
            self.players_colours_list.append(colour_list[4 * id:4 * id + 4])

        # self.clock = pygame.time.Clock()
        self.player_id = int(id)

        """if self.player_id == 0:
            self.ownColour = (colour_list[1], colour_list[2], colour_list[3])
            self.oppColour = (colour_list[5], colour_list[6], colour_list[7])
        else:
            self.oppColour = (colour_list[1], colour_list[2], colour_list[3])
            self.ownColour = (colour_list[5], colour_list[6], colour_list[7])"""
        self.gamestatus = False
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPClientSocket.settimeout(1)
        # self.UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sequence_number = 0

        self.ball_pos = (0, 0)

        self.score_1 = 0
        self.score_2 = 0
        self.score_3 = 0
        self.score_4 = 0

        self.player_pos = (0, 0)
        self.opponent_pos = (0, 0)
        self.player3_pos = (400, 50)
        self.player4_pos = (400, 550)

        self.match_features_list = match_features_list

    def play(self):
        self.ready()
        while True:
            self.keys()
            # time.sleep(0.05)
            end_game = self.score_update()
            self.update_positions(nr_player=self.nr_of_player)
            self.animate()

            if end_game == True:
                pygame.quit()
                return 0

            exiting = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exiting = True

            if self.space_was_pressed() or exiting:
                print("leaving")
                pygame.quit()
                self.send_leave()
                return 0

    def ready(self):
        # self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.settimeout(0.01)
        message = "I_AM_READY\0"
        self.tcp_socket.sendall(message.encode("ascii"))

    def keys(self):
        """
        send pressed key to teamserver
        """
        pygame.event.get()
        key_list = pygame.key.get_pressed()
        key_string_list = []
        if key_list[K_UP]:
            key_string_list.append("UP")
        if key_list[K_DOWN]:
            key_string_list.append("DOWN")

        if key_list[K_RIGHT]:
            key_string_list.append("RIGHT")
        if key_list[K_LEFT]:
            key_string_list.append("LEFT")

        if key_list[K_SPACE]:
            key_string_list.append("SPACE")
        key_string = ','.join(key_string_list)

        if True:  # key:
            message = (str(self.sequence_number) + " KEYS_PRESSED " + key_string + "\0").encode(
                "ascii")
            self.UDPClientSocket.sendto(message, self.server_address)
            self.sequence_number += 1

    def update_positions(self, nr_player=2):
        update_ball = True
        update_players = [True for _ in range(nr_player)]
        try:
            while any([update_ball] + update_players):
                message = self.UDPClientSocket.recv(1024 ** 2)
                msg_lists = recv_decorator_multi(message)
                for msg_list in msg_lists:
                    if msg_list[1] == "UPDATE_BALL":
                        ball_info = msg_list[2:]
                        self.ball_pos = (int(float(ball_info[1])), int(float(ball_info[2])))
                        update_ball = False
                    if msg_list[1] == "UPDATE_PLAYER":
                        player_info = msg_list[2:]
                        for id in range(nr_player):
                            if player_info[0] == str(id + 1):
                                self.players_position[id] = (
                                    int(float(player_info[1])), int(float(player_info[2])))
                                update_players[id] = False
        except socket.timeout:
            print('udp timeout')

    def score_update(self):
        try:
            messages = self.tcp_socket.recv(1024 ** 2)
            messages = recv_decorator_multi(messages)
            for message in messages:
                if message[0] == "SCORE_UPDATE":
                    if message[1] == '1':
                        self.score_1 = message[2]
                        print(f'===={self.score_1}====')
                    elif message[1] == '2':
                        self.score_2 = message[2]
                        print(f'===={self.score_2}====')
                    elif message[1] == '3':
                        self.score_3 = message[2]
                        print(f'===={self.score_3}====')
                    elif message[1] == '4':
                        self.score_4 = message[2]
                        print(f'===={self.score_4}====')
                if message[0] == "GAME_ENDED":
                    print(message[0])
                    print(message[1])
                    return True
        except socket.timeout:
            print('score update timeout')

    def animate(self):
        thickness = 10
        if "half_racket" in self.match_features_list:
            width = 60
        else:
            width = 120

        def big_rect_vertical(inp):
            x = inp[0]
            y = inp[1]
            return {0: pygame.Rect(x, y - width // 2, thickness, width)}

        def big_rect_horizontal(inp):
            x = inp[0]
            y = inp[1]
            return {0: pygame.Rect(x - width // 2, y, width, thickness)}

        def small_rect(inp):
            x = inp[0]
            y = inp[1]
            return pygame.Rect(x, y, 5, 5)

        players_rectangles_and_colors = []
        for player_id, player_pos in enumerate(self.players_position):
            if player_id < 2:
                player_rects = big_rect_vertical(player_pos)
            else:
                player_rects = big_rect_horizontal(player_pos)
            player_color = self.players_colours_list[player_id][1:4]
            players_rectangles_and_colors.append((player_rects, player_color))

        ball_rects = small_rect(self.ball_pos)

        if self.four_players:
            self.gui.render_screen(players_rectangles_and_colors, ball_rects,
                                   [self.score_1, self.score_2, self.score_3, self.score_4],
                                   mode='4_players_mode')
        else:
            self.gui.render_screen(players_rectangles_and_colors, ball_rects,
                                   [self.score_1, self.score_2])

    def send_leave(self):
        message = "LEAVING_MATCH no more waiting\0"
        self.tcp_socket.sendall(message.encode("ascii"))

    def space_was_pressed(self):
        pygame.event.get()
        key_list = pygame.key.get_pressed()
        if key_list[K_SPACE]:
            return True
        return False
