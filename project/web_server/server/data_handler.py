import pickle

class DataHandler:

    def __init__(self, connection_handler):
        self.connection_handler = connection_handler

    def record_data(self, sent_data):
        decoded_data = pickle.loads(sent_data)
        #print(decoded_data)