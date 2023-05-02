from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import ValidationError
from .models import Role


# Validate for length
def length(min=-1, max=-1):
    message = 'Must be between %d and %d characters long.' % (min, max)

    def _length(form, field):
        l = field.data and len(field.data) or 0
        if l < min or max != -1 and l > max:
            raise ValidationError(message)

    return _length


# Validate for duplicates
def duplicate(form, field):
    item = Role.query.filter(Role.role_attribute == field.data).first()
    if item is not None:
        raise ValidationError("Role attribute already exists")


# From attributes
class RoleForm(FlaskForm):
    role_attribute = fields.StringField(label='Role attribute', validators=[length(min=3, max=50), duplicate], description='Role attribute',
        render_kw={'class': 'field-data', 'placeholder': 'Role attribute..', 'autofocus': ""})