from utils.server_utils import send_tcp_message


def send_err_cmd_not_understood(client, logger):
    message = "ERR_CMD_NOT_UNDERSTOOD"
    send_tcp_message(client, message, logger=logger)


def send_failed_to_create(client, reason, logger):
    reason_option = ['Missing Match-name', 'Name already taken', 'Game-features does not exist']
    message = "ERR_FAILED_TO_CREATE " + reason_option[reason]
    send_tcp_message(client, message, logger=logger)


def send_failed_to_join(client, reason, logger):
    reason_option = ['', 'Match does not exist', 'Room already full', 'your can only join once']
    message = "ERR_FAILED_TO_JOIN " + reason_option[reason]
    send_tcp_message(client, message, logger=logger)


def send_game_not_exist(client, name, logger):
    message = f"ERR_GAME_NOT_EXIST {name}"
    send_tcp_message(client, message, logger=logger)


def send_match_not_exist(client, match_name, logger):
    message = f"ERR_MATCH_NOT_EXIST {match_name}"
    send_tcp_message(client, message, logger=logger)


def send_disconnecting_you(client, reason, logger):
    reason_option = ['You are banned', 'Your internetcommunication speed is wonderful']
    message = "DISCONNECTING_YOU " + reason_option[reason]
    send_tcp_message(client, message, logger=logger)


# TODO whitespaces problems
def is_leaving_match(message):
    return message[0] == "LEAVING_MATCH"
