from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..config import HEADER, ABOUT_TEXT


main = Blueprint('main', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/main/static')


@main.route('/')
def index():
    heading = 'About'
    #description = ABOUT_TEXT

    return render_template('main/index.html', header=HEADER, heading=heading)


@main.route('/home')
@login_required
def home():
    heading = 'Welcome {0}'.format(current_user.user_name)
    description = 'You are registered as:'
    data = {'name': current_user.user_name, 'email': current_user.email, 'role': current_user.role}
    
    return render_template('main/home.html', header=HEADER, heading=heading, description=description, data=data)


@main.context_processor
def looged_user():
    return dict(user=current_user.user_name, role=current_user.role)