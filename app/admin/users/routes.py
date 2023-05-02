from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import login_required
from flask_principal import RoleNeed, Permission, PermissionDenied

from ... import db
from ...config import HEADER
from .models import User
from .forms import UserForm


users = Blueprint('users', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/main/static')


# Create a permission with a single Need (RoleNeed)
admin_permission = Permission(RoleNeed('admin'))


#@admin_permission.require()


@users.route('/user/list')
@login_required
def list():
    # Set html page heading
    heading='Users'

    # Create model instance with query data
    list = User.query.all()

    return render_template('user_list.html', header=HEADER, heading=heading, list=list)


@users.route('/user/add', methods=('GET', 'POST'))
@login_required
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
        return redirect(url_for('users.list'))
    
    return render_template('user_form.html', header=HEADER, heading=heading, form=form)


@users.route('/user/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    # Set html page heading
    heading='Edit user'

    # Create model instance with query data
    item = User.query.get(id)

    if item == None:
        # Report result.        
        flash('Error - User id: {0} not found!'.format(id))
        return redirect(url_for('users.list'))

    # Create form instance and load it with object data
    form = UserForm(obj=item)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(item)

        # Commit changes to database
        db.session.commit() 
        flash('User {0} edited successfully!'.format(item.user_name))
        return redirect(url_for('users.list'))

    return render_template('user_form.html', header=HEADER, heading=heading, form=form)


@users.route('/user/delete/<int:id>', methods=('GET', 'POST'))
@login_required
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

    return redirect(url_for('users.list'))


@users.errorhandler(PermissionDenied)
def handle_error(e):
    flash('Error - Admin privileges required')
    return redirect(url_for('main.home'))