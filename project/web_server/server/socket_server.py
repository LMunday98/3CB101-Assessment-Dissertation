import sys, time, datetime, socket, traceback, select
from shutil import copyfile
from server.file_handler import FileHandler
from server.connection_handler import ConnectionHandler

sys.path.append("..")
import mpu

class SocketServer:
    def __init__(self):
        self.buffer = 4096
        self.port = 5001
        self.create_socket()
    
    def create_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.server_socket.bind(("192.168.0.184", self.port))
                self.server_socket.listen(10)
                break
            except Exception as e:
                print("Couldnt create socket server")
            time.sleep(1)
        
    def setup(self):
        # Add server socket to the list of readable connections
        self.connection_handler = ConnectionHandler(self.server_socket, self.buffer)

        # Setup server handlers
        self.file_handler = FileHandler()

        # Runtime vars
        self.run_server = True
        self.session_name = datetime.datetime.now()

    def run_listen(self):
        print ("\33[32m \t\t\t\tSocket Server Running \33[0m")
        while self.run_server:
            self.connection_handler.check_connections()
        # Close socket
        try:
            self.connection_handler.disconnect_all()
            self.server_socket.shutdown(socket.SHUT_RDWR)
            self.server_socket.close()
        except Exception as e:
            print(e)

    def run_calc_timing(self):
        x = 1
            
    def finish(self):
        print("Closing socket")
        self.run_server = False
        # copyfile("data/realtime_analysis/session_data.csv", "data/captured_analysis/session_data_" + str(self.session_name) + ".csv")

    def get_latest_data(self):
        return self.file_handler.get_csv_to_json()

    def server_request(self, socket_code):
        if socket_code == "session_start":
            print("Start session")
            self.record_session = True
            self.new_session()
        elif socket_code == "session_end":
            print("End session")
            copyfile("data/realtime_analysis/session_data.csv", "data/captured_analysis/session_data_" + str(self.session_name) + ".csv")
            self.record_session = False
        elif socket_code == "disconnect_all":
            print("Disconnect clients")
            self.connection_handler.disconnect_all(socket_code)
            #self.setup()
        else:
            self.connection_handler.send_to_all(socket_code)