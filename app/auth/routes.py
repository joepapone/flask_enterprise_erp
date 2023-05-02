from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import login_required, login_user, logout_user
from flask_principal import RoleNeed, Permission, Identity, identity_changed, PermissionDenied, AnonymousIdentity

from .. import db
from ..config import HEADER
from ..admin.users.models import User
from .forms import LoginForm, RegistrationForm
from ..admin.users.forms import UserForm


auth = Blueprint('auth', __name__,
    template_folder='templates',
    static_folder='static')


# Create a permission with a single Need (RoleNeed)
admin_permission = Permission(RoleNeed('admin'))


@auth.route('/login', methods=('GET', 'POST'))
def login():
    # Set html page heading
    heading='Login'

    # Create form instance
    form = LoginForm()
    if form.validate_on_submit():
        # Add authenticated user to current session
        login_user(form.user, remember=form.remember)

        # Inform Flask-Principal the identity changed
        identity_changed.send(current_app._get_current_object(), identity=Identity(form.user.email))

        return redirect(request.args.get("next") or url_for("main.home"))
    return render_template('auth/login.html', header=HEADER, heading=heading, form=form)


@auth.route('/logout')
@login_required
def logout():
    # Remove user from current session 
    logout_user()

    # Inform Flask-Principal user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    return redirect(url_for('main.index'))


@auth.route('/admin')
@login_required
def admin():
    # Set html page heading
    heading='User list'

    # Create model instance with query data
    users = User.query.all()

    return render_template('auth/admin.html', header=HEADER, heading=heading, users=users)


@auth.route('/register', methods=('GET', 'POST'))
@login_required
def register():
    # Set html page heading
    heading='Register'

    # Create form instance
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create model instance with query data
        user = User()

        # Populate object attributes with form data.
        form.populate_obj(user)

        # Marked for insertion
        db.session.add(user)

        # Commit changes to database
        db.session.commit()
        flash('New user {0} successfully submitted'.format(user.user_name))
        return redirect(url_for('auth.admin'))

    return render_template('auth/register.html', header=HEADER, heading=heading, form=form)


@auth.route('/modify/user<id>', methods=('GET', 'POST'))
@login_required
def modify(id):
    # Set html page heading
    heading='Modify credentials'

    # Create model instance with query data
    user = User.query.get(id)

    if user == None:
        # Report result.        
        flash('Error - User id: {0} not found!'.format(id))
        return redirect(url_for('auth.admin'))

    # Create form instance and load it with object data
    form = UserForm(obj=user)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(user)

        # Commit changes to database
        db.session.commit() 
        flash('User {0} modifications successfully submitted'.format(user.user_name))
        return redirect(url_for('auth.admin'))

    return render_template('auth/modify.html', header=HEADER, heading=heading, form=form)


@auth.route('/delete/user<id>', methods=('GET', 'POST'))
@login_required
def delete(id):
    # Create model instance with query data
    user = User.query.get(id)

    if user == None:
        # Report result.        
        flash('Error - User id: {0} not found!'.format(id))
    
    else:
        # Marked for deletion
        db.session.delete(user)

        # Commit changes to database
        db.session.commit()
        flash('User {0} successfully deleted!'.format(user.name))

    return redirect(url_for('auth.admin'))


@auth.errorhandler(PermissionDenied)
def handle_error(e):
    flash('Error - Admin privileges required')
    return redirect(url_for('main.home'))

#@admin_permission.require()