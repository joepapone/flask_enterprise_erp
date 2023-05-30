# Plotly Chart Configurtion
config = {
    'displayModeBar': False,
    'responsive': True
}


line_data = {
    'x': [50,60,70,80,90,100,110,120,130,140,150],
    'y': [7,8,8,9,9,9,10,11,14,14,15],
    'mode': 'lines'
}

# Plot line chart
def line_chart():

    # Define data traces
    data = [line_data]

    # Define Layout
    layout = {
        'width': 385,
        'height': 365,
        'title': "Line chart example",
        'xaxis': {'range': [40, 160], 'title': 'Square Meters'},
        'yaxis': {'range': [5, 16], 'title': 'Price in Millions'},  
        'annotations': [
            {
            'font': {'size': 20},
            'showarrow': False,
            'text': 'GHG',
            }]
    }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart


bar_data1 = {
    'x': ['giraffes', 'orangutans', 'monkeys'],
    'y': [20, 14, 23],
    'name': 'SF Zoo',
    'type': 'bar'
}

bar_data1  = {
    'x': ['giraffes', 'orangutans', 'monkeys'],
    'y': [12, 18, 29],
    'name': 'LA Zoo',
    'type': 'bar'
}

# Plot bar chart
def bar_chart():

    # Define data traces
    data = [bar_data1, bar_data1]

    # Define Layout
    layout = {
        'width': 385,
        'height': 365,
        'title': "Stack bar chart example",
        'annotations': [
            {
            'font': {'size': 20},
            'showarrow': False,
            'text': 'GHG',
            'x': 0.50,
            'y': 0.5
            }],
        'barmode': 'stack'
    }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart


pie_data = {
    'labels': ["Italy", "France", "Spain", "USA", "Argentina"],
    'values': [55, 49, 44, 24, 15],
    'type': 'pie'
}

# Plot pie chart
def pie_chart():

    # Define data traces
    data = [pie_data]

    # Define Layout
    layout = {
        'width': 385,
        'height': 365,
        'title': "Pie chart example",
        'annotations': [
            {
            'font': {'size': 20},
            'showarrow': False,
            'text': 'GHG',
            }]
    }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart


doughnut_data = {
    'labels': ["Italy", "France", "Spain", "USA", "Argentina"],
    'values': [55, 49, 44, 24, 15],
    'hole': .6,
    'type': 'pie'
}

# Plot doughnut chart
def doughnut_chart():

    # Define data traces
    data = [doughnut_data]

    # Define Layout
    layout = {
        'width': 385,
        'height': 365,
        'title': "doughnut chart example",
        'annotations': [
            {
            'font': {'size': 20},
            'showarrow': False,
            'text': 'GHG',
            }]
    }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart