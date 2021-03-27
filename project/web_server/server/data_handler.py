import pickle

class DataHandler:

    def __init__(self):
        x=1

    def record_data(self, sent_data):
        decoded_data = pickle.loads(sent_data)
        rower_index = decoded_data.get_rowerId()
        print(rower_index)