from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import login_required, login_user, logout_user
from flask_principal import Identity, identity_changed, AnonymousIdentity
from .auth import timed_serializer

from ..config import HEADER
from ..user.models import User
from .forms import LoginForm


auth = Blueprint('auth', __name__,
                 url_prefix='/home',
                 template_folder='templates',
                 static_folder='static',
                 static_url_path='/static')


@auth.route('/login', methods=('GET', 'POST'))
def login():
    # Set html page heading
    heading='Login'

    # Create form instance
    form = LoginForm()

    # Validate form input
    if form.validate_on_submit():
        # Create model instance with query data
        user = User.query.filter(User.email == form.email.data).first()

        print(f'Login user: {user}')

        # Validate password
        if user.is_valid_password(form.password.data):
            # Add user to session with Flask-Login
            login_user(user, remember=form.remember.data)

            # Inform Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.user_id))

            #return redirect(request.args.get('next') or '/')
            return redirect(request.args.get("next") or url_for("base.home"))

        flash('Error - Invalid user or password!')

        #return redirect(request.args.get("next") or url_for("main.home"))
    return render_template('auth/login.html', header=HEADER, heading=heading, form=form)


@auth.route('/logout')
@login_required
def logout():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    #for key in ('identity.name', 'identity.auth_type'):
    #    db.session.pop(key, None)

    # Inform Flask-Principal user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    return redirect(request.args.get('next') or '/')