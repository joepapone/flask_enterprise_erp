from plotly.offline import plot
import plotly.graph_objects as go

# Hide modobar
config = {'displayModeBar': False}

# Create line chart data list
def line_data(data):
    chart_data=[]
    x = []
    y = []
    for i in data:
        x.append(i[0])
        y.append(float(i[1]))
    
    chart_data.append(x)
    chart_data.append(y)

    return chart_data


# Create plotly line chart
def line_chart(title, x_axis, y_axis, data):

    # get chart data list
    chart_data = line_data(data)
    
    # set chart
    fig = go.Figure(go.Scatter(
        x = chart_data[0],
        y = chart_data[1],
        mode='lines+markers',
        name='Weight',
        line=dict(color='firebrick', width=2)))

    # set chart layout
    fig.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        title=dict(text='<b>'+ title +'</b>',x=0.5,y=0.95,font=dict(family="Calibri",size=26,color='#323232')),
        paper_bgcolor='#ffffff',
        plot_bgcolor='#f2f2f2',
        showlegend=True,
        legend=dict(yanchor="top",y=0.99,xanchor="left", x=0.01)
        )

    # set chart x axis
    fig.update_xaxes(
        visible=True,
        title_text = '<b>{0}</b>'.format(x_axis),
        title_font=dict(size=18, family='Calibri', color='#002b80'),
        title_standoff = 10,
        showline=True, 
        linewidth=1,
        linecolor='#808080',
        mirror=True,
        zeroline=True, 
        zerolinewidth=1, 
        zerolinecolor='#e6e6e6',
        showgrid=True,
        gridwidth=1, 
        gridcolor='#e6e6e6',
        tickangle = 45,
        ticksuffix = "",
        tickfont=dict(family='Calibri', color='#666666', size=14)
        )

    # set chart x axis
    fig.update_yaxes(
        visible=True,
        title_text = '<b>{0}</b>'.format(y_axis),
        title_font=dict(size=18, family='Calibri', color='#002b80'),
        title_standoff = 10,
        showline=True, 
        linewidth=1,
        linecolor='#808080',
        mirror=True,
        zeroline=True, 
        zerolinewidth=1, 
        zerolinecolor='#e6e6e6',
        showgrid=True,
        gridwidth=1, 
        gridcolor='#e6e6e6',
        ticksuffix = 'kg',
        tickfont=dict(family='Calibri', color='#666666', size=14)
        )

    #fig.show(config=config)
    return fig


# Get trend line chart
def get_trend(title,x_axis,y_axis,trend):

    # set configuration and layout                   
    trend_fig = line_chart(title,x_axis,y_axis,trend)

    # plot chart on html page
    if len(trend) == 0:
        return ''
    else:
        print('{0}: {1} chart successfully configured.\n'.format('Trend', 'Line graph'))
        return plot(trend_fig, output_type='div', config=config)