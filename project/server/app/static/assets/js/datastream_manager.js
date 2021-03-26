const dataLength = 100;
const seats = ["bow", "bow2", "stroke2", "stroke"];
const measurements = ["gx", "gy", "gz", "sax", "say", "saz", "rx", "ry"];

let charts = gen_charts(dataLength, seats);
let rowers = gen_rowers(seats, charts);

window.onload = function () { 

    var eventSource = new EventSource("/stream"); 
    eventSource.onmessage = function(e) {
    if (e.data == "") {
        display_data("session_satus", "Session: Ended")
        charts = gen_charts(dataLength, seats);
        rowers = gen_rowers(seats, charts);
        clear_table_data();
    } else {
        display_data("session_satus", "Session: In Progress")
        var data_array = e.data.split(',');
        display_data("datetime", get_datetime(data_array));

        rowers.forEach(rower => {
        table_data = data_array.slice(1 + rower.get_offset(), 9 + rower.get_offset());
        rower.set_data(table_data);
        rower.update_table_data();
        rower.update_chart_data();
        });
    }
    };
};

function clear_table_data() {
    seats.forEach(seat_name => {
        measurements.forEach(measurement => {
        var data_id = seat_name + measurement;
        var reset_data = seat_name + " " + measurement;
        display_data(data_id, reset_data)
        });
    });
}

function gen_rowers(seats, charts) {
    let new_rowers = [];
    seats.forEach(seat => {
    new_rowers.push(new Rower(seat, charts));
    });
    return new_rowers;
}

function gen_charts(dataLength, seats) {
    let new_charts = [];
    let chart_rx = new RowerChart("A graph of rx:", "rx", "chartContainer_rx", seats.length, dataLength);
    let chart_ry = new RowerChart("A graph of ry:", "ry", "chartContainer_ry", seats.length, dataLength);
    
    new_charts.push(chart_rx);
    new_charts.push(chart_ry);
    return new_charts;
}

function get_datetime(data_array) {
    timestamp = data_array[data_array.length - 1];
    datetime = timestamp.split('.')[0];
    return datetime;
}

function display_data(element_id, data) {
    html_element = document.getElementById(element_id)
    html_element.innerHTML = data;
}