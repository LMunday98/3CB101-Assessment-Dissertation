class ResponseHandler:

    def new_connection(self, server_socket, record, connected_list, buffer):
        # Handle the case in which there is a new connection recieved through server_socket
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

    def disconnect_client(self, sock, record, connected_list):
        (i,p)=sock.getpeername()
        print ("Client (%s, %s) is offline (error)" % (i,p)," [",record[(i,p)],"]\n")
        del record[(i,p)]
        connected_list.remove(sock)
        sock.close()