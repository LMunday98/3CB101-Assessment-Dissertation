import pickle
import time, datetime
import socket, select, traceback
from shutil import copyfile
from flask import stream_with_context

import sys
sys.path.append("..")
import mpu

class MultiServer:
    def __init__(self):
        self.name=""
        #dictionary to store address corresponding to userself.name
        self.record={}
        # List to keep track of socket descriptors
        self.connected_list = []
        self.buffer = 4096
        self.port = 5001

    def setup(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.bind(("192.168.0.184", self.port))
        self.server_socket.listen(10) #listen atmost 10 connection at one time

        # Add server socket to the list of readable connections
        self.connected_list.append(self.server_socket)

        self.run_server = True

        self.session_name = datetime.datetime.now()

        self.new_session()

        self.test_string = "TEST STRING"


    def reset(self):
        self.logged_data = [
        self.create_clean_data_array(),
        self.create_clean_data_array(),
        self.create_clean_data_array(),
        self.create_clean_data_array()]

    def create_clean_data_array(self):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def new_session(self):
        self.write_rower_data("realtime_analysis", "/session_data", ["Rower Id", "gx", "gy", "gz", "sax", "say", "saz", "rx", "ry", "Rower Id", "gx", "gy", "gz", "sax", "say", "saz", "rx", "ry", "Rower Id", "gx", "gy", "gz", "sax", "say", "saz", "rx", "ry", "Rower Id", "gx", "gy", "gz", "sax", "say", "saz", "rx", "ry", "Timestamp"], "w")
        self.reset()

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
        print ("\33[32m \t\t\t\tSOCKET SERVER WORKING \33[0m")
        while self.run_server:
            # Get the list sockets which are ready to be read through select
            rList,wList,error_sockets = select.select(self.connected_list,[],[])

            for sock in rList:
                #New connection
                if sock == self.server_socket:
                    # Handle the case in which there is a new connection recieved through self.server_socket
                    sockfd, addr = self.server_socket.accept()
                    self.name=sockfd.recv(self.buffer)
                    self.connected_list.append(sockfd)
                    self.record[addr]=""
                    #print "self.record and conn list ",self.record,self.connected_list
                    
                    #if repeated userself.name
                    if self.name in self.record.values():
                        sockfd.send("\r\33[31m\33[1m Username already taken!\n\33[0m".encode())
                        del self.record[addr]
                        self.connected_list.remove(sockfd)
                        sockfd.close()
                        continue
                    else:
                        #add name and address
                        self.record[addr]=self.name
                        print ("Client (%s, %s) connected" % addr," [",self.record[addr],"]")
                        sockfd.send("\33[32m\r\33[1m Welcome to chat room. Enter 'tata' anytime to exit\n\33[0m".encode())
                        self.send_to_all(sockfd, "\33[32m\33[1m\r "+self.name.decode()+" joined the conversation \n\33[0m")

                #Some incoming message from a client
                else:
                    # Data from client
                    try:
                        client_data = sock.recv(self.buffer)
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
        self.server_socket.shutdown()
        self.server_socket.close()

    def capture_data(self, rower_data):
        rower_index = rower_data.get_rowerId()
        logged_data = self.logged_data[rower_index]
        logged_data[0] = logged_data[0] + 1

        data_index = 1
        for data in rower_data.get_sensor_data():
            logged_data[data_index] = logged_data[data_index] + data
            data_index += 1

        self.write_rower_data("rower" + str(rower_data.get_rowerId()), "/session_data_" + str(self.session_name) ,rower_data.get_all_data())

    def write_rower_data(self, file_dir, file_name, data_to_write, file_method="a"):
        f = open("data/" + file_dir + file_name + ".csv", file_method)
        data_string = "\n"
        if file_method == "w":
            data_string = ""
        for data in data_to_write:
            data_string = data_string + str(data) + ","
        data_string = data_string[:-1]
        f.write(data_string)
        f.close()

    def run_calc_timing(self):
        while self.run_server:
            time.sleep(0.5)
            logged_data = self.logged_data

            data_array = []
            rower_index = 0
            for rower_data in logged_data:
                num_data_logs = rower_data[0]

                data_array.append(rower_index)
                
                if num_data_logs == 0:
                    for data_index in range(8):
                        data_array.append(0)
                else:
                    for data_index in range(1,9):
                        avg_data = rower_data[data_index] / num_data_logs
                        data_array.append(avg_data)
                
                rower_index += 1
                
            if len(data_array) != 0:
                data_array.append(datetime.datetime.now())
                self.write_rower_data("realtime_analysis", "/session_data", data_array)
            self.reset()
            
    def finish(self):
        self.run_server = False
        copyfile("data/realtime_analysis/session_data.csv", "data/captured_analysis/session_data_" + str(self.session_name) + ".csv")

    def read_boat_data(self):
        f1 = open("data/realtime_analysis/session_data.csv", "r")
        last_line = f1.readlines()[-1]
        f1.close()
        row = last_line.split(',')
        return row

    def get_data_string(self):
        data_array = self.read_boat_data()
        data_string = ','.join(data_array)
        return data_string

    @stream_with_context
    def get_stream(self):
        while True:
            time.sleep(.2)
            yield 'data: %s\n\n' % (self.get_data_string())