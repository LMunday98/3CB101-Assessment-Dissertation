import pickle

class DataHandler:

    def __init__(self):
        x=1

    def record_data(self, sent_data):
        decoded_data = pickle.loads(sent_data)
        print(decoded_data)