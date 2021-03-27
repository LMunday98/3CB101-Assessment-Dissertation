import pickle

class DataHandler:
    def record_data(self, sent_data):
        decoded_data = pickle.loads(sent_data)
        rower_index = decoded_data.get_rowerId()
        print(rower_index)