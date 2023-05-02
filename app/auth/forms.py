from flask_wtf import FlaskForm
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from wtforms import fields
from wtforms.validators import Email, InputRequired, ValidationError
from ..admin.users.models import User


class LoginForm(FlaskForm):
    email = fields.StringField(label='Email', validators=[InputRequired(), Email()], description="User email",
        render_kw={'class': 'field-data', 'placeholder': 'Email..', 'autofocus': ""})
    password = fields.PasswordField(label='Password', validators=[InputRequired()], description="User password",
        render_kw={'class': 'field-data', 'placeholder': 'Password..'})
    remember = fields.BooleanField(label='Remember Me', description="Remember me",
        render_kw={'class': 'field-label', 'type': 'checkbox'})

    # validator will run after all validators have passed
    def validate_password(form, field):
        try:
            user = User.query.filter(User.email == form.email.data).one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("Invalid user")
        if user is None:
            raise ValidationError("Invalid user")
        if not user.is_valid_password(form.password.data):
            raise ValidationError("Invalid password")

        # assign user
        form.user = user


class RegistrationForm(FlaskForm):
    role = fields.SelectField(label='Role', validators=[InputRequired()], description="User role",
        render_kw={'class': 'field-data', 'autofocus': ""})
    email = fields.StringField(label='Email', validators=[InputRequired(), Email()], description="User email",
        render_kw={'class': 'field-data', 'placeholder': 'Email..'})
    name = fields.StringField(label='Name', validators=[InputRequired()], description="User name",
        render_kw={'class': 'field-data', 'placeholder': 'Name..'})
    password = fields.PasswordField(label='Password', validators=[InputRequired()], description="User password",
        render_kw={'class': 'field-data', 'placeholder': 'Password..'})

    def validate_email(form, field):
        user = User.query.filter(User.email == field.data).first()
        if user is not None:
            raise ValidationError("A member with that email already exists")


'''
class UserForm(FlaskForm):
    role = fields.SelectField(label='Role', validators=[InputRequired()], choices=[('member', 'Member'), ('admin', 'Admin')],
        render_kw={'class': 'field-data', 'autofocus': ""})
    name = fields.StringField(label='Name', validators=[InputRequired()], description="Member name",
        render_kw={'class': 'field-data', 'placeholder': 'Name..'})
    password = fields.PasswordField(label='Password', validators=[InputRequired()], description="Member password",
        render_kw={'class': 'field-data', 'placeholder': 'Password..'})

    def validate_email(form, field):
        user = User.query.filter(User.email == field.data).first()
        if user is not None:
            raise ValidationError("A member with that email already exists")
'''