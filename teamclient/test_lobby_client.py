import argparse
import time

from lobby_client import LobbyClient


def test_lobby_client(match_name="my_game", join='my_game', feature='BASIC'):
    lobby_client = LobbyClient()
    lobby_client.discover_lobby()
    lobby_client.hello()
    time.sleep(0.1)
    lobby_client.send_list_match()
    time.sleep(0.1)
    if lobby_client.open_matches == '':
        _ = lobby_client.send_create_match(match_name, feature)
        open_match = match_name
    else:
        open_match = lobby_client.open_matches
    time.sleep(0.1)
    _ = lobby_client.send_join_match(open_match, (225, 225, 225))
    time.sleep(0.05)
    lobby_client.wait_for_game()


if __name__ == '__main__':
    description = ("prepregrammed command of faster testing")

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i",
                        "--id",
                        help="player id",
                        default=0)

    parser.add_argument("-c",
                        "--create_name",
                        help="default match name",
                        default="my_game")
    parser.add_argument("-f",
                        "--features",
                        help="matchfeatures",
                        default='BASIC')
    parser.add_argument("-j",
                        "--join",
                        help="game to join",
                        default="my_game")

    args = parser.parse_args()

    lobby_client = LobbyClient()
    lobby_client.discover_lobby()
    lobby_client.hello()
    time.sleep(0.1)
    lobby_client.send_list_match()
    time.sleep(0.1)
    if lobby_client.open_matches == '':
        _ = lobby_client.send_create_match(args.create_name, args.features)
        open_match = args.create_name
    else:
        open_match = lobby_client.open_matches
    time.sleep(0.1)
    _ = lobby_client.send_join_match(args.join, (225, 225, 225))
    time.sleep(0.05)
    lobby_client.wait_for_game()
