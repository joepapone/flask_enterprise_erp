__author__ = 'Jose Ferreira'

import os
from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal, identity_loaded
from .config import DEBUG, SECRET_KEY, DATABASE_URI, WTF_CSRF, HEADER

# Initize SQLAlchemy for use in models
db = SQLAlchemy()

# Application factory function.
def create_app():
    app = Flask(__name__)

    #app.config.from_object(config_class)
    # Application configuration
    app.config['DEBUG'] = DEBUG
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI                              
    app.config['WTF_CSRF_SECRET_KEY'] = WTF_CSRF

    # Set static file path
    app.root_path = app.root_path + '/home'


    # add Flask-WTForms CSRF Protection
    #CSRFProtect(app)


    # Initialize Flask-SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()


    # Initialize Flask-Principal
    from .admin.auth import on_identity_loaded
    Principal(app)
    identity_loaded.connect(on_identity_loaded, app)


    # Initialize Flask-Login
    from .admin.auth import login_manager
    login_manager.init_app(app)


    '''
    @app.before_request
    def before_request():
        g.user = 'test dumb' in request.headers
        g.header = HEADER
        print("before_request executing!")
        #g.pjax = 'X-PJAX' @app.before_request in request.headers
    '''



        #return dict(user=user, role=role)


    # initialize Flask-Mail
    #mail.init_app(app)


    # Blueprint for root routes
    from .home.routes import root, page_not_found, internal_server_error
    app.register_blueprint(root)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    # Blueprint for admin routes
    from .admin.routes import admin
    app.register_blueprint(admin)

    # Blueprint for human resources routs
    from .hr.routes import hr
    app.register_blueprint(hr)
    
    return app

