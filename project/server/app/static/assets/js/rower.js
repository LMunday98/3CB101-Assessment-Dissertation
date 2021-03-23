class Rower {
    constructor(seat_name, rower_data) {
        self.seat_name = seat_name;
        self.rower_data = rower_data;
        self.measurements = ["gx", "gy", "gz", "sax", "say", "saz", "rx", "ry"];
    }

    display_all_data() {
        for (let index = 0; index < self.rower_data.length; index++) {
            var data_id = self.seat_name + self.measurements[index];
            let data = Math.round(self.rower_data[index] * 100) / 100;
            self.display_data(data_id, data);
        }
    }

    display_data(element_id, data) {
        html_element = document.getElementById(element_id);
        html_element.innerHTML = data;
    }
  }