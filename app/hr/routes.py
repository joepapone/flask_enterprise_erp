from flask import Blueprint, flash, redirect, render_template, url_for, request, current_app, jsonify
from flask_login import login_required
from flask_principal import RoleNeed, Permission, PermissionDenied
from sqlalchemy.orm import lazyload

from .models import Department, Job, Job_Terms, Job_Status, Employee, Job_History, Email, Phone, Address, Title, Gender, Marital,\
                    Leave_Type, Leave_Balance, Leave_Taken
from .forms import DepartmentForm, JobForm, Job_TermsForm, Job_StatusForm, EmployeeForm, Job_History_StartForm, Job_History_EndForm,EmailForm,\
                    PhoneForm, AddressForm, TitleForm, GenderForm, MaritalForm, Leave_TypeForm, Leave_BalanceForm, Leave_TakenForm
from ..home.charts import angular_gauge, bullet_gauge, double_bullet_gauge, data_cards, line_chart, area_chart, bar_chart, stack_bar_chart, pie_chart, table_chart
from ..config import HEADER
from .. import db


# Set titles
TITLE_CONFIG='configuration'
TITLE_DEPARTMENT='department'
TITLE_DEPARTMENT_HISTORY = 'department history'
TITLE_JOB='job'
TITLE_JOB_HISTORY = 'job history'
TITLE_JOB_TERMS='job terms'
TITLE_JOB_STATUS='job status'
TITLE_EMPLOYEE='empoyee'
TITLE_EMAIL='email'
TITLE_PHONE='phone'
TITLE_ADDRESS='address'
TITLE_TITLE='title'
TITLE_GENDER='gender'
TITLE_MARITAL='maritual status'
TITLE_LEAVE_TYPE='leave type'
TITLE_LEAVE_BALANCE='leave balance'
TITLE_LEAVE_TAKEN='leave taken'


# Human resources blueprint
hr = Blueprint('hr', __name__,
               template_folder='templates',
               static_folder='static',
               static_url_path='/static')


# Create a permission with a single Need (RoleNeed)
hr_permission = Permission(RoleNeed('Admin'), RoleNeed('Human Resource Manager'))


# Permission denied error handler
@hr.errorhandler(PermissionDenied)
def handle_error(e):
    flash('Error - Human resource manager privileges required')
    return redirect(url_for('root.home'))


# Dashboard
@hr.route('/hr/dashboard')
@login_required
@hr_permission.require()
def dashboard():
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❱ Configurations'},
           {'link': '/hr/employee/list', 'text': ' ❱ Employees'},
           {'link': '/home', 'text': ' ❰ Back'}]

    # Set html page heading
    heading='Human Resources (HR)'

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
    plot8 = pie_chart('Employees per Sector', None, ['hristrative','Sales','Production','Maintence'], [20, 256, 320, 24], 0.6, 'Sector')
    plot9 = bar_chart('Salary', '$54.000', None, ['Mar', 'Apr', 'May', 'Jun', 'Jul'], [50, 51, 52, 53, 54], 'v')
    plot10 = area_chart('Education per Head', '$180', None, None, None, None, ['Mar', 'Apr', 'May', 'Jun', 'Jul'], [210, 209, 150, 235, 180])
    plot11 = area_chart('Education per FTE', '$210', None, None, None, None, ['Mar', 'Apr', 'May', 'Jun', 'Jul'], [285, 260, 210, 290, 210])
    plot12 = area_chart('Education spending', '$122', None, None, None, None, ['Mar', 'Apr', 'May', 'Jun', 'Jul'], [156, 139, 113, 150, 122])
    plot13 = table_chart('Other indicatores', 'test1', table1_headers, table1_values )
    plot14 = table_chart('Other indicatores', 'test2', table2_headers, table2_values)
    return render_template('hr/dashboard.html', header=HEADER, menus=menus, heading=heading, 
                           chart1=plot1, chart2=plot2, chart3=plot3, chart4=plot4, chart5=plot5, chart6=plot6, chart7=plot7, chart8=plot8,
                           chart9=plot9, chart10=plot10, chart11=plot11, chart12=plot12, chart13=plot13, chart14=plot14)


# ------------------------------------------------
#    Configurations
# ------------------------------------------------

# Config
@hr.route('/hr/config', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def config():
    # Set html page menus
    menus=[{'link': '/hr/dashboard', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'{TITLE_CONFIG.capitalize()}s'

    # Create model instance with query data
    department_obj = db.session.execute(db.select(Department).order_by(Department.department_name.asc())).scalars().all()
    job_obj = db.session.execute(db.select(Job).order_by(Job.job_title.asc())).scalars().all()
    status_obj = db.session.execute(db.select(Job_Status)).scalars().all()
    terms_obj = db.session.execute(db.select(Job_Terms)).scalars().all()
    title_obj = db.session.execute(db.select(Title)).scalars().all()
    gender_obj = db.session.execute(db.select(Gender).order_by(Gender.gender.asc())).scalars().all()
    marital_obj = db.session.execute(db.select(Marital).order_by(Marital.marital_status.asc())).scalars().all()
    leave_type_obj = db.session.execute(db.select(Leave_Type).order_by(Leave_Type.type_title.asc())).scalars().all()


    return render_template('hr/config.html', header=HEADER, menus=menus, heading=heading, department_list=department_obj, job_list=job_obj,
                           status_list=status_obj, terms_list=terms_obj, title_list=title_obj, gender_list=gender_obj, marital_list=marital_obj,
                           leave_type_list=leave_type_obj)


# Department add
@hr.route('/hr/department/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def department_add():
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_DEPARTMENT}'

    # Create model instance
    obj = Department()

    # Create form instance
    form = DepartmentForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_DEPARTMENT.capitalize()} ID: {obj.department_id} - {obj.department_name} was successfully added!')
        
        return redirect(url_for('hr.config'))
    
    return render_template('hr/department_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Department edit
@hr.route('/hr/department/edit/<int:department_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def department_edit(department_id):
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_DEPARTMENT}'

    # Create model instance with query data
    obj = db.session.get(Department, department_id)

    if obj == None:
        # Report result.        
        flash(f'Error - The department ID: {department_id} was not found!')
        return redirect(url_for('hr.config'))

    # Create form instance and load it with object data
    form = DepartmentForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_DEPARTMENT.capitalize()} ID: {obj.department_id} - {obj.department_name} was successfully edited!')

        return redirect(url_for('hr.config'))

    return render_template('hr/department_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Department delete
@hr.route('/hr/department/delete/<int:department_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def department_delete(department_id):
    # Create model instance with query data
    obj = db.session.get(Department, department_id)

    # Check for child dependencies
    child_obj = db.session.execute(
        db.select(Job_History.job_history_id)
        .join(Department, (Department.department_id == Job_History.department_id) & (Department.department_id == department_id))
        .join(Job, (Job.job_id == Job_History.job_id))
        ).all()

    if obj == None:
        # Report result
        flash(f'Error - The {TITLE_DEPARTMENT} ID: {department_id} was not found!')
    
    elif len(child_obj) > 0:
        # Report result
        flash(f'Error - {TITLE_DEPARTMENT.capitalize()} ID: {obj.department_id} - {obj.department_name} cannot be deleted because it has a dependency ({len(child_obj)}) !')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_DEPARTMENT.capitalize()} ID: {obj.department_id} - {obj.department_name} was successfully deleted!')

    return redirect(url_for('hr.config'))


# Job add
@hr.route('/hr/job/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def job_add():
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_JOB}'

    # Create model instance
    obj = Job()

    # Create form instance
    form = JobForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_JOB.capitalize()} ID: {obj.job_id} - {obj.job_title} was successfully added!')
        
        return redirect(url_for('hr.config'))
    
    return render_template('hr/job_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Job edit
@hr.route('/hr/job/edit/<int:job_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def job_edit(job_id):
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_JOB}'

    # Create model instance with query data
    obj = db.session.get(Job, job_id)

    if obj == None:
        # Report result.        
        flash(f'Error - The job ID: {job_id} was not found!')
        return redirect(url_for('hr.config'))

    # Create form instance and load it with object data
    form = JobForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_JOB.capitalize()} ID: {obj.job_id} - {obj.job_title} was successfully edited!')

        return redirect(url_for('hr.config'))

    return render_template('hr/job_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Job delete
@hr.route('/hr/job/delete/<int:job_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def job_delete(job_id):
    # Create model instance with query data
    obj = db.session.get(Job, job_id)

    # Check for child dependencies
    child_obj = db.session.execute(
        db.select(Job.job_id).join(Job_History, (Job.job_id == Job_History.job_id) & (Job.job_id == job_id))
        ).all()

    if obj == None:
        # Report result.        
        flash(f'Error - The job ID: {job_id} was not found!')
    
    elif len(child_obj) > 0:
        # Report result
        flash(f'Error - {TITLE_JOB.capitalize()} ID: {obj.job_id} - {obj.job_title} cannot be deleted because it has a dependency ({len(child_obj)}) !')

    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_JOB.capitalize()} ID: {obj.job_id} - {obj.job_title} was successfully deleted!')
        
    return redirect(url_for('hr.config'))


# Job terms add
@hr.route('/hr/job/terms/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def terms_add():
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_JOB_TERMS}'

    # Create model instance
    obj = Job_Terms()

    # Create form instance
    form = Job_TermsForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_JOB_TERMS.capitalize()} ID: {obj.terms_id} - {obj.terms} was successfully added!')
        
        return redirect(url_for('hr.config'))
    
    return render_template('hr/terms_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Job terms edit
@hr.route('/hr/job/terms/edit/<int:terms_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def terms_edit(terms_id):
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_JOB_TERMS}'

    # Create model instance with query data
    obj = db.session.get(Job_Terms, terms_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_JOB_TERMS.capitalize()} ID: {terms_id} was not found!')
        return redirect(url_for('hr.config'))

    # Create form instance and load it with object data
    form = Job_TermsForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_JOB_TERMS.capitalize()} ID: {obj.terms_id} - {obj.terms} was successfully edited!')

        return redirect(url_for('hr.config'))

    return render_template('hr/terms_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Job terms delete
@hr.route('/hr/job/terms/delete/<int:terms_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def terms_delete(terms_id):
    # Create model instance with query data
    obj = db.session.get(Job_Terms, terms_id)
    # Check for child dependencies
    child_obj = db.session.execute(
        db.select(Job_Terms.terms_id).join(Job_History, (Job_Terms.terms_id == Job_History.terms_id) & (Job_Terms.terms_id == terms_id))
        ).all()

    if obj == None:
        # Report result
        flash(f'Error - The terms ID: {terms_id} was not found!')
    
    elif len(child_obj) > 0:
        # Report result.
        flash(f'Error - {TITLE_JOB_TERMS.capitalize()} ID: {obj.terms_id} - {obj.terms} cannot be deleted because it has a dependency ({len(child_obj)}) !')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_JOB_TERMS.capitalize()} {obj.terms} successfully deleted!')
        
    return redirect(url_for('hr.config'))


# Job status add
@hr.route('/hr/job/status/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def status_add():
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_JOB_STATUS}'

    # Create model instance
    obj = Job_Status()

    # Create form instance
    form = Job_StatusForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_JOB_STATUS.capitalize()} ID: {obj.status_id} - {obj.status_title} was successfully added!')
        
        return redirect(url_for('hr.config'))
    
    return render_template('hr/status_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Job status edit
@hr.route('/hr/job/status/edit/<int:status_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def status_edit(status_id):
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_JOB_STATUS}'

    # Create model instance with query data
    obj = db.session.get(Job_Status, status_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_JOB_STATUS.capitalize()} ID: {status_id} was not found!')
        return redirect(url_for('hr.config'))

    # Create form instance and load it with object data
    form = Job_StatusForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_JOB_STATUS.capitalize()} ID: {obj.status_id} - {obj.status_title} was successfully edited!')

        return redirect(url_for('hr.config'))

    return render_template('hr/status_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Job status delete
@hr.route('/hr/job/status/delete/<int:status_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def status_delete(status_id):
    # Create model instance with query data
    obj = db.session.get(Job_Status, status_id)
    # Check for child dependencies
    child_obj = db.session.execute(
    db.select(Job_Status.status_id).join(Job_History, (Job_Status.status_id == Job_History.status_id) & (Job_Status.status_id == status_id))
    ).all()

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_JOB_STATUS.capitalize()} ID: {status_id} was not found!')
    
    elif len(child_obj) > 0:
        # Report result.        
        flash(f'Error - {TITLE_JOB_STATUS.capitalize()} {obj.status_title} cannot be deleted because it has a dependency ({len(child_obj)}) !')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_JOB_STATUS.capitalize()} ID: {obj.status_id} - {obj.status_title} successfully deleted!')
        
    return redirect(url_for('hr.config'))


# Title add
@hr.route('/hr/title/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def title_add():
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_TITLE}'

    # Create model instance
    obj = Title()

    # Create form instance
    form = TitleForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_TITLE.capitalize()} ID: {obj.title_id} - {obj.title_name} was successfully added!')
        
        return redirect(url_for('hr.config'))
    
    return render_template('hr/title_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Title edit
@hr.route('/hr/title/edit/<int:title_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def title_edit(title_id):
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_TITLE}'

    # Create model instance with query data
    obj = db.session.get(Title, title_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_TITLE.capitalize()} ID: {obj.title_id}) was not found!')
        return redirect(url_for('hr.config'))

    # Create form instance and load it with object data
    form = TitleForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_TITLE.capitalize()} ID: {obj.title_id} - {obj.title_name} was successfully edited!')

        return redirect(url_for('hr.config'))

    return render_template('hr/title_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Title delete
@hr.route('/hr/title/delete/<int:title_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def title_delete(title_id):
    # Create model instance with query data
    obj = db.session.get(Title, title_id)

    # Check for child dependencies
    child_obj = db.session.execute(
        db.select(Title).join(Employee, (Title.title_id == Employee.title_id) & (Title.title_id == title_id))
        ).all()

    if obj == None:
        # Report result
        flash(f'Error - The gender ID: {obj.title_id}) was not found!')
    
    elif len(child_obj) > 0:
        # Report result.
        flash(f'Error - {TITLE_TITLE.capitalize()} ID: {obj.title_id} - {obj.title_name} cannot be deleted because it has a dependency ({len(child_obj)}) !')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_TITLE.capitalize()} ID: {obj.title_id} - {obj.title_name} successfully deleted!')
        
    return redirect(url_for('hr.config'))


# Gender add
@hr.route('/hr/gender/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def gender_add():
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_GENDER}'

    # Create model instance
    obj = Gender()

    # Create form instance
    form = GenderForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_GENDER.capitalize()} ID: {obj.gender_id} - {obj.gender} was successfully added!')
        
        return redirect(url_for('hr.config'))
    
    return render_template('hr/gender_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Gender edit
@hr.route('/hr/gender/edit/<int:gender_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def gender_edit(gender_id):
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_GENDER}'

    # Create model instance with query data
    obj = db.session.get(Gender, gender_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_GENDER.capitalize()} ID: {obj.gender_id}) was not found!')
        return redirect(url_for('hr.config'))

    # Create form instance and load it with object data
    form = GenderForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_GENDER.capitalize()} ID: {obj.gender_id} - {obj.gender} was successfully edited!')

        return redirect(url_for('hr.config'))

    return render_template('hr/gender_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Gender delete
@hr.route('/hr/gender/delete/<int:gender_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def gender_delete(gender_id):
    # Create model instance with query data
    obj = db.session.get(Gender, gender_id)
    # Check for child dependencies
    child_obj = db.session.execute(
        db.select(Gender.gender_id).join(Employee, (Gender.gender_id == Employee.gender_id) & (Gender.gender_id == gender_id))
        ).all()

    if obj == None:
        # Report result
        flash(f'Error - The gender ID: {obj.gender_id}) was not found!')
    
    elif len(child_obj) > 0:
        # Report result.
        flash(f'Error - {TITLE_GENDER.capitalize()} ID: {obj.gender_id} - {obj.gender} cannot be deleted because it has a dependency ({len(child_obj)}) !')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_GENDER.capitalize()} ID: {obj.gender_id} - {obj.gender} successfully deleted!')
        
    return redirect(url_for('hr.config'))


# Marital add
@hr.route('/hr/marital/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def marital_add():
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_MARITAL}'

    # Create model instance
    obj = Marital()

    # Create form instance
    form = MaritalForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_MARITAL.capitalize()} ID: {obj.marital_id} - {obj.marital_status} was successfully added!')
        
        return redirect(url_for('hr.config'))
    
    return render_template('hr/marital_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Marital edit
@hr.route('/hr/marital/edit/<int:marital_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def marital_edit(marital_id):
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_MARITAL}'

    # Create model instance with query data
    obj = db.session.get(Marital, marital_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_MARITAL.capitalize()} ID: {obj.marital_id}) was not found!')
        return redirect(url_for('hr.config'))

    # Create form instance and load it with object data
    form = MaritalForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_MARITAL.capitalize()} ID: {obj.marital_id} - {obj.marital_status} was successfully edited!')

        return redirect(url_for('hr.config'))

    return render_template('hr/marital_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Marital delete
@hr.route('/hr/marital/delete/<int:marital_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def marital_delete(marital_id):
    # Create model instance with query data
    obj = db.session.get(Marital, marital_id)
    # Check for child dependencies
    child_obj = db.session.execute(
        db.select(Marital.marital_id).join(Employee, (Marital.marital_id == Employee.marital_id) & (Marital.marital_id == marital_id))
        ).all()

    if obj == None:
        # Report result
        flash(f'Error - The marital ID: {marital_id} was not found!')
    
    elif len(child_obj) > 0:
        # Report result.
        flash(f'Error - {TITLE_MARITAL.capitalize()} ID: {obj.marital_id} - {obj.marital_status} cannot be deleted because it has a dependency ({len(child_obj)}) !')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_MARITAL.capitalize()} ID: {obj.marital_id} - {obj.marital_status} successfully deleted!')
        
    return redirect(url_for('hr.config'))


# Leave type add
@hr.route('/hr/leave_type/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def leave_type_add():
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_LEAVE_TYPE}'

    # Create model instance
    obj = Leave_Type()

    # Create form instance
    form = Leave_TypeForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_LEAVE_TYPE.capitalize()} ID: {obj.type_id} - {obj.type_title} was successfully added!')
        
        return redirect(url_for('hr.config'))
    
    return render_template('hr/leave_type_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Leave type edit
@hr.route('/hr/leave_type/edit/<int:leave_type_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def leave_type_edit(leave_type_id):
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_LEAVE_TYPE}'

    # Create model instance with query data
    obj = db.session.get(Leave_Type, leave_type_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_LEAVE_TYPE.capitalize()} ID: {obj.type_id}) was not found!')
        return redirect(url_for('hr.config'))

    # Create form instance and load it with object data
    form = Leave_TypeForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_LEAVE_TYPE.capitalize()} ID: {obj.type_id} - {obj.type_title} was successfully edited!')

        return redirect(url_for('hr.config'))

    return render_template('hr/leave_type_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Leave type delete
@hr.route('/hr/leave_type/delete/<int:leave_type_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def leave_type_delete(leave_type_id):
    # Create model instance with query data
    obj = db.session.get(Leave_Type, leave_type_id)
    # Check for child dependencies
    child_obj = "" #db.session.execute(
        #db.select(Leave_Type.type_id).join(Employee, (Leave_Type.type_id == Employee.type_id) & (Leave_Type.type_id == leave_type_id))
        #).all()

    if obj == None:
        # Report result
        flash(f'Error - The leave_type ID: {leave_type_id} was not found!')
    
    elif len(child_obj) > 0:
        # Report result.
        flash(f'Error - {TITLE_LEAVE_TYPE.capitalize()} ID: {obj.type_id} - {obj.type_title} cannot be deleted because it has a dependency ({len(child_obj)}) !')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_LEAVE_TYPE.capitalize()} ID: {obj.type_id} - {obj.type_title} successfully deleted!')
        
    return redirect(url_for('hr.config'))


# ------------------------------------------------
#    Employee
# ------------------------------------------------

# Employee list
@hr.route('/hr/employee/list')
@login_required
@hr_permission.require()
def employee_list():
    # Set html page menus
    menus=[{'link': '/hr/dashboard', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'{TITLE_EMPLOYEE.capitalize()}s'

    # Create model instance with query data
    list = db.session.execute(db.select(Employee)).scalars().all()

    return render_template('hr/employee_list.html', header=HEADER, menus=menus, heading=heading, list=list)


# Employee sheet
@hr.route('/hr/employee/<int:employee_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def employee_sheet(employee_id):
    # Set html page menus
    menus=[{'link': '/hr/employee/list', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'{TITLE_EMPLOYEE.capitalize()} sheet'

    # Create model instance with query data
    employee_obj = db.session.execute(db.select(Employee).where(Employee.employee_id == employee_id)).scalars().all()
    job_history_obj = db.session.execute(db.select(Job_History).where(Job_History.employee_id == employee_id)).scalars().all()
    email_obj = db.session.execute(db.select(Email).where(Email.employee_id == employee_id)).scalars().all()
    phone_obj = db.session.execute(db.select(Phone).where(Phone.employee_id == employee_id)).scalars().all()
    address_obj = db.session.execute(db.select(Address).where(Address.employee_id == employee_id)).scalars().all()
    leave_balance_obj = db.session.execute(db.select(Leave_Balance).where(Leave_Balance.employee_id == employee_id)).scalars().all()
    leave_taken_obj = db.session.execute(db.select(Leave_Taken).where(Leave_Taken.employee_id == employee_id)).scalars().all()

    return render_template('hr/employee_sheet.html', header=HEADER, menus=menus, heading=heading, data_list=employee_obj, job_history_list=job_history_obj,
                           email_list=email_obj, phone_list=phone_obj, address_list=address_obj, leave_balance_list=leave_balance_obj, 
                           leave_taken_list=leave_taken_obj, employee_id=employee_id)


# Employee add
@hr.route('/hr/employee/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def employee_add():
    # Set html page menus
    menus=[{'link': '/hr/employee/list', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_EMPLOYEE}'

    # Create model instance
    obj = Employee()

    # Create form instance
    form = EmployeeForm()

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_EMPLOYEE.capitalize()} ID: {obj.employee_id} - {obj.employee_name} {obj.employee_surname} was successfully added!')
        
        return redirect(url_for('hr.employee_list'))
    
    return render_template('hr/employee_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Employee edit
@hr.route('/hr/employee/edit/<int:employee_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def employee_edit(employee_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_EMPLOYEE}'

    # Create model instance with query data
    obj = db.session.get(Employee, employee_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_EMPLOYEE.capitalize()} ID: {employee_id} was not found!')
        return redirect(url_for('hr.employee_list'))

    # Create form instance and load it with object data
    form = EmployeeForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_EMPLOYEE.capitalize()} ID: {obj.employee_id} - {obj.employee_name} {obj.employee_surname} was successfully edited!')

        return redirect(url_for('hr.employee_sheet', employee_id=employee_id))

    return render_template('hr/employee_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Employee delete
@hr.route('/hr/employee/delete/<int:employee_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def employee_delete(employee_id):
    # Create model instance with query data
    obj = db.session.get(Employee, employee_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_EMPLOYEE.capitalize()} ID: {employee_id} was not found!')
    
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_EMPLOYEE.capitalize()} ID: {obj.employee_id} - {obj.employee_name} {obj.employee_surname} successfully deleted!')
        
    return redirect(url_for('hr.employee_list'))


# Load job list
@hr.route('/hr/employee/job/<int:job_id>', methods=('GET', 'POST'))
@login_required
def employee_job(job_id):
    # Create a dictionary with query data
    list = [{'id': row.job_id, 'label': row.job_title} for row in db.session.execute(db.select(Job).where(Job.department_id == job_id)).scalars().all()]

    return jsonify({'list': list})


# Job history add
@hr.route('/hr/employee/<int:employee_id>/job_history/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def job_history_add(employee_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_JOB_HISTORY}'

    # Create model instance
    obj = Job_History()
    
    # Create form instance
    form = Job_History_StartForm()

    # Outside to prevent validation erros during POST
    if request.method == 'POST':
        form.job_id.choices = [(row.job_id, row.job_title) for row in db.session.execute(db.select(Job)).scalars().all()]

    if form.validate_on_submit():
        # Define associated parent object
        obj.employee_id=employee_id

        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_JOB_HISTORY.capitalize()} ID: {obj.job_history_id} - {obj.job.job_title} was successfully added!')
        
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))
    
    return render_template('hr/job_history_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Job history edit
@hr.route('/hr/employee/<int:employee_id>/job_history/edit/<int:job_history_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def job_history_edit(employee_id, job_history_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_JOB_HISTORY}'

    # Create model instance with query data
    obj = db.session.get(Job_History, job_history_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_JOB_HISTORY.capitalize()} ID: {job_history_id} was not found!')
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    # Create form instance and load it with object data
    form = Job_History_StartForm(obj=obj)

    # Outside to prevent validation erros during POST
    if request.method == 'POST':
        form.job_id.choices = [(row.job_id, row.job_title) for row in db.session.execute(db.select(Job)).scalars().all()]
    else:
        form.job_id.choices = [(row.job_id, row.job_title) for row in db.session.execute(db.select(Job).where(Job.department_id == obj.department_id)).scalars().all()]
    
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_JOB_HISTORY.capitalize()} ID: {obj.job_history_id} - {obj.job.job_title} was successfully edited!')

        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    return render_template('hr/job_history_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Job history delete
@hr.route('/hr/employee/<int:employee_id>/job_history/delete/<int:job_history_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def job_history_delete(employee_id, job_history_id):
    # Create model instance with query data
    obj = db.session.get(Job_History, job_history_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_JOB_HISTORY.capitalize()} ID: {job_history_id} was not found!')
    
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_JOB_HISTORY.capitalize()} ID: {obj.job_history_id} was successfully deleted!')
        
    return redirect(url_for('hr.employee_sheet', employee_id=employee_id))


# Job history complete
@hr.route('/hr/employee/<int:employee_id>/job_history/complete/<int:job_history_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def job_history_complete(employee_id, job_history_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Complete {TITLE_JOB_HISTORY}'

    # Create model instance with query data
    obj = db.session.get(Job_History, job_history_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_JOB_HISTORY.capitalize()} ID: {job_history_id} was not found!')
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    # Create form instance and load it with object data
    form = Job_History_EndForm(obj=obj)
    
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_JOB_HISTORY.capitalize()} ID: {obj.job_history_id} - {obj.job.job_title} was successfully edited!')

        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    return render_template('hr/job_history_complete_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Email add
@hr.route('/hr/employee/<int:employee_id>/email/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def email_add(employee_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_EMAIL}'

    # Create model instance
    obj = Email()

    # Create form instance
    form = EmailForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Define associated parent object
        obj.employee_id=employee_id

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_EMAIL.capitalize()} {obj.email} was successfully added!')

        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))
    
    return render_template('hr/email_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Email edit
@hr.route('/hr/employee/<int:employee_id>/email/edit/<int:email_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def email_edit(employee_id, email_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_EMAIL}'

    # Create model instance with query data
    obj = db.session.get(Email, email_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_EMAIL.capitalize()} ID: {email_id} was not found!')
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    # Create form instance and load it with object data
    form = EmailForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_EMAIL.capitalize()} {obj.email} was successfully edited!')

        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    return render_template('hr/email_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Email delete
@hr.route('/hr/employee/<int:employee_id>/email/delete/<int:email_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def email_delete(employee_id, email_id):
    # Create model instance with query data
    obj = db.session.get(Email, email_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_EMAIL.capitalize()} ID: {email_id} was not found!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_EMAIL.capitalize()} ID: {obj.email_id} - {obj.email} successfully deleted!')
        
    return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))


# Phone add
@hr.route('/hr/employee/<int:employee_id>/phone/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def phone_add(employee_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_PHONE}'

    # Create model instance
    obj = Phone()

    # Create form instance
    form = PhoneForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Define associated parent object
        obj.employee_id=employee_id

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_PHONE.capitalize()} {obj.dial_code} {obj.phone_number} was successfully added!')
        
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))
    
    return render_template('hr/phone_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Phone edit
@hr.route('/hr/employee/<int:employee_id>/phone/edit/<int:phone_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def phone_edit(employee_id, phone_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_PHONE}'

    # Create model instance with query data
    obj = db.session.get(Phone, phone_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_PHONE.capitalize()} ID: {phone_id} was not found!')
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    # Create form instance and load it with object data
    form = PhoneForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_PHONE.capitalize()} {obj.dial_code} {obj.phone_number} was successfully edited!')

        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    return render_template('hr/phone_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Phone delete
@hr.route('/hr/employee/<int:employee_id>/phone/delete/<int:phone_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def phone_delete(employee_id, phone_id):
    # Create model instance with query data
    obj = db.session.get(Phone, phone_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_PHONE.capitalize()} ID: {phone_id} was not found!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_PHONE.capitalize()} ID: {obj.phone_id} - {obj.dial_code} {obj.phone_number} successfully deleted!')
        
    return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))


# Address add
@hr.route('/hr/employee/<int:employee_id>/address/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def address_add(employee_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_ADDRESS}'

    # Create model instance
    obj = Address()
    
    # Create form instance
    form = AddressForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Define associated parent object
        obj.employee_id=employee_id

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_ADDRESS.capitalize()} ID: {obj.address_id} - {obj.postal_code} {obj.city} was successfully added!')
        
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))
    
    return render_template('hr/address_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Address edit
@hr.route('/hr/employee/<int:employee_id>/address/edit/<int:address_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def address_edit(employee_id, address_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_ADDRESS}'

    # Create model instance with query data
    obj = db.session.get(Address, address_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_ADDRESS.capitalize()} ID: {address_id} was not found!')
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    # Create form instance and load it with object data
    form = AddressForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_ADDRESS.capitalize()} ID: {obj.address_id} - {obj.postal_code} {obj.city} was successfully edited!')

        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    return render_template('hr/address_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Address delete
@hr.route('/hr/employee/<int:employee_id>/address/delete/<int:address_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def address_delete(employee_id, address_id):
    # Create model instance with query data
    obj = db.session.get(Address, address_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_ADDRESS.capitalize()} ({address_id}) was not found!')

    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_ADDRESS.capitalize()} ID: {obj.address_id} - {obj.postal_code} {obj.city} successfully deleted!')
        
    return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))


# Leave balance add
@hr.route('/hr/employee/<int:employee_id>/leave_balance/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def leave_balance_add(employee_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_LEAVE_BALANCE}'

    # Create model instance
    obj = Leave_Balance()
    
    # Create form instance
    form = Leave_BalanceForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Define associated parent object
        obj.employee_id=employee_id

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_LEAVE_BALANCE.capitalize()} ID: {obj.balance_id} was successfully added!')
        
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))
    
    return render_template('hr/leave_balance_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Leave balance edit
@hr.route('/hr/employee/<int:employee_id>/leave_balance/edit/<int:balance_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def leave_balance_edit(employee_id, balance_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_LEAVE_BALANCE}'

    # Create model instance with query data
    obj = db.session.get(Leave_Balance, balance_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_LEAVE_BALANCE.capitalize()} ID: {balance_id} was not found!')
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    # Create form instance and load it with object data
    form = Leave_BalanceForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_LEAVE_BALANCE.capitalize()} ID: {obj.balance_id} was successfully edited!')

        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    return render_template('hr/leave_balance_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)

# Leave balance delete
@hr.route('/hr/employee/<int:employee_id>/leave_balance/delete/<int:balance_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def leave_balance_delete(employee_id, balance_id):
    # Create model instance with query data
    obj = db.session.get(Leave_Balance, balance_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_LEAVE_BALANCE.capitalize()} ({balance_id}) was not found!')

    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_LEAVE_BALANCE.capitalize()} ID: {obj.balance_id} was successfully deleted!')
        
    return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))


# Leave taken add
@hr.route('/hr/employee/<int:employee_id>/leave_balance_id/<int:balance_id>/leave_taken/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def leave_taken_add(employee_id, balance_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_LEAVE_TAKEN}'

    # Create model instance
    obj = Leave_Taken()

    # Create model instance of parent
    parent_obj = db.session.get(Leave_Balance, balance_id)

    # Query table according to criteria
    leave_taken = db.session.execute(db.select(Leave_Taken).where(Leave_Taken.balance_id == balance_id)).scalars().all()

    # Calculate remaining leave
    remaining = parent_obj.leave_days
    for i in leave_taken:
        remaining -= i.delta()

    # Create form instance
    form = Leave_TakenForm()
    form.remaining.data = remaining
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Define associated parent object
        obj.employee_id = employee_id
        obj.balance_id = balance_id

        # Update parante table data
        parent_obj.leave_taken += obj.delta()
        parent_obj.leave_balance = parent_obj.leave_days - parent_obj.leave_taken

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_LEAVE_TAKEN.capitalize()} ID: {obj.taken_id} was successfully added!')
        
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))
    
    return render_template('hr/leave_taken_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Leave taken edit
@hr.route('/hr/employee/<int:employee_id>/leave_balance_id/<int:balance_id>/leave_taken/edit/<int:taken_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def leave_taken_edit(employee_id, balance_id, taken_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_LEAVE_TAKEN}'

    # Create model instance with query data
    obj = db.session.get(Leave_Taken, taken_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_LEAVE_TAKEN.capitalize()} ID: {taken_id} was not found!')
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    # Create model instance of parent
    parent_obj = db.session.get(Leave_Balance, balance_id)

    # Query table according to criteria
    leave_taken = db.session.execute(db.select(Leave_Taken).where(Leave_Taken.balance_id == balance_id, Leave_Taken.taken_id != taken_id)).scalars().all()

    # Calculate remaining leave
    remaining = parent_obj.leave_days
    for i in leave_taken:
        remaining -= i.delta()

    # Create form instance and load it with object data
    form = Leave_TakenForm(obj=obj)
    form.remaining.data = remaining
    if form.validate_on_submit():
        # Populate object attributes with form data
        form.populate_obj(obj)

        # Update parante table data
        parent_obj.leave_taken = parent_obj.leave_days - remaining + obj.delta()
        parent_obj.leave_balance = parent_obj.leave_days - parent_obj.leave_taken

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_LEAVE_TAKEN.capitalize()} ID: {obj.taken_id} was successfully edited!')

        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    return render_template('hr/leave_taken_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Leave taken delete
@hr.route('/hr/employee/<int:employee_id>/leave_balance_id/<int:balance_id>/taken_taken/delete/<int:taken_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def leave_taken_delete(employee_id, balance_id, taken_id):
    # Create model instance with query data
    obj = db.session.get(Leave_Taken, taken_id)

    # Create model instance of parent
    parent_obj = db.session.get(Leave_Balance, balance_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_LEAVE_TAKEN.capitalize()} ({taken_id}) was not found!')

    else:
        # Marked for deletion
        db.session.delete(obj)

        # Update parante table data
        parent_obj.leave_taken -= obj.delta()
        parent_obj.leave_balance = parent_obj.leave_days - parent_obj.leave_taken

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_LEAVE_TAKEN.capitalize()} ID: {obj.taken_id} was successfully deleted!')
        
    return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

