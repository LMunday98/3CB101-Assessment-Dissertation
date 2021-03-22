import pickle
import time, datetime
import socket, select, traceback
from shutil import copyfile

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
        port = 5001

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.bind(("192.168.0.184", port))
        self.server_socket.listen(10) #listen atmost 10 connection at one time

        # Add server socket to the list of readable connections
        self.connected_list.append(self.server_socket)

        self.run_server = True

        self.reset()

        self.session_name = datetime.datetime.now()

        self.new_session()

        print ("\33[32m \t\t\t\tSERVER WORKING \33[0m")

    def reset(self):
        self.rower0 = []
        self.rower1 = []
        self.rower2 = []
        self.rower3 = []

    def new_session(self):
        self.write_rower_data("realtime_analysis", "/session_data", [], "w")

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
                        sensor_data = pickle.loads(client_data)
                        self.write_rower_data("rower" + str(sensor_data.get_rowerId()), "/session_data_" + str(self.session_name) ,sensor_data.get_all_data())
                
                    #abrupt user exit
                    except Exception:
                        # traceback.print_exc()
                        (i,p)=sock.getpeername()
                        self.send_to_all(sock, "\r\33[31m \33[1m"+self.record[(i,p)].decode()+" left the conversation unexpectedly\33[0m\n")
                        print ("Client (%s, %s) is offline (error)" % (i,p)," [",self.record[(i,p)],"]\n")
                        del self.record[(i,p)]
                        self.connected_list.remove(sock)
                        sock.close()
                        continue
        self.server_socket.shutdown()
        self.server_socket.close()

    def write_rower_data(self, file_dir, file_name, data_to_write, file_method="a"):
        f = open("data/" + file_dir + file_name + ".csv", file_method)
        data_string = "\n"
        for data in data_to_write:
            data_string = data_string + str(data) + ","
        data_string = data_string[:-1]
        f.write(data_string)
        f.close()

    def run_calc_timing(self):
        while self.run_server:
            time.sleep(0.5)
            data_to_write = ["yeet"]
            self.write_rower_data("realtime_analysis", "/session_data", data_to_write)
            self.reset()
            
    def finish(self):
        self.run_server = False
        copyfile("data/realtime_analysis/session_data.csv", "data/captured_analysis/session_data_" + str(self.session_name) + ".csv")