from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.fields import StringField, TextAreaField, DecimalField, SelectField, DateField, DateTimeField, BooleanField, PasswordField
from wtforms.validators import Email, InputRequired, ValidationError, EqualTo
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from .models import User, Role
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

# Validate for duplicates
def duplicate(form, field):
    item = Role.query.filter(Role.role_name == field.data).first()
    if item is not None:
        raise ValidationError("Role name already exists")
    

# ------------------------------------------------
#    Data collection and Processing
# ------------------------------------------------

# Get roles to populate select field
def get_roles():
    role_list = [(row.role_id, row.role_name) for row in db.session.execute(db.select(Role)).scalars().all()]

    return role_list


# ------------------------------------------------
#    Flask Forms
# ------------------------------------------------

# Role from attributes
class RoleForm(FlaskForm):
    role_name = StringField(label='Name', validators=[length(min=3, max=50), duplicate], description="Role name",
    render_kw={'class': 'field-data', 'placeholder': 'Name..', 'autofocus': ""})

# User form attributes
class UserForm(FlaskForm):  
    user_name = StringField(label='Name', validators=[length(min=3, max=50)], description="User name",
        render_kw={'class': 'field-data', 'placeholder': 'Name..'})
    role_id = SelectField(label='Role', choices=get_roles ,validators=[InputRequired()], description="User role",
        render_kw={'class': 'field-data', 'autofocus': ""})
    email = StringField(label='Email', validators=[length(min=3, max=120), Email()], description="User email",
        render_kw={'class': 'field-data', 'placeholder': 'Email..'})

    def validate_email(form, field):
        user = User.query.filter(User.email == field.data).first()
        if user is not None:
            raise ValidationError("A user with that email already exists")
        
# Login from attributes
class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[InputRequired(), Email()], description="User email",
        render_kw={'class': 'field-data', 'placeholder': 'Email..', 'autofocus': ""})
    password = PasswordField(label='Password', validators=[InputRequired()], description="User password",
        render_kw={'class': 'field-data', 'placeholder': 'Password..'})
    remember = BooleanField(label='Remember Me', description="Remember me",
        render_kw={'class': 'field-label', 'type': 'checkbox'})

    # Validator will run after all validators have passed
    def validate_password(form, field):
        try:
            user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalars().one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("Invalid user")
        if user is None:
            raise ValidationError("Invalid user")
        if not user.is_valid_password(form.password.data):
            raise ValidationError("Invalid password")

        # Assign user
        form.user = user

# Change password form attributes
class ChangePasswordForm(FlaskForm):
    current = PasswordField(label='Current password', validators=[length(min=3, max=50)], description="Current password",
    render_kw={'class': 'field-data', 'placeholder': 'Current password..'})
    password = PasswordField(label='New password', validators=[length(min=3, max=50), EqualTo('confirm', message='Passwords must match')], description="New password",
    render_kw={'class': 'field-data', 'placeholder': 'New password..'})
    confirm = PasswordField(label='Confirm', validators=[length(min=3, max=50), EqualTo('password', message='Passwords must match')], description="Confirm password",
    render_kw={'class': 'field-data', 'placeholder': 'Confirm password..'})

    # Validator will run after all validators have passed
    def validate_password(form, field):
        try:
            user = db.session.get(User, current_user.user_id)
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("Invalid user")
        if user is None:
            raise ValidationError("Invalid user")
        if not user.is_valid_password(form.current.data):
            raise ValidationError("Invalid password")

