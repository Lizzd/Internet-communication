from utils.server_utils import send_tcp_message, send_udp_message, list_to_str


# =========================
# LOBBY Protokoll
# =========================

def is_discover_lobby(message):
    return message[0] == "DISCOVER_LOBBY"


def send_lobby(s_udp, addr, port_tcp, logger):
    message = f"LOBBY {port_tcp}"
    send_udp_message(s_udp, addr, message, logger=logger)


def is_hello(message):
    return message[0] == "HELLO"


def output_from_hello(message):
    return message[1], message[2].split(',')


def is_list_games(message):
    return message[0] == "LIST_GAMES"


def send_available_games(client, logger):
    available_games = ['Pong', 'Tron']
    messsage = "AVAILABLE_GAMES " + list_to_str(available_games)
    send_tcp_message(client, messsage, logger=logger)


def is_create_match(message):
    return message[0] == "CREATE_MATCH"


def output_from_create_match(message):
    if len(message) <= 4:
        return message[1], message[2], message[3].split(',')
    else:
        print("recv message has the wrong format")
        return 0


def send_match_created(client, logger):
    messsage = "MATCH_CREATED"
    send_tcp_message(client, messsage, logger=logger)


def is_list_matches(message):
    return message[0] == "LIST_MATCHES"


def output_from_list_matches(message):
    return message[1]


def send_games(client, games_name_list, game_name, logger):
    message = f"GAMES {game_name} " + list_to_str(list(games_name_list[game_name].keys()))
    send_tcp_message(client, message, logger=logger)


def is_match_features(message):
    return message[0] == "MATCH_FEATURES"


def output_from_match_features(message):
    return message[1]


def send_match(client, game_name, match_name, games_object_list, logger):
    match_features = games_object_list[game_name][match_name].feature
    message = f"MATCH {game_name} {match_name} " + list_to_str(match_features)
    send_tcp_message(client, message, logger=logger)


def is_join_match(message):
    return message[0] == "JOIN_MATCH"


def output_from_join_match(message):
    if len(message) <= 3:
        return message[1], message[2]
    else:
        print("recv message has the wrong format")
        return 0


def send_match_joined(client, player_id, logger):
    message = f"MATCH_JOINED {player_id}"
    send_tcp_message(client, message, logger=logger)


def send_match_started(client_list, port, players_color_list, logger):
    color_infos = ""
    for player_id, player_color in enumerate(players_color_list):
        color_infos += f"{player_id + 1},{list_to_str(player_color)},"
    for client in client_list:
        message = f"MATCH_STARTED {port} " + color_infos[:-1]  # To delete the last redundant comma.
        send_tcp_message(client, message, logger=logger)


def send_game_ended(client, outcome, logger):
    game_ended_reasons = ['YOU WON!', 'YOU LOST!']
    message = "GAME_ENDED " + game_ended_reasons[outcome]
    send_tcp_message(client, message, logger=logger)


# =========================
# GAME Protokoll
# =========================

def is_i_am_ready(message):
    return message[0] == "I_AM_READY"


def send_score_update(client, messages, logger):
    send_tcp_message(client, messages, logger=logger)


def is_keys_pressed(message):
    return message[1] == "KEYS_PRESSED"


def output_from_key_pressed(message):
    return message[2].split(',')


def send_update_ball(socket, addr, ball_info, seq, logger):
    message = f"{seq} UPDATE_BALL " + list_to_str(ball_info, delimiter=' ')
    send_udp_message(socket, addr, message, logger=logger)


def send_update_player(socket, addr, messages, logger):
    send_udp_message(socket, addr, messages, logger=logger)
