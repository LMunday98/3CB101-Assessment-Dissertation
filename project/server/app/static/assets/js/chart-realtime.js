var ctx = document.getElementById('realTimeChart').getContext('2d');

var chart = new Chart(ctx, {

  type: 'line',

  data: {

    datasets: [{

      data: []

    }, {

      data: []

    }]

  },

  options: {

    scales: {

      xAxes: [{

        type: 'realtime'

      }]

    }

  }

});