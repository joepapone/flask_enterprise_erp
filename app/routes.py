from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .app import HEADER, ABOUT_TEXT


root = Blueprint('root', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static')


@root.route('/')
def index():
    heading = 'Welcome'
    description = 'Please login to access information'

    return render_template('index.html', header=HEADER, heading=heading, description=description)


@root.route('/home')
@login_required
def home():
    heading = 'Welcome {0}'.format(current_user.user_name)
    #heading = 'Welcome {0}'.format('Bob')
    description = 'You are registered as:'
    data = {'name': current_user.user_name, 'email': current_user.email, 'role': current_user.role}
    #data = {'name': 'bob', 'email': 'bob@gmail.com', 'role': 'Admin'}
    
    return render_template('home.html', header=HEADER, heading=heading, description=description, data=data)


@root.route('/about')
def about():
    heading = 'About'
    description = ABOUT_TEXT

    return render_template('about.html', header=HEADER, heading=heading, description=description)


@root.context_processor
def logged_user():
    return dict(user=current_user.user_name, role=current_user.role)
    #return dict(user='Bob', role='admin')
