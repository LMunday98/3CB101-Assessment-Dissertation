class ResponseHandler:

    def new_connection(self, server_socket, record, connected_list, buffer):
        # Handle the case in which there is a new connection recieved through self.server_socket
        name = ""
        sockfd, addr = server_socket.accept()
        name = sockfd.recv(buffer)
        
        # if repeated username
        if name in record.values():
            sockfd.send("\r\33[31m\33[1m Username already taken!\n\33[0m".encode())
            sockfd.close()
        else:
            # add name and address
            record[addr] = name
            connected_list.append(sockfd)
            print ("Client (%s, %s) connected" % addr," [",record[addr],"]")
            #sockfd.send("\33[32m\r\33[1m Welcome to chat room. Enter 'tata' anytime to exit\n\33[0m".encode())
            #self.send_to_all(sockfd, "\33[32m\33[1m\r "+name.decode()+" joined the conversation \n\33[0m")