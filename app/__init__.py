__author__ = 'Jose Ferreira'

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
    app.config["DEBUG"] = DEBUG
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI                              
    app.config['WTF_CSRF_SECRET_KEY'] = WTF_CSRF


    # add Flask-WTForms CSRF Protection
    #CSRFProtect(app)


    # Initialize Flask-SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()


    # Initialize Flask-Principal
    from .auth.auth import on_identity_loaded
    Principal(app)
    identity_loaded.connect(on_identity_loaded, app)


    # Initialize Flask-Login
    from .auth.auth import login_manager
    login_manager.init_app(app)



    @app.before_request
    def before_request():
        g.user = 'test dumb' in request.headers
        g.header = HEADER
        print("before_request executing!")
        #g.pjax = 'X-PJAX' @app.before_request in request.headers




        #return dict(user=user, role=role)


    # initialize Flask-Mail
    #mail.init_app(app)


    # Blueprint for errors routes
    from .errors.routes import errors, page_not_found, internal_server_error
    app.register_blueprint(errors)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    # Blueprint for non-authenticated routes
    from .routes import root
    app.register_blueprint(root)

    # Blueprint authentication routes
    from .auth.routes import auth
    app.register_blueprint(auth)
    
    # Blueprint for role and user routes
    from .role.routes import role
    app.register_blueprint(role)
    from .user.routes import user
    app.register_blueprint(user)

    # Blueprint for admin routes
    from .admin.routes import admin
    app.register_blueprint(admin)

    # Blueprint for human resources routs
    from .hr.routes import hr
    app.register_blueprint(hr)


    
    return app