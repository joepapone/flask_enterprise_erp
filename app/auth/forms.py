from flask_wtf import FlaskForm
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from wtforms import fields
from wtforms.validators import Email, InputRequired, ValidationError
from ..user.models import User


# From attributes
class LoginForm(FlaskForm):
    email = fields.StringField(label='Email', validators=[InputRequired(), Email()], description="User email",
        render_kw={'class': 'field-data', 'placeholder': 'Email..', 'autofocus': ""})
    password = fields.PasswordField(label='Password', validators=[InputRequired()], description="User password",
        render_kw={'class': 'field-data', 'placeholder': 'Password..'})
    remember = fields.BooleanField(label='Remember Me', description="Remember me",
        render_kw={'class': 'field-label', 'type': 'checkbox'})

    # Validator will run after all validators have passed
    def validate_password(form, field):
        try:
            user = User.query.filter(User.email == form.email.data).one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("Invalid user")
        if user is None:
            raise ValidationError("Invalid user")
        if not user.is_valid_password(form.password.data):
            raise ValidationError("Invalid password")

        # Assign user
        form.user = user