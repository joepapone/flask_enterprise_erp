from flask_wtf import FlaskForm
from wtforms import Form, fields
from wtforms.validators import ValidationError, InputRequired, Email

from .models import Title, Gender, Marital, Department, Job, Job_Terms, Job_Status
from ..admin.models import Country
from .. import db


# ------------------------------------------------
#    Data Validation
# ------------------------------------------------

# Validate for length
def length(min=-1, max=-1):
    message = 'Must be between %d and %d characters long.' % (min, max)
    def _length(form, field):
        l = field.data and len(field.data) or 0
        if l < min or max != -1 and l > max:
            raise ValidationError(message)
    return _length

# Validate department for duplicates
def department_duplicate(form, field):
    item = Department.query.filter(Department.department_name == field.data).first()
    if item is not None:
        raise ValidationError("Department name already exists")

# Validate department for duplicates
def job_duplicate(form, field):
    item = Job.query.filter(Job.job_title == field.data).first()
    if item is not None:
        raise ValidationError("Job title already exists")

# Validate terms for duplicates
def terms_duplicate(form, field):
    obj = Job_Terms.query.filter(Job_Terms.terms == field.data).first()
    if obj is not None:
        raise ValidationError('Terms already exists')

# Validate status for duplicates
def status_duplicate(form, field):
    item = Job_Status.query.filter(Job_Status.status_title == field.data).first()
    if item is not None:
        raise ValidationError('Status title already exists')

# Validate gender for duplicates
def gender_duplicate(form, field):
    obj = Gender.query.filter(Gender.gender == field.data).first()
    if obj is not None:
        raise ValidationError('Gender already exists')

# Validate marital for duplicates
def marital_duplicate(form, field):
    obj = Marital.query.filter(Marital.marital_status == field.data).first()
    if obj is not None:
        raise ValidationError('Marital status already exists')


# ------------------------------------------------
#    Data collection and Processing
# ------------------------------------------------

# Get title to populate select field
def get_title():
    item_list = [(item.title_id, item.title_name) for item in db.session.scalars(db.select(Title)).all()]
    return item_list

# Get gender to populate select field
def get_gender():
    item_list = [(item.gender_id, item.gender) for item in db.session.scalars(db.select(Gender)).all()]
    return item_list

# Get marital status to populate select field
def get_marital():
    item_list = [(item.marital_id, item.marital_status) for item in db.session.scalars(db.select(Marital)).all()]
    return item_list

# Get departments to populate select field
def get_departments():
    item_list = [(item.department_id, item.department_name) for item in db.session.scalars(db.select(Department)).all()]
    # Add null tuple item to first position of list
    item_list.insert(0, (0,''))

    return item_list

# Get terms to populate select field
def get_terms():
    item_list = [(item.terms_id, item.terms) for item in db.session.scalars(db.select(Job_Terms)).all()]
    return item_list

# Get status to populate select field
def get_status():
    item_list = [(item.status_id, item.status_title) for item in db.session.scalars(db.select(Job_Status)).all()]
    # Remove first item from list
    item_list.pop(0)
    return item_list

# Get dial code to populate select field
def get_dial_code():
    item_list = [(item.dial_code) for item in db.session.scalars(db.select(Country)).all()]
    return item_list

# Get country to populate select field
def get_country():
    item_list = [(item.country_id, item.country_name) for item in db.session.scalars(db.select(Country)).all()]
    return item_list


# ------------------------------------------------
#    Flask Forms
# ------------------------------------------------

# Gender form attributes
class GenderForm(FlaskForm):
    gender = fields.StringField(label='Gender', validators=[length(min=3, max=50), gender_duplicate], description='Gender',
    render_kw={'class': 'field-data', 'placeholder': 'Gender..', 'autofocus': ''})

# Marital form attributes
class MaritalForm(FlaskForm):
    marital_status = fields.StringField(label='Marital status', validators=[length(min=3, max=50), marital_duplicate], description='Marital status',
    render_kw={'class': 'field-data', 'placeholder': 'Marital status..', 'autofocus': ''})

# Employee form attributes
class EmployeeForm(FlaskForm):
    title_id = fields.SelectField(label='Title', choices=get_title, validators=[InputRequired()], description='Title',
    render_kw={'class': 'field-data', 'autofocus': ''})
    employee_name = fields.StringField(label='Name', validators=[length(min=3, max=50)], description='Name',
    render_kw={'class': 'field-data', 'placeholder': 'Name..', 'autofocus': ''})
    employee_surname = fields.StringField(label='Surname', validators=[length(min=3, max=50)], description='Surname',
    render_kw={'class': 'field-data', 'placeholder': 'Surname..', 'autofocus': ''})
    birthdate = fields.DateField(label='Birthdate', validators=[InputRequired()], description='Birthdate',
    render_kw={'class': 'field-data', 'autofocus': ''})
    gender_id = fields.SelectField(label='Gender', choices=get_gender, validators=[InputRequired()], description='Gender',
    render_kw={'class': 'field-data', 'autofocus': ''})
    marital_id = fields.SelectField(label='Marital status', choices=get_marital,validators=[InputRequired()], description='Maritial',
    render_kw={'class': 'field-data', 'autofocus': ''})

# Department form attributes
class DepartmentForm(FlaskForm):
    department_name = fields.StringField(label='Department', validators=[length(min=3, max=50), department_duplicate], description="Department name",
    render_kw={'class': 'field-data', 'placeholder': 'Name..', 'autofocus': ""})

# Job form attributes
class JobForm(FlaskForm):
    department_id = fields.SelectField(label='Department', choices=get_departments ,validators=[InputRequired()], description="Department",
    render_kw={'class': 'field-data', 'autofocus': ""})
    job_title = fields.StringField(label='Job titile', validators=[length(min=3, max=50), job_duplicate], description="Job title",
    render_kw={'class': 'field-data', 'placeholder': 'Title..', 'autofocus': ""})
    job_description = fields.TextAreaField(label='Job description', validators=[length(min=3, max=1000), job_duplicate], description="Job description",
    render_kw={'class': 'field-data', 'rows': 10, 'placeholder': 'Description..', 'autofocus': ""})

# Job terms form attributes
class Job_TermsForm(FlaskForm):
    terms = fields.StringField(label='Terms', validators=[length(min=3, max=50), terms_duplicate], description='Terms',
    render_kw={'class': 'field-data', 'placeholder': 'Terms..', 'autofocus': ''})

# Job status form attributes
class Job_StatusForm(FlaskForm):
    status_title = fields.StringField(label='Status', validators=[length(min=3, max=50), status_duplicate], description='Status',
    render_kw={'class': 'field-data', 'placeholder': 'Status..', 'autofocus': ''})

# Job history start form attributes
class Job_History_StartForm(FlaskForm):
    department_id = fields.SelectField(label='Department', choices=get_departments, validators=[InputRequired()], description="Department",
    render_kw={'class': 'field-data', 'autofocus': ""})
    job_id = fields.SelectField(label='Job', coerce=int, validators=[InputRequired()], description='Job',
    render_kw={'class': 'field-data', 'autofocus': ''})
    terms_id = fields.SelectField(label='Terms', choices=get_terms, validators=[InputRequired()], description='Terms',
    render_kw={'class': 'field-data', 'autofocus': ''})
    start_date = fields.DateField(label='Start date', format='%Y-%m-%d', validators=[InputRequired()], description='Start date',
    render_kw={'class': 'field-data', 'autofocus': ''})

# Job history end form attributes
class Job_History_EndForm(FlaskForm):
    end_date = fields.DateField(label='End date', description='End date',
    render_kw={'class': 'field-data', 'autofocus': ''})
    status_id = fields.SelectField(label='Termination motive', choices=get_status, validators=[InputRequired()], description='Motive',
    render_kw={'class': 'field-data', 'autofocus': ''})

# Email form attributes
class EmailForm(FlaskForm):
    email = fields.StringField(label='Email', validators=[length(min=3, max=120), Email()], description='Email',
    render_kw={'class': 'field-data', 'placeholder': 'Email..', 'autofocus': ''})
    label = fields.SelectField(label='Label', choices=['Home','Work'], validators=[length(min=3, max=20)], description='Lable',
    render_kw={'class': 'field-data', 'placeholder': 'Email..', 'autofocus': ''})

# Phone form attributes
class PhoneForm(FlaskForm):
    dial_code = fields.SelectField(label='Dial code', choices=get_dial_code ,validators=[InputRequired()], description='Dial code',
    render_kw={'class': 'field-data', 'placeholder': 'Dial code..', 'autofocus': ''})
    phone_number = fields.StringField(label='Phone number', validators=[length(min=3, max=50)], description='Phone number',
    render_kw={'class': 'field-data', 'placeholder': 'Phone number..', 'autofocus': ''})
    label = fields.SelectField(label='Label', choices=['Home','Work','Mobile'], validators=[length(min=3, max=20)], description='Lable',
    render_kw={'class': 'field-data', 'placeholder': 'Email..', 'autofocus': ''})

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

