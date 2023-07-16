from flask import Blueprint, flash, redirect, render_template, url_for, request, current_app
from flask_login import login_required, current_user
from flask_principal import RoleNeed, Permission, PermissionDenied

from .. import db
from ..config import HEADER
from .models import User
from .forms import UserForm, ChangePasswordForm


user = Blueprint('user', __name__,
                 template_folder='templates',
                 static_folder='static',
                 static_url_path='/static')


# Create a permission with a single Need (RoleNeed)
admin_permission = Permission(RoleNeed('Admin'))


# Permission denied error handler
@user.errorhandler(PermissionDenied)
def handle_error(e):
    flash('Error - Admin privileges required')
    return redirect(url_for('root.home'))


# User list
@user.route('/user/list')
@login_required
@admin_permission.require()
def list():
    # Set html page heading
    heading='Users'

    # Create model instance with query data
    list = User.query.all()

    return render_template('user/list.html', header=HEADER, heading=heading, list=list)


# User add
@user.route('/user/add', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def add():
    # Set html page heading
    heading='Add user'

    # Create form instance
    form = UserForm()
    if form.validate_on_submit():
        # Create model instance with query data
        item = User()

        # Populate object attributes with form data.
        form.populate_obj(item)

        # Marked for insertion
        db.session.add(item)

        # Commit changes to database
        db.session.commit()
        flash('User {0} added successfully!'.format(item.user_name))
        return redirect(url_for('user.list'))
    
    return render_template('user/form.html', header=HEADER, heading=heading, form=form)


# User edit
@user.route('/user/edit/<int:id>', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def edit(id):
    # Set html page heading
    heading='Edit user'

    # Create model instance with query data
    item = User.query.get(id)

    if item == None:
        # Report result.        
        flash('Error - User id: {0} not found!'.format(id))
        return redirect(url_for('user.list'))

    # Create form instance and load it with object data
    form = UserForm(obj=item)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(item)

        # Commit changes to database
        db.session.commit() 
        flash('User {0} edited successfully!'.format(item.user_name))
        return redirect(url_for('user.list'))

    return render_template('user/form.html', header=HEADER, heading=heading, form=form)


# User delete
@user.route('/user/delete/<int:id>', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def delete(id):
    # Create model instance with query data
    item = User.query.get(id)

    if item == None:
        # Report result.        
        flash('Error - User id: {0} not found!'.format(id))
    
    else:
        # Marked for deletion
        db.session.delete(item)

        # Commit changes to database
        db.session.commit()
        flash('User {0} successfully deleted!'.format(item.user_name))

    return redirect(url_for('user.list'))


# User profile
@user.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    # Set html page heading
    heading='Profile'

    # User profile
    description = 'You are registered as:'
    data = {'name': current_user.user_name, 'email': current_user.email, 'role': current_user.role}
    
    return render_template('user/profile.html', header=HEADER, heading=heading, description=description, data=data)


# User reset
@user.route('/reset', methods=["GET", "POST"])
@login_required
def reset():
    # Set html page heading
    heading='Change password'

    # Get current user id
    id = current_user.user_id

    # Create model instance with query data
    item = User.query.get(id)

    if item == None:
        # Report result.        
        flash('Error - User id: {0} not found!'.format(id))
        return redirect(url_for('user.list'))

    # Create form instance and load it with object data
    form = ChangePasswordForm(obj=item)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(item)

        # Commit changes to database
        db.session.commit() 
        flash('User {0} passwaord changed successfully!'.format(item.user_name))
        return redirect(url_for('root.home'))

    return render_template('user/reset.html', header=HEADER, heading=heading, form=form)