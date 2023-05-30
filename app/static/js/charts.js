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
  height: 365,
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
Plotly.newPlot("piePlot2", data, layout, config);

var data = [
  {
    type: "indicator",
    value: 200,
    delta: { reference: 160 },
    gauge: { axis: { visible: false, range: [0, 250] } },
    domain: { row: 0, column: 0 }
  }
];

var layout = {
  width: 385,
  height: 200,
  margin: { t: 50, b: 25, l: 20, r: 20 },
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
        visible: false,
        range: [-200, 200]
      }
    }
  }
];

var layout = {
  width: 385,
  height: 200,
  margin: { t: 50, b: 50, l: 25, r: 25 },
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
  }
];

var layout = {
  width: 189,
  height: 200,
  margin: { t: 50, b: 25, l: 20, r: 20 },
  template: {
    data: {
      indicator: [
        {
          title: { text: "Adcentism" },
          mode: "number+delta+gauge",
          delta: { reference: 80 }
        }
      ]
    }
  }
};

Plotly.newPlot('indicator3', data, layout, config);

var data = [
  { 
  type: "indicator", 
  mode: "delta", 
  value: 40
  }
];

var layout = {
  width: 189,
  height: 200,
  margin: { t: 50, b: 25, l: 20, r: 20 },
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