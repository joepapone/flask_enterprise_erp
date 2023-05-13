from flask import Blueprint, render_template
from ..app import HEADER


errors = Blueprint('errors', __name__,
    template_folder='templates')


# page not found error template
@errors.errorhandler(404)
def page_not_found(error):
    heading = f'{404} - Page not found!'
    description = error

    return render_template('errors/404.html', header=HEADER, heading=heading, description=description), 404


# internal server error template
@errors.errorhandler(500)
def internal_server_error(error):
    heading = f'{500} - Internal server error!'
    description = error

    return render_template('errors/500.html', header=HEADER, heading=heading, description=description), 500
