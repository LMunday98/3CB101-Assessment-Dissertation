class RowerChart {
    constructor(chart_title, num_rowers, num_datapoints) {
        this.chart_title = chart_title;
        this.num_datapoints = num_datapoints;

        this.dps = this.setup_datapoints(num_rowers);
        this.chart_data = this.setup_chartdata(num_rowers);

        console.log(this.dps);
        console.log(this.chart_data);
    }

    setup_datapoints(num_rowers) {
        let dps = [];
        for (let index = 0; index < 4; index++) {
            dps.push([]);
        }
        return dps;
    }

    setup_chartdata(num_rowers) {
        let data = [];
        for (let index = 0; index < 4; index++) {
            data.push({
                type: "line",
                dataPoints: this.dps[index]
              });
        }
        return data;
    }
}