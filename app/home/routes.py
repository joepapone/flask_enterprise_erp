from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..config import HEADER, ABOUT_TEXT


# Base blueprints
base = Blueprint('base', __name__,
                 template_folder='templates',
                 static_folder='static',
                 static_url_path='/static')


# Index page route
@base.route('/')
def index():
    heading = 'Welcome'
    description = 'Please login to access information'

    return render_template('home/index.html', header=HEADER, heading=heading, description=description)


# Home page route
@base.route('/home')
@login_required
def home():
    heading = 'Welcome {0}'.format(current_user.user_name)
    description = 'You are registered as:'
    data = {'name': current_user.user_name, 'email': current_user.email, 'role': current_user.role}
    
    return render_template('home/home.html', header=HEADER, heading=heading, description=description, data=data)


# About page route
@base.route('/about')
def about():
    heading = 'About'
    description = ABOUT_TEXT

    return render_template('home/about.html', header=HEADER, heading=heading, description=description)

