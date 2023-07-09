from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import ValidationError, InputRequired
from .models import Department, Job


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

# Department form attributes
class DepartmentForm(FlaskForm):
    department_name = fields.StringField(label='Department', validators=[length(min=3, max=50), department_duplicate], description="Department name",
    render_kw={'class': 'field-data', 'placeholder': 'Name..', 'autofocus': ""})


# Get departments to populate select field
def get_departments():
    list = [(row.department_id, row.department_name) for row in Department.query.all()]

    return list

# Validate department for duplicates
def job_duplicate(form, field):
    item = Job.query.filter(Job.job_title == field.data).first()
    if item is not None:
        raise ValidationError("Job title already exists")

# Job form attributes
class JobForm(FlaskForm):
    department_id = fields.SelectField(label='Department', choices=get_departments ,validators=[InputRequired()], description="Department",
    render_kw={'class': 'field-data', 'autofocus': ""})
    job_title = fields.StringField(label='Job titile', validators=[length(min=3, max=50), job_duplicate], description="Job title",
    render_kw={'class': 'field-data', 'placeholder': 'Title..', 'autofocus': ""})
    job_description = fields.TextAreaField(label='Job description', validators=[length(min=3, max=1000), job_duplicate], description="Job description",
    render_kw={'class': 'field-data', 'rows': 10, 'placeholder': 'Description..', 'autofocus': ""})

