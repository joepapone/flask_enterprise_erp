__author__ = 'Jose Ferreira'

from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal, identity_loaded
from .config import HEADER

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
    from .auth.auth import on_identity_loaded
    Principal(app)
    identity_loaded.connect(on_identity_loaded, app)


    # initialize Flask-Login
    from .auth.auth import login_manager
    login_manager.init_app(app)



    @app.before_request
    def before_request():
        g.user = 'test dumb' in request.headers
        g.header = HEADER
        print("before_request executing!")
        #g.pjax = 'X-PJAX' @app.before_request in request.headers


    # initialize Flask-Mail
    #mail.init_app(app)


    # blueprint for non-authenticated routes
    from .routes import root
    app.register_blueprint(root)

    # blueprint authentication routes
    from .auth.routes import auth
    app.register_blueprint(auth)
    
    # blueprint for role and user routes
    from .role.routes import role
    app.register_blueprint(role)

    from .user.routes import user
    app.register_blueprint(user)

    # blueprint for errors routes
    from .errors.routes import errors, page_not_found, internal_server_error
    app.register_blueprint(errors)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    
    return app