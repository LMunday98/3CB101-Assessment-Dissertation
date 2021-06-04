import pickle, json, datetime, sys

class DataHandler:
    def __init__(self, socket_ip):
        print(socket_ip)
        if socket_ip == '192.168.0.184' or socket_ip == '192.168.0.26':
            sys.path.append("../mpu")
        else:
            sys.path.append("/home/pi/Documents/3CB101-Pi/project/mpu")
        from data import Data

        self.socket_ip = socket_ip
        self.session_status = 'end'
        self.rower_dicts = []
        self.rower_indexes = [0, 1, 2, 3]

        self.seat_labels = ['stroke', 'stroke2', 'bow2', 'bow']
        self.data_labels = ['gx', 'gy', 'gz', 'ax', 'ay', 'az', 'sgx', 'sgy', 'sgz', 'sax', 'say', 'saz', 'rx', 'ry']

        self.setup_data_dicts()

    def setup_data_dicts(self):
        for rower_index in self.rower_indexes:
            data_dict = self.populate_dict(self.data_labels)

            info_dict = {
                'rower_index' : rower_index,
                'seat' : self.seat_labels[rower_index],
                'datetime' : 'dd/mm/yyyy hh:mm:ss',
                'ip' : '0.0.0.0'
            }

            rower_dict = {
                'info' : info_dict,
                'data' : data_dict
            }

            self.rower_dicts.append(rower_dict)

    def populate_dict(self, labels):
        new_dict = {}
        for label in labels:
            new_dict[label] = 0
        return new_dict

    def record_data(self, sent_data):
        try:
            decoded_data = pickle.loads(sent_data)

            info_dict = decoded_data.get_info_dict()
            data_dict = decoded_data.get_data_dict()
            rower_index = info_dict['rower_index']
            
            rower_dict = {
                'info' : info_dict,
                'data' : data_dict
            }

            self.rower_dicts[rower_index] = rower_dict
        except Exception as e:
            print(e)
        
    def get_rower_dicts(self):
        return self.rower_dicts

    def get_rower_dict(self, rower_index):
        return self.rower_dicts[rower_index]

    def get_rower_json(self, rower_index):
        rower_dict = self.get_rower_dict(rower_index)
        rower_json = json.dumps(rower_dict)
        return rower_json