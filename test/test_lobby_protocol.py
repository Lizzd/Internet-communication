import threading
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from teamclient.lobby_client import LobbyClient
from teamserver.server import Server


def test_create_match():
    server = Server()
    thread = threading.Thread(target=server.run_server)
    thread.start()
    lobby_client = LobbyClient()
    lobby_client.discover_lobby()
    lobby_client.hello()
    answer = lobby_client.send_create_match('epic_game', 'BASIC')
    print(answer)
    if '\0' in answer:
        assert answer[:-1] == 'MATCH_CREATED'


def test_list_match():
    server = Server()
    thread = threading.Thread(target=server.run_server)
    thread.start()
    lobby_client = LobbyClient()
    lobby_client.discover_lobby()
    lobby_client.hello()
    answer = lobby_client.send_list_match()
    print(answer)

    assert answer[0] == 'GAMES'
    assert answer[1] == 'PONG'


def test_match_features():
    server = Server()
    thread = threading.Thread(target=server.run_server)
    thread.start()
    lobby_client = LobbyClient()
    lobby_client.discover_lobby()
    lobby_client.hello()
    lobby_client.send_create_match('epic_game', 'BASIC')
    answer = lobby_client.send_match_features('epic_game')
    print(answer)
    assert answer[0] == 'MATCH'
    assert answer[1] == 'PONG'
    assert answer[2] == 'epic_game'


def test_join_match():
    server = Server()
    thread = threading.Thread(target=server.run_server)
    thread.start()
    lobby_client = LobbyClient()
    lobby_client.discover_lobby()
    lobby_client.hello()
    lobby_client.send_create_match('epic_game', 'BASIC')
    answer = lobby_client.send_join_match('epic_game', (0, 0, 0))
    print('ZICHong', answer)
    assert answer[0] == 'MATCH_JOINED'


if __name__ == '__main__':
    # pass
    test_join_match()
