from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import login_required
from flask_principal import RoleNeed, Permission, PermissionDenied

from ... import db
from ...config import HEADER
from .models import Role
from .forms import RoleForm


roles = Blueprint('roles', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/main/static')


# Create a permission with a single Need (RoleNeed)
admin_permission = Permission(RoleNeed('admin'))


#@admin_permission.require()


@roles.route('/role/list')
@login_required
def list():
    # Set html page heading
    heading='Roles'

    # Create model instance with query data
    list = Role.query.all()

    return render_template('role_list.html', header=HEADER, heading=heading, list=list)


@roles.route('/role/add', methods=('GET', 'POST'))
@login_required
def add():
    # Set html page heading
    heading='Add role'

    # Create form instance
    form = RoleForm()
    if form.validate_on_submit():
        # Create model instance with query data
        item = Role()

        # Populate object attributes with form data.
        form.populate_obj(item)

        # Marked for insertion
        db.session.add(item)

        # Commit changes to database
        db.session.commit()
        flash('Role {0} added successfully!'.format(item.role_attribute))
        return redirect(url_for('roles.list'))
    
    return render_template('role_form.html', header=HEADER, heading=heading, form=form)


@roles.route('/role/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    # Set html page heading
    heading='Edit role'

    # Create model instance with query data
    item = Role.query.get(id)

    if item == None:
        # Report result.        
        flash('Error - Role id: {0} not found!'.format(id))
        return redirect(url_for('roles.list'))

    # Create form instance and load it with object data
    form = RoleForm(obj=item)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(item)

        # Commit changes to database
        db.session.commit() 
        flash('Role {0} edited successfully!'.format(item.role_attribute))
        return redirect(url_for('roles.list'))

    return render_template('role_form.html', header=HEADER, heading=heading, form=form)


@roles.route('/role/delete/<int:id>', methods=('GET', 'POST'))
@login_required
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
        flash('Role {0} successfully deleted!'.format(item.role_attribute))

    return redirect(url_for('roles.list'))


@roles.errorhandler(PermissionDenied)
def handle_error(e):
    flash('Error - Admin privileges required')
    return redirect(url_for('main.home'))