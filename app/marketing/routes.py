from flask import Blueprint, render_template
from flask_login import current_user
from ..app import HEADER, ABOUT_TEXT
from flask_login import login_required
from flask_principal import RoleNeed, Permission, PermissionDenied


marketing = Blueprint('marketing', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static')


@marketing.route('/marketing')
@login_required
def home():
    heading = 'Welcome {0}'.format(current_user.user_name)
    description = 'You are registered as:'
    data = {'name': current_user.user_name, 'email': current_user.email, 'role': current_user.role}
    
    return render_template('marketing/home.html', header=HEADER, heading=heading, description=description, data=data)


@marketing.context_processor
def looged_user():
    return dict(user=current_user.user_name, role=current_user.role)