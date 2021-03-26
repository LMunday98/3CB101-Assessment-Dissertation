import socket, select, string, sys, time, pickle

class ConnectionHandler:

    def __init__(self, client_name):
        self.host = '192.168.0.184'
        self.port = 5001
        self.buffer = 4096
        self.client_name = client_name

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)

        self.open_socket()

    def get_socket(self):
        return self.client_socket

    def open_socket(self):
        while True:
            try :
                self.client_socket.connect((self.host, self.port))
                self.client_socket.send(self.client_name.encode())
                print ("\33[32m\33[1mSuccessfully connected to the server \33[0m")
                break
            except :
                print ("\33[31m\33[1mCan't connect to the server \33[0m")
                #time.sleep(1)
    
    def close_socket(self):
        print("before", self.client_socket)
        self.client_socket.close()
        print("after", self.client_socket)

    def send_message(self, message):
        try:
            self.client_socket.send(message)
        except:
            print ("\n\33[93m\33[1mReconnecting to server \33[0m")
            self.open_socket()

    def connection_listen(self):
        try:
            data = self.client_socket.recv(self.buffer)
            if not data :
                return 0
            else :
                socket_code = data.decode()
                return socket_code
        except Exception as e:
            return 0