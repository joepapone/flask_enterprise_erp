var country = ["Italy", "France", "Spain", "USA", "Argentina"];
var value = [55, 49, 44, 24, 15];

// Bar Chart
new Chart(document.getElementById("BarChart"), {
    type: 'bar',
    data: {
        labels: country,
        datasets: [
        {
            label: "Population (millions)",
            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
            data: value
        }
        ]
    },
    options: {
        legend: { display: false },
        title: {
        display: true,
        text: 'Total Confirmed Cases of COVID in May'
        }
    }
});

// Doughnut Chart

const doughnut_data = {
    labels: [
      'Red',
      'Blue',
      'Yellow'
    ],
    datasets: [{
      label: ['My First Dataset'],
      data: [300, 50, 100],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    }]
  };

const options = {
    options: {
        rotation: 0,
        circumference: 180,
      }
  };


const doughnut_config = {
    type: 'doughnut',
    data: doughnut_data,
    options: {
      responsive: true,
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Doughnut Chart'
      }
    }
  };

new Chart(document.getElementById("DoughnutChart"), doughnut_config);

// Doughnut Chart
const halfdoughnut_config = {
    type: 'doughnut',
    data: doughnut_data,
    options: {
      responsive: true,
      rotation: 1 * Math.PI,
      circumference: 1 * Math.PI,
      title: {
        display: true,
        text: 'Title',
        font: {size: 20}
      },
      elements: {
        center: {
          text: '100%',
          color: '#FF6384', // Default is #000000
          fontStyle: 'Arial', // Default is Arial
          sidePadding: 20, // Default is 20 (as a percentage)
          minFontSize: 25, // Default is 20 (in px), set to false and text will not wrap.
          lineHeight: 25 // Default is 25 (in px), used for when text wraps
        }
      },
      legend: { 
        display: true,
        position: 'bottom'}
    }
  };



var test_config = {
  type: 'doughnut',
  data: {
    labels: [
      "Red",
      "Green",
      "Yellow"
    ],
    datasets: [{
      data: [300, 50, 100],
      backgroundColor: [
        "#FF6384",
        "#36A2EB",
        "#FFCE56"
      ],
      hoverBackgroundColor: [
        "#FF6384",
        "#36A2EB",
        "#FFCE56"
      ]
    }]
  },
  options: {
    elements: {
      center: {
        text: 'Red is 2/3 of the total numbers',
        color: '#FF6384', // Default is #000000
        fontStyle: 'Arial', // Default is Arial
        sidePadding: 20, // Default is 20 (as a percentage)
        minFontSize: 25, // Default is 20 (in px), set to false and text will not wrap.
        lineHeight: 25 // Default is 25 (in px), used for when text wraps
      }
    }
  }
};

new Chart(document.getElementById("HalfDoughnutChart"), halfdoughnut_config);

// Line Chart

//const labels = Utils.months({count: 7});
const labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul']
const linedata = {
  labels: labels,
  datasets: [{
    label: 'My First Dataset',
    data: [65, 59, 80, 81, 56, 55, 40],
    fill: false,
    borderColor: 'rgb(75, 192, 192)',
    tension: 0.1
  }]
};

new Chart(document.getElementById("LineChart"), {
    type: 'line',
    data: linedata,
});

// Plotly Chart Configurtion
var config = {
  displayModeBar: false,
  responsive: true
}

// Plotly Line Chart
var exp = "x + 17";

// Generate values
var xValues = [];
var yValues = [];
for (var x = 0; x <= 10; x += 1) {
  yValues.push(eval(exp));
  xValues.push(x);
}

// Define Data
var data = [{
  x: xValues,
  y: yValues,
  mode: "lines"
}];

// Define Layout
var layout = {
  title: "World Wide Wine Production",
  annotations: [
    {
      font: {
        size: 20
      },
      showarrow: false,
      text: 'GHG',
      x: 0.50,
      y: 0.5
    }]
  };

// Display using Plotly
Plotly.newPlot("linePlot", data, layout, config);

// Plotly Bar Chart
var xArray = ["Italy","France","Spain","USA","Argentina"];
var yArray = [55, 49, 44, 24, 15];

var data = [{
  x: xArray,
  y: yArray,
  type: "bar"  }];

Plotly.newPlot("barPlot", data, layout, config);

// Plotly Pie Chart
var data = [{
  labels: xArray,
  values: yArray,
  hole: .6,
  type: "pie",
  textinfo: "label+percent",
  textposition: "outside",
  automargin: true
}];

Plotly.newPlot("piePlot", data, layout, config);

var data = [
  {
    type: "indicator",
    value: 200,
    delta: { reference: 160 },
    gauge: { axis: { visible: false, range: [0, 250] } },
    domain: { row: 0, column: 0 }
  },
  {
    type: "indicator",
    value: 120,
    gauge: {
      shape: "bullet",
      axis: {
        visible: false,
        range: [-200, 200]
      }
    },
    domain: { x: [0.1, 0.5], y: [0.15, 0.35] }
  },
  {
    type: "indicator",
    mode: "number+delta",
    value: 300,
    domain: { row: 0, column: 1 }
  },
  { type: "indicator", mode: "delta", value: 40, domain: { row: 1, column: 1 } }
];

var layout = {
  width: 600,
  height: 400,
  margin: { t: 25, b: 25, l: 25, r: 25 },
  grid: { rows: 2, columns: 2, pattern: "independent" },
  template: {
    data: {
      indicator: [
        {
          title: { text: "Speed" },
          mode: "number+delta+gauge",
          delta: { reference: 90 }
        }
      ]
    }
  }
};

Plotly.newPlot('myDiv', data, layout, config);




var data1 = {
  // A labels array that can contain any sort of values
  labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
  // Our series array that contains series objects or in this case series data arrays
  series: [
    [5, 2, 4, 2, 0]
  ]
};

// As options we currently only set a static size of 300x200 px. We can also omit this and use aspect ratio containers
// as you saw in the previous example
var options1 = {
  width: 300,
  height: 200
};

// Create a new line chart object where as first parameter we pass in a selector
// that is resolving to our chart container element. The Second parameter
// is the actual data object. As a third parameter we pass in our custom options.
new Chartist.Line('.ct-chart1', data1, options1);


var data2 = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    series: [
    [5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8],
    [3, 2, 9, 5, 4, 6, 4, 6, 7, 8, 7, 4]
  ]
};

var options2 = {
  seriesBarDistance: 15
};

var responsiveOptions2 = [
  ['screen and (min-width: 641px) and (max-width: 1024px)', {
    seriesBarDistance: 10,
    axisX: {
      labelInterpolationFnc: function (value) {
        return value;
      }
    }
  }],
  ['screen and (max-width: 640px)', {
    seriesBarDistance: 5,
    axisX: {
      labelInterpolationFnc: function (value) {
        return value[0];
      }
    }
  }]
];

new Chartist.Bar('.ct-chart2', data2, options2, responsiveOptions2);


new Chartist.Pie('.ct-chart3', {
  series: [20, 10, 30, 40]
}, {
  donut: true,
  donutWidth: 60,
  startAngle: 270,
  total: 200,
  showLabel: true
});


new Chartist.Bar('.ct-chart4', {
  labels: ['Q1', 'Q2', 'Q3', 'Q4'],
  series: [
    [800000, 1200000, 1400000, 1300000],
    [200000, 400000, 500000, 300000],
    [100000, 200000, 400000, 600000]
  ]
}, {
  stackBars: true,
  axisY: {
    labelInterpolationFnc: function(value) {
      return (value / 1000) + 'k';
    }
  }
}).on('draw', function(data) {
  if(data.type === 'bar') {
    data.element.attr({
      style: 'stroke-width: 30px'
    });
  }
});


function mytime() {
    let d = new Date();
    return document.body.innerHTML = "<h1>Today's date is " + d + "</h1>"
}

TESTER = document.getElementById('tester');
Plotly.newPlot( TESTER, [{
x: [1, 2, 3, 4, 5],
y: [1, 2, 4, 8, 16] }], {
margin: { t: 0 } } );

