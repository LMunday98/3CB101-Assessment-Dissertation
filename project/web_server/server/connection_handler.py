import sys, time, datetime, socket, traceback, select
from data_handler import DataHandler

class ConnectionHandler:

    def __init__(self, server_socket, buffer, socket_ip):
        self.names = []
        self.record = {}
        self.buffer = buffer
        self.connected_list = []
        self.socket_ip = socket_ip
        self.data_handler = DataHandler(socket_ip)
        self.server_socket = server_socket
        self.add_connection(server_socket)

    def add_connection(self, socket):
        self.connected_list.append(socket)

    def remove_connection(self, socket):
        self.connected_list.remove(socket)

    def get_connections(self):
        return self.connected_list

    def get_data_handler(self):
        return self.data_handler
    
    def print_connections(self):
        print("\nconnected_list", self.connected_list)
        print("\nrecord", self.record)
        print("\n")

    def check_connections(self):
        try:
            # Get the list sockets which are ready to be read through select
            rList, wList, error_sockets = select.select(self.connected_list, [], self.connected_list)
            for sock in rList:
                # Check connection against pre-existing ones
                if sock == self.server_socket:
                    self.new_connection(self.server_socket)
                #Some incoming message from a client
                else:
                    # Data from client
                    try:
                        self.recieve_data(sock)
                    #abrupt user exit
                    except Exception:
                        traceback.print_exc()
                        self.disconnect_client(sock)
        except:
            #print("No connections")
            x = 1

    def recieve_data(self, sock):
        recieved_data = sock.recv(self.buffer)
        self.data_handler.record_data(recieved_data)

    def new_connection(self, server_socket):
        # Handle the case in which there is a new connection recieved through server_socket
        name = ""
        sock, addr = server_socket.accept()
        name = sock.recv(self.buffer).decode()
        
        # if repeated username
        # print("name", name)
        # print("names", self.record.values())
        if name in self.record.values():
            self.send_message(sock, "\r\33[31m\33[1m Username already taken!\n\33[0m")
            sock.close()
        else:
            # add name and address
            print("Add name and address")
            self.record[addr] = name
            self.add_connection(sock)
            print ("Client (%s, %s) connected" % addr," [",self.record[addr],"]")

    def disconnect_client(self, sock):
        (i,p)=sock.getpeername()
        print ("Client (%s, %s) is offline (error)" % (i,p)," [",self.record[(i,p)],"]\n")
        del self.record[(i,p)]
        self.remove_connection(sock)
        sock.close()

    def disconnect_all(self, code):
        self.send_to_all(code)
        for connection_index in range(1,len(self.connected_list)):
            sock = self.connected_list[connection_index]
            self.disconnect_client(sock)

    def send_message(self, sock, message):
        try:
            sock.send(message.encode())
        except Exception as e:
            print("Error sending message to\t", sock)
            print("Disconnecting client...")
            self.disconnect_client(sock)
    
    def send_to_all(self, message):
        # print("Send to all", message)
        for connection_index in range(1,len(self.connected_list)):
            sock = self.connected_list[connection_index]
            self.send_message(sock, message)