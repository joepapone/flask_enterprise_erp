from flask_login import LoginManager, current_user
from flask_principal import RoleNeed, UserNeed

from ..admin.users.models import User


login_manager = LoginManager()
login_manager.login_view = 'auth.login'

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
    if hasattr(current_user, 'role_id'):
        identity.provides.add(RoleNeed(current_user.role_id))