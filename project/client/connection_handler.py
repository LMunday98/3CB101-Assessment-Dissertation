import socket, select, string, sys, time, pickle

class ConnectionHandler:

    def __init__(self, client_name):
        self.client_name = client_name
        self.host = "192.168.0.185"
        self.port = 5001
        self.buffer = 4096
        self.is_connected = False

    def socket_create(self):
        print ("\33[93m\33[1mCreate socket \33[0m")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)

    def socket_connect(self):
        while True:
            try :
                print ("\33[93m\33[1mConnecting to server \33[0m")
                self.client_socket.connect((self.host, self.port))
                print ("\33[32m\33[1mConnected to server \33[0m")
                self.is_connected = True
                break
            except :
                print ("\33[31m\33[1mCan't connect to the server \33[0m")
                time.sleep(1)
        # if connceted, send client name to server
        self.socket_send(self.client_name.encode())

    def socket_reconnect(self):
        #self.socket_close()

        self.socket_create()
        self.socket_connect()

    def socket_close(self):
        print ("\33[31m\33[1m Shutting down socket \33[0m")
        try:
            self.client_socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print (e)
        print ("\33[31m\33[1m Closing socket \33[0m")
        try:
            self.client_socket.close()
        except Exception as e:
            print (e)
        self.is_connected = False;

    def socket_send(self, data):
        self.client_socket.send(data)

    def connection_listen(self):
        try:
            data = self.client_socket.recv(self.buffer)
            if not data :
                print ("\33[31m\33[1mCan't connect to the server \33[0m")
                self.is_connected = False
                self.socket_reconnect()
                return 0
            else :
                socket_code = data.decode()
                return socket_code
        except Exception as e:
            return 0

    def check_connection(self):
        return self.is_connected