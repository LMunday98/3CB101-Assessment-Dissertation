class Rower {
    constructor(seat_name, charts) {
        this.seat_name = seat_name;
        this.charts = charts;

        this.seat_index = this.find_index(seat_name);
        this.offset = this.seat_index * 9; 

        this.measurements = ["gx", "gy", "gz", "sax", "say", "saz", "rx", "ry"];
    }

    set_charts(charts) {
        this.charts = charts;
    }

    get_offset() {
        return this.offset;
    }

    find_index(seat_name) {
        let seat_dict = {
            "bow" : 0,
            "bow2" : 1,
            "stroke2" : 2,
            "stroke" : 3
        }
        return seat_dict[seat_name];
    }

    set_data(new_data) {
        this.rower_data = new_data;
    }

    update_table_data() {
        for (let index = 0; index < this.rower_data.length; index++) {
            var data_id = this.seat_name + this.measurements[index];
            let data = Math.round(this.rower_data[index] * 100) / 100;
            this.display_data(data_id, data);
        }
    }

    update_chart_data() {
        this.charts.forEach(chart => {
            let chart_data = this.rower_data[chart.get_measurement_index()]
            chart.update_chart(this.seat_index, chart_data);
        });
    }

    display_data(element_id, data) {
        html_element = document.getElementById(element_id);
        html_element.innerHTML = data;
    }
  }