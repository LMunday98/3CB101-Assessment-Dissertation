import socket, select, string, sys
import time
import random

class MultiClient:
    def __init__(self, client_name):

        self.run_client = True
        self.name = str(client_name)

        if len(sys.argv)<2:
            # host = input("Enter host ip address: ")
            host = 'localhost'
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
            
            # Get the list of sockets which are readable
            rList, wList, error_list = select.select(socket_list , [], [])
            
            for sock in rList:
                #incoming message from server
                if sock == self.s:
                    data = sock.recv(4096)
                    if not data :
                        print ('\33[31m\33[1m \rDISCONNECTED!!\n \33[0m')
                        sys.exit()
                    else :
                        sys.stdout.write(data.decode())

            msg = str(random.randint(1,10)) + " "
            self.s.send(msg.encode())
            time.sleep(.1)

    def finish(self):
        self.s.send("tata ".encode())