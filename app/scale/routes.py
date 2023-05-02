from flask import Blueprint, redirect, render_template, flash, request, Markup
from flask_login import login_required

from .. import db
from ..config import HEADER
from .models import Cal
from .forms import Zero_Form, Span_Form, Offset_Form, Comments_Form, Alarms_Form
from .data import get_raw, get_mean, get_weight
from .graphs import get_trend


scale = Blueprint('scale', __name__,
    template_folder='templates',
    static_folder='static')


@scale.route('/get/raw', methods=['GET'])
def raw_value():
    
    return str(get_raw())


@scale.route('/get/mean', methods=['GET'])
def mean_value():
    
    return str(get_mean())


@scale.route('/get/weight', methods=['GET'])
def weight_value():
    
    return str(get_weight())


@scale.route('/calibration/raw_<id>', methods=['GET','POST'])
def view_raw(id):
    # set html page heading
    heading='Raw calibration'

     # set initial values
    progress_text='Read raw values:'
    raw_value = 0.000
    get_raw.count = 0
    get_raw.values = []

    if request.method == 'POST':
        if id == 'zero':
            return redirect('/calibration/zero')
        elif id == 'span':
            return redirect('/calibration/span')
    
    return render_template('calibration/raw.html', header=HEADER, heading=heading, 
        progress_text=progress_text, raw_value=raw_value, id=id)


@scale.route("/calibration/zero", methods=["GET", "POST"])
@login_required
def zero():
    # set html page heading
    heading='Zero calibration'
    
    # create model instance with query data
    scale = Cal.query.get(1)

    # transfer new raw zero to form
    if get_raw.store:
        scale.raw_zero = get_raw.mean
        # reset flag
        get_raw.store = False

    # create form instance and load it with object data
    form = Zero_Form(obj=scale)

    if form.validate_on_submit():
        # marked for update
        scale.raw_zero = form.raw_zero.data
        scale.zero = form.zero.data

        # commit changes to database
        db.session.commit()
        flash('Raw zero {0} and zero {1} values successfully submitted'.format(scale.raw_zero, scale.zero))
        return redirect('/calibration/zero')

    return render_template('calibration/zero.html', header=HEADER, heading=heading, form=form)


@scale.route("/calibration/span", methods=["GET", "POST"])
@login_required
def span():
    # set html page heading
    heading='Span calibration'
    
    # create model instance with query data
    scale = Cal.query.get(1)

    # transfer new raw span to form
    if get_raw.store:
        scale.raw_span = get_raw.mean
        # reset flag
        get_raw.store = False

    # create form instance and load it with object data
    form = Span_Form(obj=scale)

    if form.validate_on_submit():
        # marked for update
        scale.raw_span = form.raw_span.data
        scale.span = form.span.data

        # commit changes to database
        db.session.commit()
        flash('Raw span {0} and span {1} values successfully submitted'.format(scale.raw_span, scale.span))
        return redirect('/calibration/span')

    return render_template('calibration/span.html', header=HEADER, heading=heading, form=form)


@scale.route("/calibration/offset", methods=["GET", "POST"])
@login_required
def offset():
    # set html page heading
    heading='Offset calibration'

    # create model instance with query data
    scale = Cal.query.get(1)

    # create form instance and load it with object data
    form = Offset_Form(obj=scale)

    if form.validate_on_submit():
        # marked for update
        scale.offset = form.offset.data

        # commit changes to database
        db.session.commit() 
        flash('Offset {0} value successfully submitted'.format(scale.offset))
        return redirect('/calibration/offset')

    return render_template('calibration/offset.html', header=HEADER, heading=heading, form=form)


@scale.route("/calibration/comments", methods=["GET", "POST"])
@login_required
def comments():
    # set html page heading
    heading='Comments'

    # create model instance with query data
    scale = Cal.query.get(1)

    # create form instance and load it with object data
    form = Comments_Form(obj=scale)

    if form.validate_on_submit():
        # marked for update
        scale.comments = form.comments.data

        # commit changes to database
        db.session.commit() 
        flash('Comments {0} successfully submitted'.format(scale.comments))
        return redirect('/calibration/comments')

    return render_template('calibration/comments.html', header=HEADER, heading=heading, form=form)


@scale.route("/alarms/alarms", methods=["GET", "POST"])
@login_required
def alarms():
    # set html page heading
    heading='Alarms'

    # create model instance with query data
    scale = Cal.query.get(1)

    # create form instance and load it with object data
    form = Alarms_Form(obj=scale)

    if form.validate_on_submit():
        # marked for update
        scale.alarm_H = form.alarm_H.data
        scale.alarm_L = form.alarm_L.data
        scale.alarm_LL = form.alarm_LL.data

        # commit changes to database
        db.session.commit() 
        flash('Alarms H: {0}, L: {1} and LL: {2} successfully submitted'.format(scale.alarm_H, scale.alarm_L, scale.alarm_LL))
        return redirect('/alarms/alarms')

    return render_template('alarms/alarms.html', header=HEADER, heading=heading, form=form)


@scale.route('/calibration')
@login_required
def calibration():
    # set html page heading
    heading='Scale calibration'

    # create model instance with query data
    scale = Cal.query.get(1)

    return render_template('calibration/calibration.html', header=HEADER, heading=heading, scale=scale)


@scale.route('/weight')
@login_required
def weight():
    # set html page heading      
    heading = 'Weight'

    # set initial values
    value = '0'
    unit = 'kg'

    return render_template('view/scale.html', header=HEADER, heading=heading, value=value, unit=unit)


# -- Events view
@scale.route('/diagnostic/events')
@login_required
def events():
    # set html page heading
    heading='Diagnostic events'

    # create model instance with query data.
    events = cal = [('2021-10-12','15:01','Communication failure','#0001'), 
                    ('2021-10-13','09:01','Low level warning','#0002'),
                    ('2021-10-14','09:01','Low level alarm','#0003')] 
    
    return render_template('diagnostic/events.html', header=HEADER, heading=heading, events=events)


# -- Trend view
@scale.route('/diagnostic/trend')
@login_required
def trend():
    # set html page heading
    heading='Diagnostic trend'

    # graph settings
    title = ''
    x_axis = ''
    y_axis = ''

    # create model instance with query data
    trend = [("2021-10-12", 0.00),("2021-10-13 15:00", 1.00),("2021-10-14 16:00", 6.00), 
    ("2021-10-15 19:00", 50.00), ("2021-10-16 20:00", 60.00)]

    # get graphs
    trend_div = get_trend(title,x_axis,y_axis,trend)

    return render_template('diagnostic/trend.html', header=HEADER, heading=heading, trend=Markup(trend_div))