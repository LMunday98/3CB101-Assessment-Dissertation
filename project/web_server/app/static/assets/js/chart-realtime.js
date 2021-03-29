function create_chart(data_stream) {

	var chartColors = {
	  red: 'rgb(255, 99, 132)',
	  orange: 'rgb(255, 159, 64)',
	  yellow: 'rgb(255, 205, 86)',
	  green: 'rgb(75, 192, 192)',
	  blue: 'rgb(54, 162, 235)',
	  purple: 'rgb(153, 102, 255)',
	  grey: 'rgb(201, 203, 207)'
	};

	function randomScalingFactor() {
	  return (Math.random() > 0.5 ? 1.0 : -1.0) * Math.round(Math.random() * 100);
	}

	function onRefresh(chart) {
		var rower_index = 0	
	  	chart.config.data.datasets.forEach(function(dataset) {
			dataset.data.push({
		  		x: Date.now(),
		  		y: data_stream.get_data(rower_index)
			});
			rower_index++;
	  	});
	}

	var color = Chart.helpers.color;
	var config = {
	  type: 'line',
	  data: {
		datasets: [{
		  label: 'Stroke',
		  backgroundColor: color(chartColors.blue).alpha(0.5).rgbString(),
		  borderColor: chartColors.blue,
		  fill: false,
		  cubicInterpolationMode: 'monotone',
		  data: []
		}, {
		label: 'Stroke 2',
		backgroundColor: color(chartColors.yellow).alpha(0.5).rgbString(),
		borderColor: chartColors.yellow,
		fill: false,
		cubicInterpolationMode: 'monotone',
		data: []
		}, {
		label: 'Bow 2',
		backgroundColor: color(chartColors.green).alpha(0.5).rgbString(),
		borderColor: chartColors.green,
		fill: false,
		cubicInterpolationMode: 'monotone',
		data: []
		}, {
		label: 'Bow',
		backgroundColor: color(chartColors.red).alpha(0.5).rgbString(),
		borderColor: chartColors.red,
		fill: false,
		cubicInterpolationMode: 'monotone',
		data: []
		}]
	  },
	  options: {
		title: {
		  display: false,
		  text: ''
		},
		scales: {
		  xAxes: [{
			type: 'realtime',
			realtime: {
			  duration: 20000,
			  refresh: 1000,
			  delay: 1000,
			  onRefresh: onRefresh
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
	  var ctx = document.getElementById('realtime_chart').getContext('2d');
	  window.myChart = new Chart(ctx, config);
	};
}

function bind_chart_button(measurement_label) {
	document.getElementById(measurement_label).addEventListener('click', function() {
	  console.log(measurement_label);
	  display_data('chart_label', 'Realtime ' + measurement_label.toUpperCase() + ' Chart');
	  data_stream.set_measurement(measurement_label);
	  destroy_data();
	  });
  }

  function destroy_data() {
	console.log("destroy");
	window.myChart.config.data.datasets.forEach(function(dataset) {
	  dataset.data = [];
	});
  }