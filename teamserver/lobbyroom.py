from gameroom import Gameroom


class Lobbyroom():
    def __init__(self):
        self.game_ended = False
        self.games_object_list = {'Pong': {},
                                  'Tron': {}}
        self.port_number = self.port_generator()

    def create_new_game(self, game_name, match_name, game_features, server_features):
        # TODO check duplicated matchname and player color then return as flag 0,1 or 2
        if self.match_name_not_taken(match_name):
            is_game_feature_available = True
            for game_feature in game_features:
                if any(game_feature in substring for substring in server_features):
                    pass
                else:
                    is_game_feature_available = False

            if is_game_feature_available:
                gameroom = Gameroom(game_name, match_name, game_features)
                port_udp = self.port_number.__next__()
                gameroom.initial_ip_port_config(ip='0.0.0.0', port_udp=port_udp)
                self.games_object_list[game_name][match_name] = gameroom
                flag = 0
            else:
                flag = 2
        else:
            flag = 1
        return flag

    def get_match_info(self, match_name):
        if not self.match_name_not_taken(match_name):
            game_name = self.find_game_from_match_name(match_name)
            gameroom = self.games_object_list[game_name][match_name]
            players_color_list = gameroom.get_colors()

            port_udp = gameroom.port_udp_gameroom

            return port_udp, players_color_list

    def is_game_room_full(self, match_name):
        if not self.match_name_not_taken(match_name):
            gameroom = self.get_gameroom_from_name(match_name)
        return gameroom.is_full()

    def match_name_not_taken(self, match_name):
        name_available = True
        for game_name, match_list in self.games_object_list.items():
            if match_name in match_list.keys():
                name_available = False
        return name_available

    def able_to_join_match_from_lobby(self, match_name, addr_tcp):
        # TODO check duplicated matchname and player color then return as flag 0,1
        # TODO Player ID
        if not self.match_name_not_taken(match_name):
            gameroom = self.get_gameroom_from_name(match_name)
            if not gameroom.is_full():
                if addr_tcp not in gameroom.get_tcp_addr_list():
                    flag = 0
                else:
                    flag = 3
            else:
                flag = 2
        else:
            flag = 1
        return flag

    def get_gameroom_from_name(self, match_name):
        game_name = self.find_game_from_match_name(match_name)
        return self.games_object_list[game_name][match_name]

    def find_game_from_match_name(self, match_name):
        game = "ERROR"
        for game_name, match_list in self.games_object_list.items():
            if match_name in match_list.keys():
                game = game_name
        return game

    def delete_gameroom(self, match_name):
        game_name = self.find_game_from_match_name(match_name)
        game_room = self.games_object_list[game_name].pop(match_name)
        print('game room', game_room, 'get deleted')

    def port_generator(self):
        for port_nr in range(54010, 54100):
            yield port_nr

    def sense_danger(self):
        return False

    # TODO clear up empty room every 10 s
    def update_room(self):
        pass
