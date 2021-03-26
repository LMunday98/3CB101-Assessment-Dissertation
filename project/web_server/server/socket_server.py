import pickle
import time, datetime
import socket, select, traceback
from shutil import copyfile
from server.file_handler import FileHandler
from server.connection_handler import ConnectionHandler

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
        
    def setup(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("192.168.0.184", self.port))
        self.server_socket.listen(10) #listen atmost 10 connection at one time

        # Add server socket to the list of readable connections
        self.connection_handler = ConnectionHandler(self.server_socket, self.buffer)

        # Runtime vars
        self.run_server = True
        self.session_name = datetime.datetime.now()

    def run_listen(self):
        print ("\33[32m \t\t\t\tSocket Server Running \33[0m")
        while self.run_server:
            # Get the list sockets which are ready to be read through select
            current_connections = self.connection_handler.get_connections()
            rList,wList,error_sockets = select.select(current_connections,[],[])

            for sock in rList:
                if sock == self.server_socket:
                    self.connection_handler.new_connection(self.server_socket)
                    continue
                #Some incoming message from a client
                else:
                    # Data from client
                    try:
                        client_data = sock.recv(self.buffer)
                        try:
                            if client_data.decode() == "disconnect":
                                self.connection_handler.disconnect_client(sock)
                                continue
                        except Exception as e:
                            x = 1

                        ### CAPTURE DATA ###
                        rower_data = pickle.loads(client_data)
                        self.capture_data(rower_data)
                            
                    #abrupt user exit
                    except Exception:
                        traceback.print_exc()
                        self.connection_handler.disconnect_client(sock)
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

        self.connection_handler(socket_code)