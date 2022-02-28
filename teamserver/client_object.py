import socket
import sys
import threading
import time

sys.path.append('./teamserver')
from utils.messages import *
from utils.errors_messages import *
from utils.server_utils import list_to_str, send_tcp_message, recv_decorator, \
    recv_decorator_gameserver
from game_object import Game_Object
from extra_feature_utils.game_object_for_4_players import Game_Object_For_4_Player


class ClientObject():
    def __init__(self, lobbyroom, tcp_client_object, addr, server_features_list, thread_id=0,
                 lock=None, logger=None):
        self.lobbyroom = lobbyroom
        self.tcp_client_object = tcp_client_object
        self.addr_tcp = addr
        self.addr_udp_gameserver = None
        self.lock = lock
        self.logger = logger

        self.thread_id = thread_id
        self.sequence_nr = self.sequence_nummer_generator()

        self.udp_sequence_nr = []
        for i in range(4):
            self.udp_sequence_nr.append(self.sequence_nummer_generator())

        self.player_gameroom_id = None
        self.message = None
        self.match_name = None
        self.is_player_in_game_room = False
        self.is_player_ready = False
        self.gameroom = None
        self.game_object = None

        self.cmd_list = ["HELLO", "LIST_GAMES", "CREATE_MATCH", "LIST_MATCHES", "MATCH_FEATURES",
                         "JOIN_MATCH",
                         "LEAVING_MATCH", "I_AM_READY"]

        self.player_name = None
        self.server_features_list = server_features_list
        self.client_feature_list = []

    def run_thread_communication(self):
        while True:
            message = self.tcp_client_object.recv(2048)
            if not message:
                self.tcp_client_object.close()
                print('connection abort')
                break

            message = recv_decorator(message, self.thread_id, self.sequence_nr.__next__(),
                                     logger=self.logger)
            if message[0] not in self.cmd_list:
                send_err_cmd_not_understood(self.tcp_client_object, logger=self.logger)
            if self.lobbyroom.sense_danger():
                send_disconnecting_you(self.tcp_client_object, 0, logger=self.logger)
                self.tcp_client_object.close()
                break

            if self.is_player_in_game_room:
                if is_leaving_match(message):
                    self.is_player_in_game_room = False
                    self.gameroom.in_progress = False

                if is_i_am_ready(message):
                    self.is_player_ready = True
            else:
                self.process_tcp_messages(message)

    def process_tcp_messages(self, message):
        print("waiting for tcp messages ...")
        self.handshake_with_client(message)
        self.information_handling(message)
        self.action_handling(message)

    def handshake_with_client(self, message):
        if is_hello(message):
            self.player_name, self.client_feature_list = output_from_hello(message)
            hand_shake_message = "WELCOME " + list_to_str(self.server_features_list)
            send_tcp_message(self.tcp_client_object, hand_shake_message, logger=self.logger)

    def action_handling(self, message):
        if is_create_match(message):
            game_name, match_name, game_features_list = output_from_create_match(message)
            flag = self.lobbyroom.create_new_game(game_name, match_name, game_features_list,
                                                  self.server_features_list)
            if flag:
                send_failed_to_create(self.tcp_client_object, flag, logger=self.logger)
            else:
                send_match_created(self.tcp_client_object, logger=self.logger)

        if is_join_match(message):
            match_name, color_string = output_from_join_match(message)
            flag = self.lobbyroom.able_to_join_match_from_lobby(match_name, self.addr_tcp)
            if flag or self.is_player_in_game_room:
                if self.is_player_in_game_room: flag = 3
                send_failed_to_join(self.tcp_client_object, flag, logger=self.logger)
            else:
                self.is_player_in_game_room = True
                self.match_name = match_name

                # ----------------colorlist wird von client übernommen-------------------------
                color_list = list(color_string.split(","))
                self.gameroom = self.lobbyroom.get_gameroom_from_name(match_name)
                self.player_gameroom_id = self.gameroom.add_player(self)

                # self.game_object = Game_Object(player_id, color = color_list)
                if '4_players_mode' in self.gameroom.feature:
                    self.game_object = Game_Object_For_4_Player(self.player_gameroom_id,
                                                                color=color_list)
                else:
                    self.game_object = Game_Object(self.player_gameroom_id, color=color_list)

                send_match_joined(self.tcp_client_object, self.player_gameroom_id,
                                  logger=self.logger)

                if self.lobbyroom.is_game_room_full(match_name):
                    port_udp, players_color_list = self.lobbyroom.get_match_info(self.match_name)
                    client_list = self.lobbyroom.get_gameroom_from_name(
                        self.match_name).get_client_list()
                    send_match_started(client_list, port_udp, players_color_list,
                                       logger=self.logger)
                    self.gameroom.in_progress = True
                    threading.Thread(target=self.start_match_thread).start()

    def information_handling(self, message):
        if is_list_games(message):
            send_available_games(self.tcp_client_object, logger=self.logger)

        if is_list_matches(message):
            game_name = output_from_list_matches(message)
            send_games(self.tcp_client_object, self.lobbyroom.games_object_list, game_name,
                       logger=self.logger)

        if is_match_features(message):
            match_name = output_from_match_features(message)
            game_name = self.lobbyroom.find_game_from_match_name(match_name)
            if game_name == 'ERROR':
                send_match_not_exist(self.tcp_client_object, match_name, logger=self.logger)
            else:
                send_match(self.tcp_client_object, game_name, match_name,
                           self.lobbyroom.games_object_list, logger=self.logger)

    def start_match_thread(self):
        self.connect_udp()
        self.wait_for_player_to_be_ready()
        self.streaming_udp_and_tcp()

        match_name = self.close_game()
        self.lobbyroom.delete_gameroom(match_name)

    def close_game(self):
        match_name = self.match_name
        for player in self.gameroom.players:
            winner_id = self.gameroom.winner
            if winner_id is not None:
                if winner_id == player.player_gameroom_id:
                    send_game_ended(player.tcp_client_object, 0, logger=self.logger)
                else:
                    send_game_ended(player.tcp_client_object, 1, logger=self.logger)
                player.reset_client_player()
        return match_name

    def connect_udp(self):
        self.gameroom.s_udp.bind((self.gameroom.ip, self.gameroom.port_udp_gameroom))
        print(f"===  ===")
        print(f"udp binded to port: {self.gameroom.port_udp_gameroom}")

    def wait_for_player_to_be_ready(self):
        # TODO check if the address is duplicated
        while not self.gameroom.all_players_ready():
            time.sleep(0.2)
            print("waiting for player")

        # for player in self.gameroom.players:
        #   player.tcp_client_object.setblocking(True)

    def streaming_udp_and_tcp(self):
        while self.gameroom.in_progress:
            print('Streaming ...')
            for _ in self.gameroom.players:
                self._recv_udp()
            for player in self.gameroom.players:
                self._send_tcp(player, score=self.gameroom.ball_logic.score)
                self._send_udp(player,
                               ball_info=self.gameroom.ball_logic.get_ball_info())
            self.gameroom.update_game()

        print("game ended")

    def _recv_udp(self):
        def udp_addr_already_assigned_to_other_player(addr, current_player):
            already_assigned_to_other_player = False
            for player in players:
                if player is not current_player and addr == player.addr_udp_gameserver:
                    already_assigned_to_other_player = True
            return already_assigned_to_other_player

        players = self.gameroom.players

        if not self.gameroom.all_udp_gameserver_is_assigned():
            while not self.gameroom.all_udp_gameserver_is_assigned():
                message, addr = self.gameroom.s_udp.recvfrom(1024 ** 2)
                for player in players:
                    if addr[0] == player.addr_tcp[0] and player.addr_udp_gameserver is None \
                            and not udp_addr_already_assigned_to_other_player(addr, player):
                        player.addr_udp_gameserver = addr
                        if self.logger is not None:
                            self.logger.info(
                                f'udp connection established with player: {player.player_gameroom_id} on ==================================== addr: {addr}')
                        print(
                            f'udp connection established with player: {player.player_gameroom_id} on ==================================== addr: {addr}')
        else:
            self.gameroom.s_udp.settimeout(0.1)
            try:
                message, addr = self.gameroom.s_udp.recvfrom(1024 ** 2)
                player = players[0]
                for _player in players:
                    if addr == _player.addr_udp_gameserver:
                        player = _player

                messages = recv_decorator_gameserver(message, logger=self.logger)
                for message in messages:
                    if is_keys_pressed(message):
                        player.game_object.key_list = output_from_key_pressed(message)
            except socket.timeout:
                pass

    def _send_tcp(self, current_player, score):
        client = current_player.tcp_client_object
        messages = []
        for player in self.gameroom.players:
            message = f"SCORE_UPDATE {player.player_gameroom_id} {score[player.player_gameroom_id - 1]}"
            messages.append(message)
        messages = list_to_str(messages, '\0')
        send_score_update(client,
                          messages, logger=self.logger)

    def _send_udp(self, player, ball_info):
        addr_udp_gameserver = player.addr_udp_gameserver
        client_id = player.player_gameroom_id - 1

        sequence = self.udp_sequence_nr[client_id].__next__()
        message_ball = f"{sequence} UPDATE_BALL " + list_to_str(ball_info, delimiter=' ')
        messages = [message_ball]
        for player in self.gameroom.players:
            sequence = self.udp_sequence_nr[client_id].__next__()
            player_id, player_state_info = player.game_object.get_player_info()

            messages.append(
                f"{sequence} UPDATE_PLAYER {player_id} " + list_to_str(player_state_info,
                                                                       delimiter=' '))
        messages = list_to_str(messages, '\0')
        send_update_player(self.gameroom.s_udp, addr_udp_gameserver, messages, logger=self.logger)

    def sequence_nummer_generator(self):
        sequence_nummer = 0
        while True:
            yield sequence_nummer
            sequence_nummer += 1

    def reset_client_player(self):
        self.addr_udp_gameserver = None

        self.player_gameroom_id = None
        self.message = None
        self.match_name = None
        self.is_player_in_game_room = False
