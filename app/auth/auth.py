from flask_login import LoginManager, current_user
from flask_principal import RoleNeed, UserNeed
from ..user.models import User


login_manager = LoginManager()
# Defined login view
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    '''
    Method for Flask Login load user listener
    '''
    print(f'Login manager: user ID-{user_id}')
    return User.query.get(user_id)


def on_identity_loaded(sender, identity):
    '''
    Method for Flask Principal identity load listener
    '''
    # Set identity user object
    identity.user = current_user
    print(f'Identity: {identity.user}')

    #  Add UserNeed to identity
    if hasattr(current_user, 'user_id'):
        identity.provides.add(UserNeed(current_user.user_id))

    # Update identity with role provided by user
    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role))
    
    
    print(f'User: {current_user.email}, Role: {current_user.role}')
    #print(f'User: {identity.}, Role: {current_user.role}')


    '''
    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))
    '''