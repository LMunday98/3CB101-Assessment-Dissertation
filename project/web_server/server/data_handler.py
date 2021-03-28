import pickle, json

class DataHandler:
    def __init__(self):
        self.rower_dicts = []
        self.rower_indexes = [0, 1, 2, 3]

        self.seat_labels = ['stroke', 'stroke2', 'bow2', 'bow']
        self.info_labels = ['rower_index', 'seat', 'datetime']
        self.data_labels = ['gx', 'gy', 'gz', 'ax', 'ay', 'az', 'sgx', 'sgy', 'sgz', 'sax', 'say', 'saz', 'rx', 'ry']

        self.setup_data_dicts()

    def setup_data_dicts(self):
        for rower_index in self.rower_indexes:
            info_dict = {}
            data_dict = {}
            for label in self.info_labels:
                info_dict[label] = ''
            for label in self.data_labels:
                data_dict[label] = 0
            rower_dict = {
                'info' : info_dict,
                'data' : data_dict
            }
            self.rower_dicts.append(rower_dict)

    def record_data(self, sent_data):
        decoded_data = pickle.loads(sent_data)
        rower_index = decoded_data.get_rower_index()

        info_dict = decoded_data.get_info_dict()
        data_dict = decoded_data.get_data_dict()

        print('\nInfo dict: ', info_dict)
        print('\nData dict: ', data_dict)

        #self.rower_dicts[rower_index] = sensor_dict
    
    def get_rower_dicts(self):
        return self.rower_dicts

    def get_rower_dict(self, rower_index):
        return self.rower_dicts[rower_index]

    def get_rower_json(self, rower_index):
        rower_dict = self.get_rower_dict(rower_index)
        rower_json = json.dumps(rower_dict)
        return rower_json