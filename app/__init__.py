__author__ = 'Jose Ferreira'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal, identity_loaded

# initize SQLAlchemy for use in models
db = SQLAlchemy()

# Application factory function.
def create_app():
    app = Flask(__name__)

    #app.config.from_object(config_class)
    app.config["DEBUG"] = False
    app.config['SECRET_KEY'] = 'YFa91!cTb#' # Generate via terminal: $ python3 -c "import uuid; print(uuid.uuid4().hex)"
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost/business_erp'
    #                                             username:password@host:port/database
    app.config['WTF_CSRF_SECRET_KEY'] = 'YFa91!cTb#'


    # add Flask-WTForms CSRF Protection
    #CSRFProtect(app)


    # initialize Flask-SQLAlchemy
    db.init_app(app)
    #with app.app_context():
    #    db.create_all()


    # initialize Flask-Principal
    from .main.authentication import on_identity_loaded
    Principal(app)
    identity_loaded.connect(on_identity_loaded, app)


    # initialize Flask-Login
    from .main.authentication import login_manager
    login_manager.init_app(app)

    
    # initialize Flask-Mail
    #mail.init_app(app)


    # blueprint for main non-authenticated routes
    from .main.routes import main
    app.register_blueprint(main)


    # blueprint for users routes
    from .auth.routes import auth
    app.register_blueprint(auth)


    # blueprint for user roles routes
    from .admin.roles.routes import roles
    app.register_blueprint(roles)


    # blueprint for users routes
    from .admin.users.routes import users
    app.register_blueprint(users)


    # blueprint for scale routes
    from .scale.routes import scale
    app.register_blueprint(scale)


    # blueprint for errors routes
    from .errors.handlers import errors, page_not_found, internal_server_error
    app.register_blueprint(errors)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    

    return app