class ResponseHandler:

    def __init__(self, buffer):
        self.record = {}
        self.buffer = buffer

    def new_connection(self, server_socket, connected_list):
        # Handle the case in which there is a new connection recieved through server_socket
        name = ""
        sockfd, addr = server_socket.accept()
        name = sockfd.recv(self.buffer)
        
        # if repeated username
        if name in self.record.values():
            sockfd.send("\r\33[31m\33[1m Username already taken!\n\33[0m".encode())
            sockfd.close()
        else:
            # add name and address
            self.record[addr] = name
            connected_list.append(sockfd)
            print ("Client (%s, %s) connected" % addr," [",self.record[addr],"]")

    def disconnect_client(self, sock, connected_list):
        (i,p)=sock.getpeername()
        print ("Client (%s, %s) is offline (error)" % (i,p)," [",self.record[(i,p)],"]\n")
        del self.record[(i,p)]
        connected_list.remove(sock)
        sock.close()  