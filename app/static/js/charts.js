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
  width: 385,
  height: 360,
  title: '<b>Number of Employees</b><br><span style="font-size: 25"><b>630</b></span>',
  annotations: [
    {
      font: {
        size: 20
      },
      showarrow: false,
      text: 'GHG',
      x: 0.5,
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
Plotly.newPlot("piePlot2", data, layout, config);

var data = [
  {
    type: "indicator",
    value: 200,
    delta: { reference: 160 },
    gauge: { axis: { visible: true, range: [0, 250] } },
    domain: { x: [0.1, 0.9], y: [0, 1] },
    title: { text: "Speed" }
  }
];

var layout = {
  width: 385,
  height: 200,
  margin: { t: 50, b: 20, l: 20, r: 20 },
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

Plotly.newPlot('indicator1', data, layout, config);

var data = [
  {
    type: "indicator",
    value: 120,
    gauge: {
      shape: "bullet",
      axis: {
        visible: true,
        range: [-200, 200]
      }
    },
    domain: { x: [0.15, 1], y: [0.35, 0.65] },
    title: { text: "Profit" }
  }
];

var layout = {
  width: 385,
  height: 200,
  margin: { t: 20, b: 20, l: 20, r: 20 },
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

Plotly.newPlot('indicator2', data, layout, config);

var data = [
  {
    type: "indicator",
    mode: "number+delta",
    value: 300,
    domain: { row: 0, column: 0 },
    title: { text: "Accelaration" }
  },
  { 
    type: "indicator", 
    mode: "delta", 
    value: 40,
    domain: { row: 0, column: 1 },
    title: { text: "Velocity" }
  }
];

var layout = {
  autosize: false,
  width: 385,
  height: 200,
  margin: { t: 50, b: 25, l: 20, r: 20 },
  grid: { rows: 1, columns: 2, pattern: "independent" },
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

Plotly.newPlot('indicator4', data, layout, config);