class RealtimeChart {
	constructor(chart_id) {
		this.chartColors = this.get_colours();

		var color = Chart.helpers.color;
		var config = {
			type: 'line',
			data: {
				datasets: [{
					label: 'Dataset 1 (linear interpolation)',
					backgroundColor: color(this.chartColors.red).alpha(0.5).rgbString(),
					borderColor: this.chartColors.red,
					fill: false,
					lineTension: 0,
					borderDash: [8, 4],
					data: []
				}, {
					label: 'Dataset 2 (cubic interpolation)',
					backgroundColor: color(this.chartColors.blue).alpha(0.5).rgbString(),
					borderColor: this.chartColors.blue,
					fill: false,
					cubicInterpolationMode: 'monotone',
					data: []
				}]
			},
			options: {
				title: {
					display: true,
					text: 'Line chart (hotizontal scroll) sample'
				},
				scales: {
					xAxes: [{
						type: 'realtime',
						realtime: {
							duration: 20000,
							refresh: 1000,
							delay: 2000,
							onRefresh: this.onRefresh
						}
					}],
					yAxes: [{
						scaleLabel: {
							display: true,
							labelString: 'value'
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

		window.onload = function() {
			var ctx = document.getElementById(chart_id).getContext('2d');
			window.myChart = new Chart(ctx, config);
		};
		
		
		
		
		
		
		this.create_listeners();
		
	}

	get_colours() {
		let chartColors = {
			red: 'rgb(255, 99, 132)',
			orange: 'rgb(255, 159, 64)',
			yellow: 'rgb(255, 205, 86)',
			green: 'rgb(75, 192, 192)',
			blue: 'rgb(54, 162, 235)',
			purple: 'rgb(153, 102, 255)',
			grey: 'rgb(201, 203, 207)'
		};
		return chartColors;
	}

	create_listeners() {
		this.create_listen_randomise()
		this.create_listen_add_dataset()
		this.create_listen_remove_dataset()
		this.create_listen_add_data()
	}

	create_listen_randomise() {
		document.getElementById('randomizeData').addEventListener('click', function() {
			config.data.datasets.forEach(function(dataset) {
				dataset.data.forEach(function(dataObj) {
					dataObj.y = this.randomScalingFactor();
				});
			});
			window.myChart.update();
		});
	}

	create_listen_add_dataset() {
		var colorNames = Object.keys(this.chartColors);
		document.getElementById('addDataset').addEventListener('click', function() {
			var colorName = colorNames[config.data.datasets.length % colorNames.length];
			var newColor = this.chartColors[colorName];
			var newDataset = {
				label: 'Dataset ' + (config.data.datasets.length + 1),
				backgroundColor: color(newColor).alpha(0.5).rgbString(),
				borderColor: newColor,
				fill: false,
				lineTension: 0,
				data: []
			};
		
			config.data.datasets.push(newDataset);
			window.myChart.update();
		});
	}

	create_listen_remove_dataset() {
		document.getElementById('removeDataset').addEventListener('click', function() {
			config.data.datasets.pop();
			window.myChart.update();
		});
	}

	create_listen_add_data() {
		document.getElementById('addData').addEventListener('click', function() {
			this.onRefresh(window.myChart);
			window.myChart.update();
		});
	}

	onRefresh(chart) {
		chart.config.data.datasets.forEach(function(dataset) {
			//var new_y = this.randomScalingFactor();
			var new_y = (Math.random() > 0.5 ? 1.0 : -1.0) * Math.round(Math.random() * 100);
			dataset.data.push({
				x: Date.now(),
				y: new_y
			});
		});
	}

	randomScalingFactor() {
		return (Math.random() > 0.5 ? 1.0 : -1.0) * Math.round(Math.random() * 100);
	}
}