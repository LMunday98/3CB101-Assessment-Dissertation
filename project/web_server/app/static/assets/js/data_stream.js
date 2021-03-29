class DataStream {
    constructor() {
        this.rower_dicts = [];
    }

    get_data(rower_index) {
        var rower_dict = this.rower_dicts[rower_index];
        var data_dict = rower_dict['data'];
        var data = data_dict['rx'];
        return data;
    }

    update_data(rower_index, results) {
        this.rower_dicts[rower_index] = results;
    }
}