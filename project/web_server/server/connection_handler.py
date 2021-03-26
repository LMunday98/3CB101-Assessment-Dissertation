class ConnectionHandler:

    def __init__(self, server_socket, buffer):
        self.record = {}
        self.buffer = buffer
        self.connected_list = []
        self.add_connection(server_socket)

    def add_connection(self, socket):
        self.connected_list.append(socket)

    def remove_connection(self, socket):
        self.connected_list.remove(socket)

    def get_connections(self):
        return self.connected_list

    def new_connection(self, server_socket):
        # Handle the case in which there is a new connection recieved through server_socket
        name = ""
        sock, addr = server_socket.accept()
        name = sock.recv(self.buffer)
        
        # if repeated username
        if name in self.record.values():
            self.send_message(sock, "\r\33[31m\33[1m Username already taken!\n\33[0m")
            sock.close()
        else:
            # add name and address
            self.record[addr] = name
            self.add_connection(sock)
            print ("Client (%s, %s) connected" % addr," [",self.record[addr],"]")

    def disconnect_client(self, sock):
        (i,p)=sock.getpeername()
        print ("Client (%s, %s) is offline (error)" % (i,p)," [",self.record[(i,p)],"]\n")
        del self.record[(i,p)]
        self.remove_connection(sock)
        sock.close()  

    def send_message(self, sock, message):
        sock.send(message.encode())
    
    def send_to_all(self, message):
        for connection_index in range(1,len(self.connected_list)):
            sock = self.connected_list[connection_index]
            self.send_message(sock, message)