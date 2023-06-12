from flask import Blueprint, flash, redirect, render_template, url_for, request, current_app
from flask_login import login_required
from flask_principal import RoleNeed, Permission, PermissionDenied

from .. import db
from ..app import HEADER
from .models import Role
from .forms import RoleForm


role = Blueprint('role', __name__,
                 template_folder='templates',
                 static_folder='static',
                 static_url_path='/static')


# Create a permission with a single Need (RoleNeed)
admin_permission = Permission(RoleNeed('Admin'))


# Permission denied error handler
@role.errorhandler(PermissionDenied)
def handle_error(e):
    flash('Error - Admin privileges required')
    return redirect(url_for('root.home'))


# Role list
@role.route('/role/list')
@login_required
@admin_permission.require()
def list():
    # Set html page heading
    heading='Roles'

    # Create model instance with query data
    list = Role.query.all()

    return render_template('role/list.html', header=HEADER, heading=heading, list=list)


# Role add
@role.route('/role/add', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def add():
    # Set html page heading
    heading='Add role'

    # Create form instance
    form = RoleForm()
    if form.validate_on_submit():
        # Create model instance with query data
        item = Role(None,None)

        # Populate object attributes with form data.
        form.populate_obj(item)

        # Marked for insertion
        db.session.add(item)

        # Commit changes to database
        db.session.commit()
        flash('Role {0} added successfully!'.format(item.role_name))
        return redirect(url_for('role.list'))
    
    return render_template('role/form.html', header=HEADER, heading=heading, form=form)


# Role edit
@role.route('/role/edit/<int:id>', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def edit(id):
    # Set html page heading
    heading='Edit role'

    # Create model instance with query data
    item = Role.query.get(id)

    if item == None:
        # Report result.        
        flash('Error - Role id: {0} not found!'.format(id))
        return redirect(url_for('role.list'))

    # Create form instance and load it with object data
    form = RoleForm(obj=item)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(item)

        # Commit changes to database
        db.session.commit() 
        flash('Role {0} edited successfully!'.format(item.role_name))
        return redirect(url_for('role.list'))

    return render_template('role/form.html', header=HEADER, heading=heading, form=form)


# Role delete
@role.route('/role/delete/<int:id>', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def delete(id):
    # Create model instance with query data
    item = Role.query.get(id)

    if item == None:
        # Report result.        
        flash('Error - Role id: {0} not found!'.format(id))
    
    else:
        # Marked for deletion
        db.session.delete(item)

        # Commit changes to database
        db.session.commit()
        flash('Role {0} successfully deleted!'.format(item.role_name))

    return redirect(url_for('role.list'))


