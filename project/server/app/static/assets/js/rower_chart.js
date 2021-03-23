class RowerChart {
    constructor(chart_title, measurement_name, chart_element, num_rowers, num_datapoints) {
        this.chart_title = chart_title;
        this.measurement_index = this.find_measurement_index(measurement_name);
        this.num_datapoints = num_datapoints;

        this.x_val = 0;
        this.dps = this.setup_datapoints(num_rowers);
        this.chart_data = this.setup_chartdata(num_rowers);

        this.chart = new CanvasJS.Chart(chart_element, {
            title :{
              text: chart_title
            },
            data: this.chart_data
          });
    }

    get_measurement_index() {
        return this.measurement_index;
    }

    setup_datapoints(num_rowers) {
        let dps = [];
        for (let index = 0; index < num_rowers; index++) {
            dps.push([]);
        }
        return dps;
    }

    setup_chartdata(num_rowers) {
        let data = [];
        for (let index = 0; index < num_rowers; index++) {
            data.push({
                type: "line",
                dataPoints: this.dps[index]
            });
        }
        return data;
    }

    update_chart(rower_index, new_y) {
        this.add_coords(this.dps[rower_index], this.x_val, parseInt(new_y));
        this.shift_coords(this.dps[rower_index], this.num_datapoints);
        this.chart.render();
        this.x_val++;
    }

    add_coords(coords_array, x_val, y_val) {
        coords_array.push({
            x: x_val,
            y: y_val
        });
    }
  
    shift_coords(coords_array, data_length) {
        if (coords_array.length > data_length) {
            coords_array.shift();
        }
    }

    find_measurement_index(measurement_name) {
        let measurement_dict = {
        "gx" : 0,
        "gy" : 1,
        "gz" : 2,
        "sax" : 3,
        "say" : 4,
        "saz" : 5,
        "rx" : 6,
        "ry" : 7,
        }
        return measurement_dict[measurement_name]
    }
}