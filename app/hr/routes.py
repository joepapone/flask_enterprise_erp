
from flask import Blueprint, render_template
from flask_login import login_required
from markupsafe import Markup

from ..app import HEADER
from .charts import bar_chart, line_chart, pie_chart, doughnut_chart

hr = Blueprint('hr', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static')


# Dashboard
@hr.route('/hr/dashboard')
@login_required
def dashboard():
    # Set html page heading
    heading='Human Resources (HR)'

    '''
    # Set bar chart
    BarPlot1 = bar_chart()
    BarPlot2 = bar_chart()

    return render_template('hr/dashboard.html', header=HEADER, heading=heading, 
                           chart1=Markup(BarPlot1),
                           chart2=Markup(BarPlot2))
    
    BarPlot3 = bar_chart_JSON()
    return render_template('hr/dashboard.html', header=HEADER, heading=heading, 
                           chart3=BarPlot3)
    '''

    BarPlot1 = bar_chart()
    BarPlot2 = line_chart()
    BarPlot3 = pie_chart()
    BarPlot4 = doughnut_chart()
    return render_template('hr/dashboard.html', header=HEADER, heading=heading, 
                           chart1=BarPlot1,
                           chart2=BarPlot2,
                           chart3=BarPlot3,
                           chart4=BarPlot4                         
                           )