class DataStream {
    constructor() {
        this.rower_dicts = [];
        this.measurement = 'rx';
    }

    set_measurement(new_measurement) {
        this.measurement = new_measurement;
    }

    get_measurement() {
        return this.measurement;
    }

    get_data(rower_index) {
        var rower_dict = this.rower_dicts[rower_index];
        var data_dict = rower_dict['data'];
        var data = data_dict[this.measurement];
        return data;
    }

    update_data(rower_index, results) {
        this.rower_dicts[rower_index] = results;
    }
}