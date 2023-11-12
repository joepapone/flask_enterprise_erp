from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, DecimalField, SelectField, DateField, DateTimeField, DateTimeLocalField
from wtforms.validators import ValidationError, InputRequired, Email
from datetime import datetime

from .models import Department, Job, Job_Terms, Job_Status, Employee_Status, Title, Gender, Marital, Leave_Type, Period, Benefit_Type
from ..admin.models import Country, Currency
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
    item = Job_Status.query.filter(Job_Status.title == field.data).first()
    if item is not None:
        raise ValidationError('Status title already exists')

# Validate title for duplicates
def title_duplicate(form, field):
    obj = Title.query.filter(Title.title == field.data).first()
    if obj is not None:
        raise ValidationError('Title already exists')

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

# Validate leave type for duplicates
def leave_type_duplicate(form, field):
    obj = Leave_Type.query.filter(Leave_Type.type_title == field.data).first()
    if obj is not None:
        raise ValidationError('Lease type already exists')
    
# ------------------------------------------------
#    Data collection and Processing
# ------------------------------------------------

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

# Get job status to populate select field
def get_job_status():
    item_list = [(item.status_id, item.title) for item in db.session.scalars(db.select(Job_Status)).all()]
    # Remove first item from list
    item_list.pop(0)
    return item_list

# Get employee status to populate select field
def get_employee_status():
    item_list = [(item.status_id, item.title) for item in db.session.scalars(db.select(Employee_Status)).all()]
    return item_list

# Get title to populate select field
def get_title():
    item_list = [(item.title_id, item.title) for item in db.session.scalars(db.select(Title)).all()]
    return item_list

# Get gender to populate select field
def get_gender():
    item_list = [(item.gender_id, item.gender) for item in db.session.scalars(db.select(Gender)).all()]
    return item_list

# Get marital status to populate select field
def get_marital():
    item_list = [(item.marital_id, item.marital_status) for item in db.session.scalars(db.select(Marital)).all()]
    return item_list

# Get leave type to populate select field
def get_leave_type():
    item_list = [(item.type_id, item.type_title) for item in db.session.scalars(db.select(Leave_Type)).all()]
    return item_list

# Get time frame to populate select field
def get_period():
    item_list = [(item.period_id,f'per {item.title}') for item in db.session.scalars(db.select(Period)).all()]
    return item_list

# Get benefit type to populate select field
def get_benefit_type():
    item_list = [(item.benefit_type_id, item.title) for item in db.session.scalars(db.select(Benefit_Type)).all()]
    return item_list

# Get years to populate select field
def get_years():
    years = [datetime.today().year - index for index in range(5)]
    item_list = [(year, year) for year in years]

    return item_list

# Get months to populate select field
def get_months():
    months = [index + 1 for index in range(12)]
    item_list = [(month, datetime(2023, month, 1).strftime('%B')) for month in months]
    
    return item_list

# Get dial code to populate select field
def get_dial_code():
    item_list = [(item.dial_code) for item in db.session.scalars(db.select(Country)).all()]
    return item_list

# Get country to populate select field
def get_country():
    item_list = [(item.country_id, item.country_name) for item in db.session.scalars(db.select(Country)).all()]
    return item_list

# Get currency to populate select field
def get_currency():
    item_list = [(item.currency_id, f'{item.currency_name} ({item.currency_code})') for item in db.session.scalars(db.select(Currency)).all()]
    return item_list


# ------------------------------------------------
#    Flask Forms
# ------------------------------------------------

# Department form attributes
class DepartmentForm(FlaskForm):
    department_name = StringField(label='Department', validators=[length(min=3, max=50), department_duplicate], description="Department name",
    render_kw={'class': 'field-data', 'placeholder': 'Name..', 'autofocus': ""})

# Job form attributes
class JobForm(FlaskForm):
    department_id = SelectField(label='Department', choices=get_departments ,validators=[InputRequired()], description="Department",
    render_kw={'class': 'field-data', 'autofocus': ""})
    job_title = StringField(label='Job titile', validators=[length(min=3, max=50), job_duplicate], description="Job title",
    render_kw={'class': 'field-data', 'placeholder': 'Title..', 'autofocus': ""})
    job_description = TextAreaField(label='Job description', validators=[length(min=3, max=1000), job_duplicate], description="Job description",
    render_kw={'class': 'field-data', 'rows': 10, 'placeholder': 'Description..', 'autofocus': ""})

# Job terms form attributes
class Job_TermsForm(FlaskForm):
    terms = StringField(label='Terms', validators=[length(min=3, max=50), terms_duplicate], description='Terms',
    render_kw={'class': 'field-data', 'placeholder': 'Terms..', 'autofocus': ''})

# Job status form attributes
class Job_StatusForm(FlaskForm):
    title = StringField(label='Status', validators=[length(min=3, max=50), status_duplicate], description='Status',
    render_kw={'class': 'field-data', 'placeholder': 'Status..', 'autofocus': ''})

# Employee form attributes
class EmployeeForm(FlaskForm):
    status_id = SelectField(label='Employee status', choices=get_employee_status, validators=[InputRequired()], description='Employee status',
    render_kw={'class': 'field-data', 'autofocus': ''})

# Title form attributes
class TitleForm(FlaskForm):
    title = StringField(label='Title', validators=[length(min=3, max=50), title_duplicate], description='Title',
    render_kw={'class': 'field-data', 'placeholder': 'Title..', 'autofocus': ''})

# Gender form attributes
class GenderForm(FlaskForm):
    gender = StringField(label='Gender', validators=[length(min=3, max=50), gender_duplicate], description='Gender',
    render_kw={'class': 'field-data', 'placeholder': 'Gender..', 'autofocus': ''})

# Marital form attributes
class MaritalForm(FlaskForm):
    marital_status = StringField(label='Marital status', validators=[length(min=3, max=50), marital_duplicate], description='Marital status',
    render_kw={'class': 'field-data', 'placeholder': 'Marital status..', 'autofocus': ''})

# Leave_Type form attributes
class Leave_TypeForm(FlaskForm):
    type_title = StringField(label='Leave type', validators=[length(min=3, max=50), leave_type_duplicate], description='Leave type',
    render_kw={'class': 'field-data', 'placeholder': 'Leave type..', 'autofocus': ''})

# Employee info form attributes
class Employee_InfoForm(FlaskForm):
    title_id = SelectField(label='Title', choices=get_title, validators=[InputRequired()], description='Title',
    render_kw={'class': 'field-data', 'autofocus': ''})
    given_name = StringField(label='Given Name', validators=[length(min=3, max=50)], description='Given Name',
    render_kw={'class': 'field-data', 'placeholder': 'Name..', 'autofocus': ''})
    surname = StringField(label='Surname', validators=[length(min=3, max=50)], description='Surname',
    render_kw={'class': 'field-data', 'placeholder': 'Surname..', 'autofocus': ''})
    passport_no = StringField(label='Passport Nº', validators=[length(min=3, max=50)], description='Passport Nº',
    render_kw={'class': 'field-data', 'placeholder': 'Passport Nº..', 'autofocus': ''})
    id_card_no = StringField(label='ID Card Nº', validators=[length(min=3, max=50)], description='ID Card Nº',
    render_kw={'class': 'field-data', 'placeholder': 'ID Card Nº..', 'autofocus': ''})
    nationality = StringField(label='Nationality', validators=[length(min=2, max=50)], description='Nationality',
    render_kw={'class': 'field-data', 'placeholder': 'Nationality..', 'autofocus': ''})
    place_of_birth_id = SelectField(label='Place of birth', choices=get_country,validators=[InputRequired()], description='Place of birth',
    render_kw={'class': 'field-data', 'autofocus': ''})
    birthdate = DateField(label='Birthdate', validators=[InputRequired()], description='Birthdate',
    render_kw={'class': 'field-data', 'autofocus': ''})
    gender_id = SelectField(label='Gender', choices=get_gender, validators=[InputRequired()], description='Gender',
    render_kw={'class': 'field-data', 'autofocus': ''})
    marital_id = SelectField(label='Marital status', choices=get_marital,validators=[InputRequired()], description='Maritial',
    render_kw={'class': 'field-data', 'autofocus': ''})
    tin = StringField(label='Tax Identification Nº', validators=[length(min=3, max=50)], description='Tax Identification Nº',
    render_kw={'class': 'field-data', 'placeholder': 'Tax Identification Nº..', 'autofocus': ''})
    ssn = StringField(label='Social Security Nº', validators=[length(min=3, max=50)], description='Social Security Nº',                                 
    render_kw={'class': 'field-data', 'placeholder': 'Social Security Nº..', 'autofocus': ''})
    iban = StringField(label='Bank Account Nº', validators=[length(min=3, max=50)], description='Bank Account Nº',                                 
    render_kw={'class': 'field-data', 'placeholder': 'Bank Account Nº..', 'autofocus': ''})

# Job history start form attributes
class Job_History_StartForm(FlaskForm):
    department_id = SelectField(label='Department', choices=get_departments, validators=[InputRequired()], description="Department",
    render_kw={'class': 'field-data', 'autofocus': ""})
    job_id = SelectField(label='Job', coerce=int, validators=[InputRequired()], description='Job',
    render_kw={'class': 'field-data', 'autofocus': ''})
    terms_id = SelectField(label='Terms', choices=get_terms, validators=[InputRequired()], description='Terms',
    render_kw={'class': 'field-data', 'autofocus': ''})
    start_date = DateField(label='Start date', format='%Y-%m-%d', validators=[InputRequired()], description='Start date',
    render_kw={'class': 'field-data', 'autofocus': ''})

# Job history end form attributes
class Job_History_EndForm(FlaskForm):
    end_date = DateField(label='End date', description='End date',
    render_kw={'class': 'field-data', 'autofocus': ''})
    status_id = SelectField(label='Termination motive', choices=get_job_status, validators=[InputRequired()], description='Motive',
    render_kw={'class': 'field-data', 'autofocus': ''})

# Email form attributes
class EmailForm(FlaskForm):
    email = StringField(label='Email', validators=[length(min=3, max=120), Email()], description='Email',
    render_kw={'class': 'field-data', 'placeholder': 'Email..', 'autofocus': ''})
    label = SelectField(label='Label', choices=['Home','Work'], validators=[length(min=3, max=20)], description='Lable',
    render_kw={'class': 'field-data', 'placeholder': 'Email..', 'autofocus': ''})

# Phone form attributes
class PhoneForm(FlaskForm):
    dial_code = SelectField(label='Dial code', choices=get_dial_code ,validators=[InputRequired()], description='Dial code',
    render_kw={'class': 'field-data', 'placeholder': 'Dial code..', 'autofocus': ''})
    phone_number = StringField(label='Phone number', validators=[length(min=3, max=50)], description='Phone number',
    render_kw={'class': 'field-data', 'placeholder': 'Phone number..', 'autofocus': ''})
    label = SelectField(label='Label', choices=['Home','Work','Mobile'], validators=[length(min=3, max=20)], description='Lable',
    render_kw={'class': 'field-data', 'placeholder': 'Email..', 'autofocus': ''})

# Address form attributes
class AddressForm(FlaskForm):
    address1 = StringField(label='Address line 1', validators=[length(min=0, max=50)], description='Address1',
    render_kw={'class': 'field-data', 'placeholder': 'Address line 1..', 'autofocus': ''})
    address2 = StringField(label='Address line 2', validators=[length(min=0, max=50)], description='Address2',
    render_kw={'class': 'field-data', 'placeholder': 'Address line 2..', 'autofocus': ''})
    postal_code = StringField(label='Postal code', validators=[length(min=0, max=50)], description='Postal code',
    render_kw={'class': 'field-data', 'placeholder': 'Postal code..', 'autofocus': ''})
    city = StringField(label='City', validators=[length(min=0, max=50)], description='City',
    render_kw={'class': 'field-data', 'placeholder': 'City..', 'autofocus': ''})
    state = StringField(label='State', validators=[length(min=0, max=50)], description='State',
    render_kw={'class': 'field-data', 'placeholder': 'State..', 'autofocus': ''})
    country_id = SelectField(label='Country', choices=get_country ,validators=[InputRequired()], description='Country',
    render_kw={'class': 'field-data', 'placeholder': 'Country..', 'autofocus': ''})

# Leave balance form attributes
class Leave_BalanceForm(FlaskForm):
    type_id = SelectField(label='Leave type', choices=get_leave_type, validators=[InputRequired()], description="Leave type",
    render_kw={'class': 'field-data', 'autofocus': ""})
    leave_days  = DecimalField(label='Leave days', validators=[InputRequired()], description='Leave days',
    render_kw={'class': 'field-data', 'autofocus': ''})
    expiry_date = DateField(label='Expiry date', validators=[InputRequired()], description="Expiry date",
    render_kw={'class': 'field-data', 'autofocus': ""})

# Leave taken form attributes
class Leave_TakenForm(FlaskForm):
    start_date = DateField(label='Start date', validators=[InputRequired()], description="Start date",
    render_kw={'class': 'field-data', 'autofocus': ""})
    end_date = DateField(label='End date', validators=[InputRequired()], description="End date",
    render_kw={'class': 'field-data', 'autofocus': ""})
    remaining = DecimalField(label='remaining')

    # Validate for end date less than start date
    def validate_end_date(form, field):
        # Calculate timespan
        delta = form.end_date.data - form.start_date.data

        if form.end_date.data < form.start_date.data:
            raise ValidationError("End date must be greater than start date.")
        elif form.remaining.data <= delta.days:
            raise ValidationError(f"Leave time exceeded by {int(delta.days + 1 - form.remaining.data)} day(s).")

# Salary form attributes
class SalaryForm(FlaskForm):
    period_id = SelectField(label='Period', choices=get_period ,validators=[InputRequired()], description='Period',
    render_kw={'class': 'field-data', 'placeholder': 'Period..', 'autofocus': ''})
    gross_value = DecimalField(label='Gross value', validators=[InputRequired()], description='Gross value',
    render_kw={'class': 'field-data', 'autofocus': ''})
    currency_id = SelectField(label='Currency', choices=get_currency ,validators=[InputRequired()], description='Currency',
    render_kw={'class': 'field-data', 'placeholder': 'Currency..', 'autofocus': ''})

# Benefit form attributes
class BenefitForm(FlaskForm):
    period_id = SelectField(label='Period', choices=get_period ,validators=[InputRequired()], description='Period',
    render_kw={'class': 'field-data', 'placeholder': 'Period..', 'autofocus': ''})
    benefit_type_id = SelectField(label='Benefit type', choices=get_benefit_type ,validators=[InputRequired()], description='Benefit type',
    render_kw={'class': 'field-data', 'placeholder': 'Benefit type..', 'autofocus': ''})
    series  = DecimalField(label='Number of times', validators=[InputRequired()], description='Number of times',
    render_kw={'class': 'field-data', 'autofocus': ''})
    gross_value  = DecimalField(label='Gross value', validators=[InputRequired()], description='Gross value',
    render_kw={'class': 'field-data', 'autofocus': ''})
    currency_id = SelectField(label='Currency', choices=get_currency ,validators=[InputRequired()], description='Currency',
    render_kw={'class': 'field-data', 'placeholder': 'Currency..', 'autofocus': ''})

# Time log form attributes
class Time_LogForm(FlaskForm):
    start_time = DateTimeLocalField(label='Start time', validators=[InputRequired()], description="Start time",
    render_kw={'class': 'field-data', 'placeholder': 'YYYY-MM-DH HH:MM:SS..', 'autofocus': ""})
    end_time = DateTimeLocalField(label='End time', validators=[InputRequired()], description="End time",
    render_kw={'class': 'field-data', 'placeholder': 'YYYY-MM-DH HH:MM:SS..', 'autofocus': ""})

# Year month form attributes
class Year_MonthForm(FlaskForm):
    year = SelectField(label='Year', choices=get_years, description='Year',
    render_kw={'class': 'field-data', 'placeholder': 'Year..', 'autofocus': ''})
    month = SelectField(label='Month', choices=get_months, description='Month',
    render_kw={'class': 'field-data', 'placeholder': 'Month..', 'autofocus': ''})


