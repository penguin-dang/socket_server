import socket
import time
import json
from queue import Queue
from threading import Thread

class CommunicationServer():
    def __init__(self, host_ip = 12002):
        self.host_ip = host_ip 

        self.__data_line = ''
        self.conn_status = 'not_connected'

        self.__init_socket(self.host_ip)

        self.__communicat_queue = Queue()
        self.__communicate_thread = Thread(
                target = self.__communicate,
                args=())
        self.__communicate_thread.daemon = True
        self.__communicate_thread.start()

    def __init_socket(self, host_ip):
        self.conn = None
        self.addr = None    
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.setblocking(0)
        self.server_address=('', host_ip)
        self.serversocket.bind(self.server_address)

        self.prev_conn_status = self.conn_status
 
        self.serversocket.listen(10)
        print('done init socket')

    def get_conn_status(self):
        return self.conn_status

    def server_socket_close(self):
        self.serversocket.shutdown(socket.SHUT_RDWR)
        self.serversocket.close()

    def sendline(self, data):
        try:
            data = self.__json_output(data)
            self.__sendline_socket(data)
            return True
        except:
            self.__handle_connection_failure()
            return False

    def readline(self):
        return self.__communicat_queue.get()

    def isHasNewData(self):
        return not self.__communicat_queue.empty()

    def __handle_connection_receive_data(self, data_line):
        self.__communicat_queue.put(data_line)
    
    def __json_output(self, send_string={}):
        data_json = json.dumps(send_string) 
        return data_json

    def __accept_connection(self):
        self.conn, self.addr = self.serversocket.accept()
        self.conn.settimeout(2)

    def __handle_connection_failure(self):
        if self.conn != None:
            self.conn.close()
            self.conn_status = 'not connected'
            self.conn = None

    def __readline_socket(self):
        data = self.conn.recv(1)

        data= data.decode()
        if data != "\n":
            self.__data_line += data
            self.conn_status = 'connected'
            self.prev_conn_status = self.conn_status
            return None
        else:
            ret = self.__data_line
            self.__data_line = ''
            return ret

    def __sendline_socket(self, data):
        data = str(data)+"\r\n" #"\r\n" : end of line
        encoded_data = data.encode()
        self.conn.send(encoded_data)

    def __handle_connection(self):
        while True:
            try:
                data_line = self.__readline_socket()
            except:
                self.__handle_connection_failure()
                return False

            if data_line != None:
                self.__handle_connection_receive_data(data_line)

    def __communicate(self):
        while True:
            try:
                self.__accept_connection()
            except BlockingIOError:
                time.sleep(0.1)
                continue
    
            print("Receving data")
            self.__handle_connection()

            print("3- Done reiceive data")
            time.sleep(0.1)
