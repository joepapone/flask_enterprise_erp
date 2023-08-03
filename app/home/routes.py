from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..config import HEADER, ABOUT_TEXT


# Base blueprints
root = Blueprint('root', __name__,
                 template_folder='templates',
                 static_folder='static',
                 static_url_path='/static')


# Index page route
@root.route('/')
def index():
    heading = 'Hello,'
    title = 'Login required!'
    description = '''Please hover over the icon on the top right hand corner of the page, and click on the login menu.
                     Insert your user name and password to access the ERP Enterprise webserver application.
                  '''

    return render_template('home/index.html', header=HEADER, heading=heading, title=title, description=description)


# Home page route
@root.route('/home')
@login_required
def home():
    # Set html page menus
    menus=[{'link': '/admin/dashboard', 'text': ' ❱ Admin'},
           {'link': '/hr/dashboard', 'text': ' ❱ Human Resources'}]

    heading = 'Home'
    title = f'Hi {current_user.user_name},'
    description = "It's nice to have you back!."
    
    return render_template('home/home.html', header=HEADER, menus=menus, heading=heading, title=title, description=description)


# About page route
@root.route('/about')
def about():
    heading = 'About'
    description = ABOUT_TEXT

    return render_template('home/about.html', header=HEADER, heading=heading, description=description)


# Page not found error route
@root.errorhandler(404)
def page_not_found(error):
    # Set html page menus
    menus=[{'link': '/', 'text': ' ❰ Back'}]

    # Set html page heading
    heading = f'{404} - Page not found!'

    return render_template('home/404.html', header=HEADER, menus=menus, heading=heading, error=error), 404


# Internal server error route
@root.errorhandler(500)
def internal_server_error(error):
    # Set html page menus
    menus=[{'link': '/', 'text': ' ❰ Back'}]

    # Set html page heading
    heading = f'{500} - Internal server error!'
    
    return render_template('home/500.html', header=HEADER, menus=menus, heading=heading, error=error), 500