import socket, select, string, sys, time, pickle

class ConnectionHandler:

    def __init__(self, client_name):
        self.client_name = client_name