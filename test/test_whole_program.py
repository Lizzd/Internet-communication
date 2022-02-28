import sys
import os

import threading
from teamserver.server import Server
from teamclient.test_lobby_client import test_lobby_client
import time

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

server = Server()
thread = threading.Thread(target=server.run_server)
thread.start()
time.sleep(1)
# threading.Thread(target= lambda : test_lobby_client(feature='4_players_mode')).start()
# time.sleep(1)
threading.Thread(target=test_lobby_client).start()
time.sleep(1)
threading.Thread(target=test_lobby_client).start()
# time.sleep(1)
# threading.Thread(target=  test_lobby_client).start()
