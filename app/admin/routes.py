from flask import Blueprint, flash, redirect, render_template, url_for, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import Identity, AnonymousIdentity, Permission, PermissionDenied, RoleNeed, identity_changed

from .models import User, Role, Currency, Country, Tax
from .forms import LoginForm, UserForm, RoleForm, ChangePasswordForm
from .auth import timed_serializer
from ..home.charts import angular_gauge, bullet_gauge, double_bullet_gauge, data_cards, line_chart, area_chart, bar_chart, stack_bar_chart, pie_chart, table_chart
from ..config import HEADER
from .. import db

admin = Blueprint('admin', __name__,
                  template_folder='templates',
                  static_folder='static',
                  static_url_path='/static')


# Create a permission with a single Need (RoleNeed)
admin_permission = Permission(RoleNeed('Admin'))


# Set titles
TITLE_CONFIG='configuration'
TITLE_USER='user'
TITLE_ROLE='role'


# Permission denied error handler
@admin.errorhandler(PermissionDenied)
def handle_error(e):
    flash('Error - Admin privileges required')
    return redirect(url_for('root.home'))


# Admin dashboard
@admin.route('/admin/dashboard')
@login_required
@admin_permission.require()
def dashboard():
        # Set html page menus
    menus=[{'link': '/admin/config', 'text': ' ❱ Configurations'},
           {'link': '/admin/user/list', 'text': ' ❱ Users'}]
  
    # Set html page heading
    heading='Admin'

    # Overhead Ratio = Operating Expenses / (Taxable Net Interest Income + Operating Income)
    # Overtime Ratio = (Overtime hours / Regular hours) x 100

    # Table headers
    table1_headers = [["<b>EXPENSES</b>"], ["<b>Q1</b>"], ["<b>Q2</b>"], ["<b>Q3</b>"], ["<b>Q4</b>"]]
    table1_values = [
        ['Salaries', 'Office', 'Merchandise', 'Legal', '<b>TOTAL</b>'],
        [1200000, 20000, 80000, 2000, 12120000],
        [1300000, 20000, 70000, 2000, 130902000],
        [1300000, 20000, 120000, 2000, 131222000],
        [1400000, 20000, 90000, 2000, 14102000]]
    
    table2_headers = [["<b>EXPENSES</b>"], ["<b>Q1</b>"], ["<b>Q2</b>"], ["<b>Q3</b>"], ["<b>Q4</b>"]]
    table2_values = [
        ['Salaries', 'Office', 'Merchandise', 'Legal', '<b>TOTAL</b>'],
        [1200000, 20000, 80000, 2000, 12120000],
        [1300000, 20000, 70000, 2000, 130902000],
        [1300000, 20000, 120000, 2000, 131222000],
        [1400000, 20000, 90000, 2000, 14102000]]
    

    plot1 = angular_gauge('Overhead ratio', 8, 13, [0, 100], None, True, True)
    plot2 = angular_gauge('Overtime ratio', 50, 70, [0, 100], None, True, True)
    plot3 = angular_gauge('Absenteeism', 11, 10, [0, 100], '%', True, True)
    plot4 = data_cards('Revenue per Staff', 1000000, 915000)
    plot5 = bar_chart('Number of Employees', 620, None, ['Mar', 'Apr', 'May', 'Jun', 'Jul'], [750, 850, 630, 700, 620], 'v')
    plot6 = pie_chart('Employee Structure', None, ['Male', 'Female'], [434, 186], 0.6, 'Gender')
    plot7 = bar_chart('Full Time Employees', 600, None, ['Mar', 'Apr', 'May', 'Jun', 'Jul'], [700, 810, 600, 680, 590], 'v')
    plot8 = pie_chart('Employees per Sector', None, ['Administrative','Sales','Production','Maintence'], [20, 256, 320, 24], 0.6, 'Sector')
    plot9 = bar_chart('Salary', '$54.000', None, ['Mar', 'Apr', 'May', 'Jun', 'Jul'], [50, 51, 52, 53, 54], 'v')
    plot10 = area_chart('Education per Head', '$180', None, None, None, None, ['Mar', 'Apr', 'May', 'Jun', 'Jul'], [210, 209, 150, 235, 180])
    plot11 = area_chart('Education per FTE', '$210', None, None, None, None, ['Mar', 'Apr', 'May', 'Jun', 'Jul'], [285, 260, 210, 290, 210])
    plot12 = area_chart('Education spending', '$122', None, None, None, None, ['Mar', 'Apr', 'May', 'Jun', 'Jul'], [156, 139, 113, 150, 122])
    plot13 = table_chart('Other indicatores', 'test1', table1_headers, table1_values )
    plot14 = table_chart('Other indicatores', 'test2', table2_headers, table2_values)
    return render_template('admin/dashboard.html', header=HEADER, menus=menus, heading=heading, 
                           chart1=plot1, chart2=plot2, chart3=plot3, chart4=plot4, chart5=plot5, chart6=plot6, chart7=plot7, chart8=plot8,
                           chart9=plot9, chart10=plot10, chart11=plot11, chart12=plot12, chart13=plot13, chart14=plot14)


# Config
@admin.route('/admin/config')
@login_required
def config():
    # Set html page menus
    menus=[{'link': '/admin/dashboard', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'{TITLE_CONFIG.capitalize()}s'

    # Create model instances with query data
    country = db.session.execute(db.select(Country)).scalars().all()
    currency = db.session.execute(db.select(Currency)).scalars().all()
    tax = db.session.execute(db.select(Tax)).scalars().all()

    return render_template('admin/config.html', header=HEADER, menus=menus, heading=heading, country=country, currency=currency, tax=tax)


# Login form
@admin.route('/login', methods=('GET', 'POST'))
def login():
    # Set html page heading
    heading='Login'

    # Create form instance
    form = LoginForm()

    # Validate form input
    if form.validate_on_submit():
        # Create model instance with query data
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalars().first()

        print(f'Login user: {user} history requeired')

        # Validate password
        if user.is_valid_password(form.password.data):
            # Add user to session with Flask-Login
            login_user(user, remember=form.remember.data)

            # Inform Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.user_id))

            #return redirect(request.args.get('next') or '/')
            return redirect(request.args.get("next") or url_for("root.home"))

        flash('Error - Invalid user or password!')

        #return redirect(request.args.get("next") or url_for("main.home"))
    return render_template('admin/login.html', header=HEADER, heading=heading, form=form)


# Login form
@admin.route('/logout')
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


# User list
@admin.route('/admin/user/list')
@login_required
@admin_permission.require()
def user_list():
    # Set html page menus
    menus=[{'link': '/admin/dashboard', 'text': ' ❰ Back'},
           {'link': '/user/role/list', 'text': ' ❱ Roles'}]

    # Set html page heading
    heading=f'{TITLE_USER.capitalize()}s'

    # Create model instance with query data
    list = db.session.execute(db.select(User).order_by(User.user_name.asc())).scalars().all()

    return render_template('admin/user_list.html', header=HEADER, menus=menus, heading=heading, list=list)


# User index
@admin.route('/user/index', methods=('GET', 'POST'))
@login_required
def user_index():
    # Set html page menus
    menus=[{'link': '/admin/dashboard', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'{TITLE_USER.capitalize()}s'

    # Create model instance with query data
    user_obj = db.session.execute(db.select(User).order_by(User.user_name.asc())).scalars().all()
    role_obj = db.session.execute(db.select(Role).order_by(Role.role_name.asc())).scalars().all()

    return render_template('admin/user_index.html', header=HEADER, menus=menus, heading=heading, user_list=user_obj, role_list=role_obj)


# User add
@admin.route('/user/add', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def user_add():
    # Set html page heading
    heading=f'Add {TITLE_USER}'

    # Create form instance
    form = UserForm()
    if form.validate_on_submit():
        # Create model instance with query data
        obj = User()

        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_USER.capitalize()} ID: {obj.user_id} - {obj.user_name} was successfully added!')

        return redirect(url_for('admin.user_list'))
    
    return render_template('admin/user_form.html', header=HEADER, heading=heading, form=form)


# User edit
@admin.route('/user/edit/<int:user_id>', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def user_edit(user_id):
    # Set html page heading
    heading=f'Edit {TITLE_USER}'

    # Create model instance with query data
    obj = db.session.get(User, user_id)

    if obj == None:
        # Report result.        
        flash(f'Error - The {TITLE_USER} ID: {user_id} was not found!')
        
        return redirect(url_for('admin.list'))

    # Create form instance and load it with object data
    form = UserForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_USER.capitalize()} ID: {obj.user_id} - {obj.user_name} was successfully edited!')

        return redirect(url_for('admin.user_list'))

    return render_template('admin/user_form.html', header=HEADER, heading=heading, form=form)


# User delete
@admin.route('/user/delete/<int:user_id>', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def user_delete(user_id):
    # Create model instance with query data
    obj = db.session.get(User, user_id)

    if obj == None:
        # Report result.        
        flash(f'Error - The {TITLE_USER} ID: {user_id} was not found!')
    
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_USER.capitalize()} ID: {obj.user_id} - {obj.user_name} was successfully deleted!')

    return redirect(url_for('admin.user_list'))


# User profile
@admin.route('/user/profile', methods=["GET", "POST"])
@login_required
def profile():
    # Set html page menus
    menus=[{'link': '/home', 'text': ' ❱ Home'},
           {'link': '/user/reset', 'text': ' ❱ Change password'}]

    # Set html page heading
    heading=f'{TITLE_USER.capitalize()} profile'

    # User profile
    description = 'You are registered as:'
    data = {'name': current_user.user_name, 'email': current_user.email, 'role': current_user.role}
    
    return render_template('admin/profile.html', header=HEADER, menus=menus, heading=heading, description=description, data=data)


# User reset
@admin.route('/user/password_reset', methods=["GET", "POST"])
@login_required
def password_reset():
    # Set html page menus
    menus=[{'link': '/user/profile', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Change password'

    # Get current user id
    user_id = current_user.user_id

    # Create model instance with query data
    obj = db.session.get(User, user_id)

    if obj == None:
        # Report result.        
        flash(f'Error - The {TITLE_USER} ID: {user_id} was not found!')
        return redirect(url_for('admin.user_index'))

    # Create form instance and load it with object data
    form = ChangePasswordForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_USER.capitalize()} ID: {obj.user_id} - {obj.user_name} password was successfully edited!')

        return redirect(url_for('root.home'))

    return render_template('admin/reset.html', header=HEADER, menus=menus, heading=heading, form=form)


# Role list
@admin.route('/user/role/list', methods=('GET', 'POST'))
@login_required
def role_list():
    # Set html page menus
    menus=[{'link': '/admin/dashboard', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'{TITLE_USER.capitalize()}s'

    # Create model instance with query data
    role_obj = db.session.execute(db.select(Role).order_by(Role.role_name.asc())).scalars().all()

    return render_template('admin/role_index.html', header=HEADER, menus=menus, heading=heading, role_list=role_obj)


# Role add
@admin.route('/user/role/add', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def role_add():
    # Set html page heading
    heading=f'Add {TITLE_ROLE}'

    # Create form instance
    form = RoleForm()
    if form.validate_on_submit():
        # Create model instance with query data
        #obj = Role(None,None)
        obj = Role()

        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_ROLE.capitalize()} ID: {obj.role_id} - {obj.role_name} was successfully added!')

        return redirect(url_for('admin.role_index'))
    
    return render_template('role/role_form.html', header=HEADER, heading=heading, form=form)


# Role edit
@admin.route('/user/role/edit/<int:id>', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def role_edit(role_id):
    # Set html page heading
    heading=f'Edit {TITLE_ROLE}'

    # Create model instance with query data
    obj = db.session.get(Role, role_id)

    if obj == None:
        # Report result.        
        flash(f'Error - The {TITLE_ROLE} ID: {role_id} was not found!')

        return redirect(url_for('admin.user_index'))

    # Create form instance and load it with object data
    form = RoleForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_ROLE.capitalize()} ID: {obj.role_id} - {obj.role_name} was successfully edited!')

        return redirect(url_for('admin.role_index'))

    return render_template('role/role_form.html', header=HEADER, heading=heading, form=form)


# Role delete
@admin.route('/user/role/delete/<int:id>', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def delete(role_id):
    # Create model instance with query data
    obj = db.session.get(Role, role_id)

    if obj == None:
        # Report result.        
        flash(f'Error - The {TITLE_ROLE} ID: {role_id} was not found!')
    
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_ROLE.capitalize()} ID: {obj.role_id} - {obj.role_name} was successfully delete!')

    return redirect(url_for('admin.role_index'))

