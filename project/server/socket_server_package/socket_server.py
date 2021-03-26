import pickle
import time, datetime
import socket, select, traceback
from shutil import copyfile
from socket_server_package.file_handler import FileHandler
from socket_server_package.response_handler import ResponseHandler

import sys
sys.path.append("..")
import mpu

class SocketServer:
    def __init__(self):
        #dictionary to store address corresponding to userself.name
        # List to keep track of socket descriptors
        self.buffer = 4096
        self.port = 5001
        self.file_handler = FileHandler()
        self.response_handler = ResponseHandler()

    def setup(self):
        self.record={}
        self.connected_list = []

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("192.168.0.184", self.port))
        self.server_socket.listen(10) #listen atmost 10 connection at one time

        # Add server socket to the list of readable connections
        self.connected_list.append(self.server_socket)
        self.run_server = True
        self.session_name = datetime.datetime.now()

    #Function to send message to all connected clients
    def send_to_all (self, sock, message):
        #Message not forwarded to server and sender itself
        for socket in self.connected_list:
            if socket != self.server_socket and socket != sock :
                try :
                    socket.send(message.encode())
                except :
                    # if connection not available
                    socket.close()
                    self.connected_list.remove(socket)   

    def run_listen(self):
        print ("\33[32m \t\t\t\tSocket Server Running \33[0m")
        while self.run_server:
            # Get the list sockets which are ready to be read through select
            rList,wList,error_sockets = select.select(self.connected_list,[],[])

            for sock in rList:
                if sock == self.server_socket:
                    self.response_handler.new_connection(self.server_socket, self.record, self.connected_list, self.buffer)

                #Some incoming message from a client
                else:
                    # Data from client
                    try:
                        client_data = sock.recv(self.buffer)
                        try:
                            if client_data.decode() == "disconnect":
                                (i,p)=sock.getpeername()
                                self.send_to_all(sock, "\r\33[31m \33[1m"+self.record[(i,p)].decode()+" left the conversation unexpectedly\33[0m\n")
                                print ("Client (%s, %s) is offline (error)" % (i,p)," [",self.record[(i,p)],"]\n")
                                del self.record[(i,p)]
                                self.connected_list.remove(sock)
                                sock.close()
                                continue
                        except Exception as e:
                            x = 1

                        ### CAPTURE DATA ###
                        rower_data = pickle.loads(client_data)
                        self.capture_data(rower_data)
                            
                    #abrupt user exit
                    except Exception:
                        traceback.print_exc()
                        (i,p)=sock.getpeername()
                        self.send_to_all(sock, "\r\33[31m \33[1m"+self.record[(i,p)].decode()+" left the conversation unexpectedly\33[0m\n")
                        print ("Client (%s, %s) is offline (error)" % (i,p)," [",self.record[(i,p)],"]\n")
                        del self.record[(i,p)]
                        self.connected_list.remove(sock)
                        sock.close()
                        continue

    def capture_data(self, rower_data):
        rower_index = rower_data.get_rowerId()

    def run_calc_timing(self):
        x = 1
            
    def finish(self):
        print("Shutting down socket server")
        self.run_server = False
        try:
            self.server_socket.shutdown()
            self.server_socket.close()
        except Exception as e:
            print(e)
        copyfile("data/realtime_analysis/session_data.csv", "data/captured_analysis/session_data_" + str(self.session_name) + ".csv")

    def get_latest_data(self):
        return self.file_handler.get_csv_to_json()

    def send_message(self, socket_code):
        if socket_code == "session_start":
            print("Start session")
            self.record_session = True
            self.new_session()
        if socket_code == "session_end":
            print("End session")
            copyfile("data/realtime_analysis/session_data.csv", "data/captured_analysis/session_data_" + str(self.session_name) + ".csv")
            self.record_session = False

        for client_index in range(1,len(self.connected_list)):
            client = self.connected_list[client_index]
            client.send(socket_code.encode())