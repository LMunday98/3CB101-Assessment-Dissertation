class Datastream {
    constructor(stream_url) {



        var seats = ["bow", "bow2", "stroke2", "stroke"]
        var sensor_points = ["gx", "gy", "gz", "sax", "say", "saz", "rx", "ry"]
        
        var eventSource = new EventSource(stream_url)
            eventSource.onmessage = function(e) {
            var data_array = e.data.split(',');
            
            var num_rowers = (data_array.length - 1) / 9
            var rower_ids = []

            for (let index = 0; index < num_rowers; index++) {
            rower_id = data_array[index * 9]
            rower_ids.push(rower_id)
            }

            timestamp = data_array[data_array.length - 1]
            datetime = timestamp.split('.')[0]
            display_data("datetime", datetime)

            rower_index = 0
            rower_ids.forEach(rower_index => {
            seat_name = seats[rower_index]
            var sensor_count = 1
            sensor_points.forEach(sensor_point => {
                var data_id = seat_name + sensor_point
                data_index = (rower_index * 9) + sensor_count
                data = data_array[data_index]
                data = Math.round(data * 100) / 100
                display_data(data_id, data)
                sensor_count++
            });
            sensor_index = get_sensor_index("rx")
            data_to_plot = data_array[(rower_index * 9) + sensor_index]
            chart_rx.update_chart(rower_index, data_to_plot);

            sensor_index = get_sensor_index("ry")
            data_to_plot = data_array[(rower_index * 9) + sensor_index]
            chart_ry.update_chart(rower_index, data_to_plot);

            rower_index++
            });
        };

        function get_sensor_index(sensor_name) {
            sensor_dict = {
            "gx" : 1,
            "gy" : 2,
            "gz" : 3,
            "sax" : 4,
            "say" : 5,
            "saz" : 6,
            "rx" : 7,
            "ry" : 8,
            }
            return sensor_dict[sensor_name]
        }

        function display_data(element_id, data) {
            html_element = document.getElementById(element_id)
            html_element.innerHTML = data;
        }
    } 
}