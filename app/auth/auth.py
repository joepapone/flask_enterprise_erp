from flask_login import LoginManager, current_user
from flask_principal import RoleNeed, UserNeed
from itsdangerous import URLSafeTimedSerializer
from ..user.models import User
from ..config import SECRET_KEY


# Create instance of LoginManager
login_manager = LoginManager()
# Defined login view
login_manager.login_view = 'auth.login'

# URL safe timed serializer ??? email to reset password
timed_serializer = URLSafeTimedSerializer(SECRET_KEY)


@login_manager.user_loader
def load_user(user_id):
    '''
    Method for Flask Login load user listener
    '''
    return User.query.get(user_id)


def on_identity_loaded(sender, identity):
    '''
    Method for Flask Principal identity load listener
    '''
    # Set identity user object
    identity.user = current_user

    #  Add UserNeed to identity
    if hasattr(current_user, 'user_id'):
        identity.provides.add(UserNeed(current_user.user_id))

    # Update identity with role provided by user
    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(str(current_user.role)))
    


    '''
    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))
    '''