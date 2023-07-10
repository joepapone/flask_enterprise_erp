from flask_wtf import FlaskForm
from wtforms import Form, fields
from wtforms.validators import ValidationError, InputRequired, Email

from .. import db
from ..admin.models import Country, Department
from .models import Terms, Status


# Validate for length
def length(min=-1, max=-1):
    message = 'Must be between %d and %d characters long.' % (min, max)
    def _length(form, field):
        l = field.data and len(field.data) or 0
        if l < min or max != -1 and l > max:
            raise ValidationError(message)
    return _length


# Validate terms for duplicates
def terms_duplicate(form, field):
    obj = Terms.query.filter(Terms.terms == field.data).first()
    if obj is not None:
        raise ValidationError('Terms already exists')

# Terms form attributes
class TermsForm(FlaskForm):
    terms = fields.StringField(label='Terms', validators=[length(min=3, max=50), terms_duplicate], description='Terms',
    render_kw={'class': 'field-data', 'placeholder': 'Terms..', 'autofocus': ''})


# Validate status for duplicates
def status_duplicate(form, field):
    item = Status.query.filter(Status.status_title == field.data).first()
    if item is not None:
        raise ValidationError('Status title already exists')

# Status form attributes
class StatusForm(FlaskForm):
    status_title = fields.StringField(label='Status', validators=[length(min=3, max=50), status_duplicate], description='Status',
    render_kw={'class': 'field-data', 'placeholder': 'Status..', 'autofocus': ''})


# Get departments to populate select field
def get_departments():
    item_list = [(item.department_id, item.department_name) for item in db.session.scalars(db.select(Department)).all()]
    return item_list

# Get terms to populate select field
def get_terms():
    item_list = [(item.terms_id, item.terms) for item in db.session.scalars(db.select(Terms)).all()]
    return item_list

# Get status to populate select field
def get_status():
    item_list = [(item.status_id, item.status_title) for item in db.session.scalars(db.select(Status)).all()]
    return item_list

# Employee form attributes
class EmployeeForm(FlaskForm):
    employee_name = fields.StringField(label='Name', validators=[length(min=3, max=50)], description='Name',
    render_kw={'class': 'field-data', 'placeholder': 'Name..', 'autofocus': ''})
    employee_surname = fields.StringField(label='Surname', validators=[length(min=3, max=50)], description='Surname',
    render_kw={'class': 'field-data', 'placeholder': 'Surname..', 'autofocus': ''})
    department_id = fields.SelectField(label='Department', choices=get_departments ,validators=[InputRequired()], description='Department',
    render_kw={'class': 'field-data', 'autofocus': ''})
    job_id = fields.SelectField(label='Job', coerce=int, validators=[InputRequired()], description='Job',
    render_kw={'class': 'field-data', 'autofocus': ''})
    terms_id = fields.SelectField(label='Terms', choices=get_terms ,validators=[InputRequired()], description='Terms',
    render_kw={'class': 'field-data', 'autofocus': ''})
    status_id = fields.SelectField(label='Status', choices=get_status ,validators=[InputRequired()], description='Status',
    render_kw={'class': 'field-data', 'autofocus': ''})


# Email form attributes
class EmailForm(FlaskForm):
    email = fields.StringField(label='Email', validators=[length(min=3, max=120), Email()], description='Email',
    render_kw={'class': 'field-data', 'placeholder': 'Email..', 'autofocus': ''})
    label = fields.SelectField(label='Label', choices=['Home','Work'], validators=[length(min=3, max=20)], description='Lable',
    render_kw={'class': 'field-data', 'placeholder': 'Email..', 'autofocus': ''})


# Get dial code to populate select field
def get_dial_code():
    item_list = [(item.dial_code) for item in db.session.scalars(db.select(Country)).all()]
    return item_list

# Phone form attributes
class PhoneForm(FlaskForm):
    dial_code = fields.SelectField(label='Dial code', choices=get_dial_code ,validators=[InputRequired()], description='Dial code',
    render_kw={'class': 'field-data', 'placeholder': 'Dial code..', 'autofocus': ''})
    phone_number = fields.StringField(label='Phone number', validators=[length(min=3, max=50)], description='Phone number',
    render_kw={'class': 'field-data', 'placeholder': 'Phone number..', 'autofocus': ''})
    label = fields.SelectField(label='Label', choices=['Home','Work','Mobile'], validators=[length(min=3, max=20)], description='Lable',
    render_kw={'class': 'field-data', 'placeholder': 'Email..', 'autofocus': ''})


# Get country to populate select field
def get_country():
    item_list = [(item.country_id, item.country_name) for item in db.session.scalars(db.select(Country)).all()]
    return item_list

# Address form attributes
class AddressForm(FlaskForm):
    address1 = fields.StringField(label='Address line 1', validators=[length(min=0, max=50)], description='Address1',
    render_kw={'class': 'field-data', 'placeholder': 'Address line 1..', 'autofocus': ''})
    address2 = fields.StringField(label='Address line 2', validators=[length(min=0, max=50)], description='Address2',
    render_kw={'class': 'field-data', 'placeholder': 'Address line 2..', 'autofocus': ''})
    postal_code = fields.StringField(label='Postal code', validators=[length(min=0, max=50)], description='Postal code',
    render_kw={'class': 'field-data', 'placeholder': 'Postal code..', 'autofocus': ''})
    city = fields.StringField(label='City', validators=[length(min=0, max=50)], description='City',
    render_kw={'class': 'field-data', 'placeholder': 'City..', 'autofocus': ''})
    state = fields.StringField(label='State', validators=[length(min=0, max=50)], description='State',
    render_kw={'class': 'field-data', 'placeholder': 'State..', 'autofocus': ''})
    country_id = fields.SelectField(label='Country', choices=get_country ,validators=[InputRequired()], description='Country',
    render_kw={'class': 'field-data', 'placeholder': 'Country..', 'autofocus': ''})


