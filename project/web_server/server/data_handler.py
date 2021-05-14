import pickle, json, datetime, sys

class DataHandler:
    def __init__(self, socket_ip):
        if socket_ip == '192.168.0.184':
            sys.path.append("../mpu")
        else:
            sys.path.append("/home/pi/Documents/3CB101-Pi/project/mpu")
        from data import Data

        self.socket_ip = socket_ip
        self.rower_dicts = []
        self.rower_indexes = [0, 1, 2, 3]

        self.seat_labels = ['stroke', 'stroke2', 'bow2', 'bow']
        self.info_labels = ['rower_index', 'seat', 'datetime']
        self.data_labels = ['gx', 'gy', 'gz', 'ax', 'ay', 'az', 'sgx', 'sgy', 'sgz', 'sax', 'say', 'saz', 'rx', 'ry']

        self.setup_data_dicts()

    def setup_data_dicts(self):
        for rower_index in self.rower_indexes:
            data_dict = self.populate_dict(self.data_labels, 0)

            info_dict = {
                'rower_index' : rower_index,
                'seat' : self.seat_labels[rower_index],
                'datetime' : str(datetime.datetime.now())
            }

            rower_dict = {
                'info' : info_dict,
                'data' : data_dict
            }

            self.rower_dicts.append(rower_dict)

    def populate_dict(self, labels, inital_value):
        new_dict = {}
        for label in labels:
            new_dict[label] = inital_value
        return new_dict

    def record_data(self, sent_data):
        decoded_data = pickle.loads(sent_data)
        rower_index = decoded_data.get_rower_index()

        info_dict = decoded_data.get_info_dict()
        data_dict = decoded_data.get_data_dict()
        
        rower_dict = {
            'info' : info_dict,
            'data' : data_dict
        }

        self.rower_dicts[rower_index] = rower_dict
    
    def get_rower_dicts(self):
        return self.rower_dicts

    def get_rower_dict(self, rower_index):
        return self.rower_dicts[rower_index]

    def get_rower_json(self, rower_index):
        rower_dict = self.get_rower_dict(rower_index)
        rower_json = json.dumps(rower_dict)
        return rower_json