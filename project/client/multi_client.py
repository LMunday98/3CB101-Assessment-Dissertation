import socket, select, string, sys
import time
import random
import pickle

class MultiClient:
    def __init__(self, client_name, sensor):

        self.run_client = True
        self.name = str(client_name)
        self.sensor = sensor

        if len(sys.argv)<2:
            # host = input("Enter host ip address: ")
            host = '192.168.0.184'
        else:
            host = sys.argv[1]

        port = 5001
        
        #asks for user name
        # name = input("\33[34m\33[1m CREATING NEW ID:\n Enter username: \33[0m")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)
        
        # connecting host
        try :
            self.s.connect((host, port))
        except :
            print ("\33[31m\33[1m Can't connect to the server \33[0m")
            sys.exit()

        #if connected
        self.s.send(self.name.encode())
        

    def run(self):
        print("name", self.name)
        while self.run_client:
            socket_list = [sys.stdin, self.s]
            # msg = str(random.randint(1,10)) + " "
            data_string = pickle.dumps(self.sensor.get_data())
            self.s.send(data_string)
            time.sleep(.2)

    def finish(self):
        self.s.send("tata ".encode())