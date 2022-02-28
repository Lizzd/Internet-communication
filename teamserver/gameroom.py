import socket

from ball_logic import Ball_Logic
from extra_feature_utils.ball_logic_for_4_players import Ball_Logic_For_4_Players


class Gameroom():
    def __init__(self, game_name, match_name, features_list):
        self.s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.ip = "0.0.0.0"
        self.port_udp_gameroom = None

        self.feature = features_list

        self.game_name = game_name
        self.match_name = match_name

        self.players = []
        self.ball_info = None

        if '4_players_mode' in self.feature:
            self.max_player_number = 4
            self.field_size = [800, 800]
            self.ball_logic = Ball_Logic_For_4_Players(self.field_size, self.feature)

        else:
            self.max_player_number = 2
            self.field_size = [800, 600]
            self.ball_logic = Ball_Logic(self.field_size, self.feature)

        self.in_progress = False
        self.winner = None

    def initial_ip_port_config(self, ip, port_udp):
        self.ip = ip
        self.port_udp_gameroom = port_udp

    def get_colors(self):
        players_color_list = []
        for player in self.players:
            players_color_list.append(player.game_object.color)
        return players_color_list

    def is_full(self):
        return len(self.players) == self.max_player_number

    def update_game(self):
        for player in self.players:
            player.game_object.update_playerstates()
        players_states = [player.game_object.position for player in self.players]
        players_velocity_states = [player.game_object.velocity for player in self.players]

        self.winner = self.ball_logic.update_ball(players_states, players_velocity_states)
        if self.winner is None:
            self.in_progress = True
        else:
            self.in_progress = False

    def add_player(self, client_player):
        if not self.is_full():
            player_id = len(self.players) + 1
        self.players.append(client_player)
        return player_id

    def get_tcp_addr_list(self):
        addrs_tcp = []
        for player in self.players:
            addrs_tcp.append(player.addr_tcp)
        return addrs_tcp

    def get_client_list(self):
        clients = []
        for player in self.players:
            clients.append(player.tcp_client_object)
        return clients

    def all_players_ready(self):
        all_player_ready = True
        for player in self.players:
            if not player.is_player_ready:
                all_player_ready = False
        return all_player_ready

    def all_udp_gameserver_is_assigned(self):
        is_assigned = True
        for player in self.players:
            if player.addr_udp_gameserver == None:
                is_assigned = False
        return is_assigned

    def delete_gameroom(self):
        del self
