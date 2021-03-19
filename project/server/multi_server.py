import socket, select, traceback

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

        self.server_socket.bind(("localhost", port))
        self.server_socket.listen(10) #listen atmost 10 connection at one time

        # Add server socket to the list of readable connections
        self.connected_list.append(self.server_socket)

        print ("\33[32m \t\t\t\tSERVER WORKING \33[0m") 

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

    def run(self):
        while True:
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
                        data1 = sock.recv(self.buffer).decode()
                        #print "sock is: ",sock
                        data=data1[:-1]
                        #print "\ndata received: ",data
                        
                        #get addr of client sending the message
                        i,p=sock.getpeername()
                        clientname = self.record[(i,p)].decode()
                        if data == "tata":
                            msg="\r\33[1m"+"\33[31m "+clientname+" left the conversation \33[0m\n"
                            self.send_to_all(sock,msg)
                            print ("Client (%s, %s) is offline" % (i,p)," [",self.record[(i,p)],"]")
                            del self.record[(i,p)]
                            self.connected_list.remove(sock)
                            sock.close()
                            continue

                        else:
                            print(clientname, data)
                            msg = "\r\33[1m" + "\33[35m " + clientname + ": " + "\33[0m" + data + "\n"
                            self.send_to_all(sock,msg)
                
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

        self.server_socket.close()