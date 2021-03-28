class RealtimeChart {
	constructor(chart_id, chart_name, x_label, y_label) {
		this.chartColors = this.get_colours();

		this.color = Chart.helpers.color;
		this.config = {
			type: 'line',
			data: {
				datasets: [{
					label: 'Dataset 1 (Stroke)',
					backgroundColor: this.color(this.chartColors.red).alpha(0.5).rgbString(),
					borderColor: this.chartColors.red,
					fill: false,
					cubicInterpolationMode: 'monotone',
					data: []
				}/*, {
					label: 'Dataset 2 (Stroke 2)',
					backgroundColor: this.color(this.chartColors.blue).alpha(0.5).rgbString(),
					borderColor: this.chartColors.blue,
					fill: false,
					cubicInterpolationMode: 'monotone',
					data: []
				}, {
					label: 'Dataset 3 (Bow 2)',
					backgroundColor: this.color(this.chartColors.yellow).alpha(0.5).rgbString(),
					borderColor: this.chartColors.yellow,
					fill: false,
					cubicInterpolationMode: 'monotone',
					data: []
				}, {
					label: 'Dataset 4 (Bow)',
					backgroundColor: this.color(this.chartColors.green).alpha(0.5).rgbString(),
					borderColor: this.chartColors.green,
					fill: false,
					cubicInterpolationMode: 'monotone',
					data: []
				}*/]
			},
			options: {
				title: {
					display: true,
					text: chart_name
				},
				scales: {
					xAxes: [{
						type: 'realtime',
						realtime: {
							duration: 20000,
							refresh: 1000,
							delay: 2000,
							onRefresh: this.onRefresh
						},
						scaleLabel: {
							display: true,
							labelString: x_label
						}
					}],
					yAxes: [{
						scaleLabel: {
							display: true,
							labelString: y_label
						}
					}]
				},
				tooltips: {
					mode: 'nearest',
					intersect: false
				},
				hover: {
					mode: 'nearest',
					intersect: false
				}
			}
		};

		this.ctx = document.getElementById(chart_id).getContext('2d');
		
		this.create_listen_randomise();
		this.create_listen_add_dataset();
		this.create_listen_remove_dataset();
		this.create_listen_add_data();
	}

	get_chart_element() {
		return this.ctx;
	}

	get_config() {
		return this.config;
	}

	get_colours() {
		let colours_dict = {
			red: 'rgb(255, 99, 132)',
			orange: 'rgb(255, 159, 64)',
			yellow: 'rgb(255, 205, 86)',
			green: 'rgb(75, 192, 192)',
			blue: 'rgb(54, 162, 235)',
			purple: 'rgb(153, 102, 255)',
			grey: 'rgb(201, 203, 207)'
		};
		return colours_dict;
	}

	create_listen_randomise() {
		document.getElementById('randomizeData').addEventListener('click', function() {
			config.data.datasets.forEach(function(dataset) {
				dataset.data.forEach(function(dataObj) {
					dataObj.y = this.randomScalingFactor();
				});
			});
			this.myChart.update();
		});
	}

	create_listen_add_dataset() {
		var config = this.config;
		var chartColors = this.chartColors;
		var colorNames = Object.keys(this.chartColors);
		var color = this.color;
		document.getElementById('addDataset').addEventListener('click', function() {
			var colorName = colorNames[config.data.datasets.length % colorNames.length];
			var newColor = chartColors[colorName];
			var newDataset = {
				label: 'Dataset ' + (config.data.datasets.length + 1),
				backgroundColor: color(newColor).alpha(0.5).rgbString(),
				borderColor: newColor,
				fill: false,
				lineTension: 0,
				data: []
			};
		
			config.data.datasets.push(newDataset);
			this.myChart.update();
		});
	}

	create_listen_remove_dataset() {
		document.getElementById('removeDataset').addEventListener('click', function() {
			config.data.datasets.pop();
			this.myChart.update();
		});
	}

	create_listen_add_data() {
		document.getElementById('addData').addEventListener('click', function() {
			this.onRefresh(this.myChart);
			this.myChart.update();
		});
	}

	onRefresh(chart) {
		chart.config.data.datasets.forEach(function(dataset) {
			
			var call_url = '/get_data?rower_index=' + '0';
			$.getJSON(call_url, function(results) {
				var info_dict = results['info'];
				var data_dict = results['data'];

				var rx_data = data_dict['rx'];

				var new_y = rx_data;
				dataset.data.push({
					x: Date.now(),
					y: new_y
				});
			} );

		});
	}

	randomScalingFactor() {
		return (Math.random() > 0.5 ? 1.0 : -1.0) * Math.round(Math.random() * 100);
	}
}