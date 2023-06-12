# Plotly chart configurtion
config = {
    'displayModeBar': False,
    'responsive': True
}


# Format title and subtitle
def format_title(title, subtitle=None, subtitle_font_size=20):
    if not subtitle:
        return title
    subtitle = f'<span style="font-size: {subtitle_font_size}px;"><b>{subtitle}</b></span>'
    return f'{title}<br>{subtitle}'


# Indicator delta color
def delta_color(reference, relative_delta=False, invert_color=False):
    default = {'reference': reference, 'relative': relative_delta, 'increasing': { 'color': '#3D9970' } , 'decreasing': { 'color': '#FF4136' }}
    if invert_color:
        default = {'reference': reference, 'relative': relative_delta, 'increasing': { 'color': '#FF4136' } , 'decreasing': { 'color': '#3D9970' }}

    return default


# Plot angular gauge
def angular_gauge(title, reference, value, range, suffix, relative_delta, invert_color):
    """ 
    Angular gauge chart
    :param title: Indicator title (any)
    :param value: Indicator reference value (integer)
    :param value: Indicator value (integer)
    :param range: Indicator value range ([integer, integer])
    :param relative_delta: Indicator delta percentage  (bool)
    :param invert_color: Indicator delta color (bool)
    :return: Indicator plotly.js data, layout, and config
    """

    # Define data
    data = [{
        'title': { 'text': title },
        'type': "indicator",
        'delta': delta_color(reference, relative_delta, invert_color),
        'value': value,
        'number': { 'suffix': suffix },
        'gauge': { 'axis': { 'visible': True, 'range': range } },
        'mode': "number+delta+gauge",
        'domain': { 'x': [0.1, 0.9], 'y': [0, 1] }
    }]
    
    # Define Layout
    layout = {
        'width': 385,
        'height': 150,
        'margin': { 't': 50, 'b': 20, 'l': 20, 'r': 20 }
    }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart


# Plot bullet gauge
def bullet_gauge(title, reference, value, range):
    """ 
    Bullet gauge chart
    :param title: Indicator title (integer,integer)
    :param value: Indicator reference value (integer)
    :param value: Indicator value (integer)
    :param range: Indicator value range ([integer, integer])
    :return: Indicator plotly.js data, layout, and config
    """

    # Define data
    data = [{
        'title': { 'text': title },
        'type': "indicator",
        'delta': { 'reference': reference },
        'value': value,
        'gauge': {'shape': "bullet", 'axis': {'visible': True, 'range': range }},
        'mode': "number+delta+gauge",
        'domain': { 'x': [0.20, 1], 'y': [0.35, 0.65] }
    }]

    # Define Layout
    layout = {
        'width': 385,
        'height': 150,
        'margin': { 't': 20, 'b': 20, 'l': 20, 'r': 20 },
    }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart


# Plot double bullet gauge
def double_bullet_gauge(title1, title2, reference, value1, value2, range):
    """ 
    Double bullet gauge chart
    :param title: Indicator title (integer,integer)
    :param value: Indicator reference value (integer)
    :param value: Indicator value (integer)
    :param range: Indicator value range ([integer, integer])
    :return: Indicator plotly.js data, layout, and config
    """

    # Define data
    data = [{
        'title': { 'text': title1 },
        'type': "indicator",
        'value': value1,
        'gauge': {
        'shape': "bullet",
        'axis': {
            'visible': False,
            'range': range
        }
        },
        'domain': { 'x': [0.2, 1], 'y': [0.10, 0.40] }
    },
    {
        'title': { 'text': title2 },
        'type': "indicator",
        'value': value2,
        'gauge': {
        'shape': "bullet",
        'axis': {
            'visible': False,
            'range': range
        }
        },
        'domain': { 'x': [0.2, 1], 'y': [0.60, 0.90] }
    }]

    # Define Layout
    layout = {
        'width': 385,
        'height': 150,
        'margin': { 't': 20, 'b': 20, 'l': 20, 'r': 20 },
        'template': {
            'data': {
            'indicator': [
                {
                'mode': "number+delta+gauge",
                'delta': { 'reference': reference }
                }
            ]
            }
        }
    }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart


# Plot data cards
def data_cards(title, reference, value):
    """ 
    Data cards chart
    :param title: Indicator title (str)
    :param value: Indicator reference value (integer)
    :param value: Indicator value (integer)
    :return: Indicator plotly.js data, layout, and config
    """

    # Define data
    data = [{
        'title': { 'text': title },
        'type': "indicator",
        'mode': "number+delta",
        'delta': { 'reference': reference },
        'value': value,
        'domain': { 'row': 0, 'column': 0 },
    }]

    # Define Layout
    layout = {
        'width': 385,
        'height': 150,
        'margin': { 't': 50, 'b': 25, 'l': 20, 'r': 20 },
        'grid': { 'rows': 1, 'columns': 1, 'pattern': "independent" }
     }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart


# Plot line chart
def line_chart(title, subtitle, x_title, y_title, x_range, y_range, x_data, y_data):
    """ 
    Line chart
    :param title: Chart title (any)
    :param subtitle: Chart subtitle (any)
    :param x_title: Chart x axis title (any)
    :param y_title: Chart y axis title (any)
    :param x_range: Chart x axis range (integer, double, str)
    :param y_range: Chart y axis range (integer, double, str)
    :param x_data: Chart x data range (integer, double, str)
    :param y_data: Chart y data range (integer, double, str)
    :return: Indicator plotly.js data, layout, and config
    """

    # Define data
    data = [{
        'x': x_data,
        'y': y_data,
        'mode': 'lines'
        }]

    # Define Layout
    layout = {
        'width': 385,
        'height': 300,
        'title': format_title(title, subtitle),
        'margin': {'t': 80, 'b': 60, 'l': 60, 'r': 50},
        'xaxis': {'range': x_range, 'title': x_title},
        'yaxis': {'range': y_range, 'title': y_title},
    }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart


# Plot area chart
def area_chart(title, subtitle, x_title, y_title, x_range, y_range, x_data, y_data):
    """ 
    Line chart
    :param title: Chart title (any)
    :param subtitle: Chart subtitle (any)
    :param x_title: Chart x axis title (any)
    :param y_title: Chart y axis title (any)
    :param x_range: Chart x axis range (integer, double, str)
    :param y_range: Chart y axis range (integer, double, str)
    :param x_data: Chart x data range (integer, double, str)
    :param y_data: Chart y data range (integer, double, str)
    :return: Indicator plotly.js data, layout, and config
    """

    # Define data
    data = [{
        'x': x_data,
        'y': y_data,
        'fill': 'tozeroy',
        'type': 'scatter'
        }]

    # Define Layout
    layout = {
        'width': 385,
        'height': 300,
        'title': format_title(title, subtitle),
        'margin': {'t': 80, 'b': 60, 'l': 60, 'r': 50},
        'xaxis': {'range': x_range, 'title': x_title},
        'yaxis': {'range': y_range, 'title': y_title},
    }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart

# Plot bar chart
def bar_chart(title, subtitle, name, x_data, y_data, orientation):
    """ 
    Bar chart
    :param title: Chart title (any)
    :param subtitle: Chart subtitle (any)
    :param name: Chart stack name (any)
    :param orientation: Chart bar orientation (str), 'v' - vertical, 'h' - horizontal
    :param x_data: Chart x data range (integer, double, str)
    :param y_data: Chart y data range (integer, double, str)
    :return: Indicator plotly.js data, layout, and config
    """

    # Define data
    data = [{
        'x': x_data,
        'y': y_data,
        'name': name,
        'orientation': orientation,
        'type': 'bar'
        }]

    # Define Layout
    layout = {
        'width': 385,
        'height': 300,
        'title': format_title(title, subtitle),
        'margin': {'t': 80, 'b': 50, 'l': 80, 'r': 50},
        'barmode': 'stack'
    }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart


# Plot stack bar chart
def stack_bar_chart(title, subtitle, name1, name2, x_data1, y_data1, x_data2, y_data2, orientation):
    """ 
    Stact bar chart
    :param title: Chart title (any)
    :param subtitle: Chart subtitle (any)
    :param name: Chart stack name (any)
    :param x_data: Chart x data range (integer, double, str)
    :param y_data: Chart y data range (integer, double, str)
    :param orientation: Chart bar orientation (str), 'v' - vertical, 'h' - horizontal
    :return: Indicator plotly.js data, layout, and config
    """

    # Define data
    data = [{
        'x': x_data1,
        'y': y_data1,
        'name': name1,
        'orientation': orientation,
        'type': 'bar'
        }, 
        {
        'x': x_data2,
        'y': y_data2,
        'name': name2,
        'orientation': orientation,
        'type': 'bar'
    }]

    # Define Layout
    layout = {
        'width': 385,
        'height': 300,
        'title': format_title(title, subtitle),
        'margin': {'t': 80, 'b': 50, 'l': 80, 'r': 50},
        'barmode': 'stack',
    }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart


# Plot pie chart
def pie_chart(title, subtitle, labels, values, hole, annotation):
    """ 
    Pie chart
    :param title: Chart title (any)
    :param subtitle: Chart subtitle (any)
    :param labels: Chart lables (any)
    :param values: Chart data range (integer, double)
    :param hole: Chart hole size (double), 0.0 to 1.0
    :param annotation: Chart annotation (str)
    :return: Indicator plotly.js data, layout, and config
    """

    # Define data
    data = [{
    'labels': labels,
    'values': values,
    'type': 'pie',
    'hole': hole,
    'textinfo': "label+percent",
    'textposition': "outside",
    'automargin': True
    }]

    # Define Layout
    layout = {
        'width': 385,
        'height': 300,
        'title': format_title(title, subtitle),
        'margin': {'t': 80, 'b': 50, 'l': 50, 'r': 50},
        'showlegend': False,
        'annotations': [
            {
            'font': {'size': 25},
            'showarrow': False,
            'text': annotation,
            }]
    }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart


# Plot chart chart
def table_chart(title, subtitle, headers, values):
    """ 
    Table chart
    :param title: Chart title (any)
    :param subtitle: Chart subtitle (any)
    :param headers: Chart table headers (any)
    :param values: Chart table rows and cell values (any)
    :return: Indicator plotly.js data, layout, and config
    """

    # Define data
    data = [{
        'type': 'table',
        'header': {
            'values': headers,
            'align': 'center',
            'line': {'width': 1, 'color': 'grey'},
            'fill': {'color': '#34495E'},
            'font': {'family': 'Arial', 'size': 16, 'color': 'white'}
        },
        'cells': {
            'values': values,
            'align': 'center',
            'line': {'width': 1, 'color': 'grey'},
            'fill': {'color': [['white','lightgrey','white',
                                'lightgrey','white']]},
            'font': {'family': 'Arial', 'size': 14, 'color': ['black']},
            'height': 30
        }
    }]
    

    # Define Layout
    layout = {
        'width': 770,
        'title': format_title(title, subtitle),
        'margin': {'t': 80, 'b': 50, 'l': 50, 'r': 50},
    }

    # Chart assigment
    chart = {'data': data, 'layout': layout, 'config': config}

    return chart