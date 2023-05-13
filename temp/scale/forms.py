from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.fields.simple import SubmitField
from wtforms.validators import InputRequired, NumberRange


class Zero_Form(FlaskForm):
    raw_zero = fields.DecimalField(label='Raw value (Zero)',
        validators=[InputRequired()],
        places=3,
        description="Set scale calibration zero",
        render_kw={'class': 'field-data', 'type': 'number', 'readonly': True})
    zero = fields.DecimalField(label='Zero',
        validators=[InputRequired(), NumberRange(min=0, max=150, message='Zero value must be between %(min)d and %(max)d')],
        description="Set scale calibration zero",
        render_kw={'class': 'field-data', 'type': 'number', 'step': 0.01, 'placeholder': 'Ajust zero..'})
    submit = SubmitField(label='Submit',
        render_kw={'class': 'field-submit'})


class Span_Form(FlaskForm):
    raw_span = fields.DecimalField(label='Raw value (Span)',
        validators=[InputRequired()],
        places=3,
        description="Set scale calibration span",
        render_kw={'class': 'field-data', 'type': 'number', 'readonly': True})
    span = fields.DecimalField(label='Span',
        validators=[InputRequired(), NumberRange(min=0, max=150, message='Span value must be between %(min)d and %(max)d')],
        description="Set scale calibration span",
        render_kw={'class': 'field-data', 'type': 'number', 'step': 0.01, 'placeholder': 'Ajust span..'})
    submit = SubmitField(label='Submit',
        render_kw={'class': 'field-submit'})


class Offset_Form(FlaskForm):
    offset = fields.DecimalField(label='Offset',
        validators=[InputRequired(), NumberRange(min=-10, max=10, message='Offset value must be between %(min)d and %(max)d')],
        description="Set scale calibration offset",
        render_kw={'class': 'field-data', 'type': 'number', 'step': 0.01, 'placeholder': 'Ajust offset..'})


class Comments_Form(FlaskForm):
    comments = fields.TextAreaField(label='Comments',
        validators=[InputRequired()],
        description="Set scale calibration comments",
        render_kw={'placeholder': 'Comments..', 'style': 'height:200px'})


class Alarms_Form(FlaskForm):
    alarm_H = fields.DecimalField(label='Alarm H',
        validators=[InputRequired(), NumberRange(min=0, max=150, message='Alarm H value must be between %(min)d and %(max)d')],
        description="Set scale alarm high",
        render_kw={'class': 'field-data', 'type': 'number', 'step': 0.01, 'placeholder': 'Ajust alarm high..'})
    alarm_L = fields.DecimalField(label='Alarm L',
        validators=[InputRequired(), NumberRange(min=0, max=150, message='Alarm L value must be between %(min)d and %(max)d')],
        description="Set scale alarm low",
        render_kw={'class': 'field-data', 'type': 'number', 'step': 0.01, 'placeholder': 'Ajust alarm low..'})
    alarm_LL = fields.DecimalField(label='Alarm LL',
        validators=[InputRequired(), NumberRange(min=0, max=150, message='Alarm LL value must be between %(min)d and %(max)d')],
        description="Set scale alarm very low",
        render_kw={'class': 'field-data', 'type': 'number', 'step': 0.01, 'placeholder': 'Ajust alarm very low..'})