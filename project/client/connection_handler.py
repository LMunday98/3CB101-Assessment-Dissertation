import socket, select, string, sys, time, pickle

class ConnectionHandler:

    def __init__(self, client_name):
        self.client_name = client_name
        self.host = "192.168.0.184"
        self.port = 5001
        self.buffer = 4096

    def socket_create(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)

    def socket_connect(self):
        while True:
            try :
                self.client_socket.connect((self.host, self.port))
                break
            except :
                print ("\33[31m\33[1m Can't connect to the server \33[0m")
        # if connceted, send client name to server
        self.socket_send(self.client_name)

    def socket_send(self, data):
        self.client_socket.send(data.encode())