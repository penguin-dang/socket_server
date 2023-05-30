import time
import json
import traceback
import threading
from threading import Thread

from server import CommunicationServer
import messages

def main():
    global socket_server
    while True:
        try:
            socket_server = CommunicationServer(host_ip = 12002)
            break
        except Exception as e:
            print(e)
            traceback.print_exc()
            time.sleep(0.1)

    sendAlwaysThread = Thread(
            target=sendAlways,
            args=(),
            daemon=True)
    sendAlwaysThread.start()

    while True:
        print_recv_mess()

def print_recv_mess():
    global socket_server
    if socket_server.isHasNewData():
        try:
            message = json.loads(socket_server.readline())
            print(message)
        except:
            pass

def sendAlways():
    global socket_server
    sequenceID = 0
    while True:
        time.sleep(1)
        if sequenceID < 100:
            sequenceID = sequenceID + 1
        else:
            sequenceID = 0

        messages.heartbeat['heartbeat']['data']['sequenceID'] = sequenceID
        socket_server.sendline(messages.heartbeat)

if __name__ == '__main__':
    main()
