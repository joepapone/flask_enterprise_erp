from flask import Blueprint, flash, redirect, render_template, url_for, request, current_app, jsonify
from flask_login import login_required
from flask_principal import RoleNeed, Permission, PermissionDenied
from sqlalchemy.orm import lazyload
from sqlalchemy import func, extract
from datetime import datetime, date

from .models import Department, Job, Job_Terms, Job_Status, Employee_Info, Title, Gender, Marital, Email, Phone, Address,\
                    Employee, Job_History, Leave_Type, Leave_Balance, Leave_Taken, Salary, Allowance, Attendance_Log, Payroll, Holiday
from .forms import DepartmentForm, JobForm, Job_TermsForm, Job_StatusForm, EmployeeForm, TitleForm, GenderForm, MaritalForm, Employee_InfoForm,\
                   EmailForm, PhoneForm, AddressForm, Job_History_StartForm, Job_History_EndForm, Leave_TypeForm, Leave_BalanceForm, Leave_TakenForm,\
                   SalaryForm, AllowanceForm, Attendance_LogForm, Year_MonthForm, PayrollForm, HolidayForm
from .hr import YearMonth, EarningsTaxes, cal_hours_worked, cal_attendance, total_amount, set_calendar_days, net_income
from ..home.charts import angular_gauge, bullet_gauge, double_bullet_gauge, data_cards, line_chart, area_chart, bar_chart, stack_bar_chart, pie_chart,\
                          table_chart
from ..config import HEADER
from .. import db


# Set titles
TITLE_CONFIG='configuration'
TITLE_DEPARTMENT='department'
TITLE_DEPARTMENT_HISTORY = 'department history'
TITLE_JOB='job'
TITLE_JOB_TERMS='job terms'
TITLE_JOB_STATUS='job status'
TITLE_EMPLOYEE='employee'
TITLE_TITLE='title'
TITLE_GENDER='gender'
TITLE_MARITAL='maritual status'
TITLE_EMPLOYEE_INFO='employee information'
TITLE_EMAIL='email'
TITLE_PHONE='phone'
TITLE_ADDRESS='address'
TITLE_JOB_HISTORY = 'job history'
TITLE_LEAVE_TYPE='leave type'
TITLE_LEAVE_BALANCE='leave balance'
TITLE_LEAVE_TAKEN='leave taken'
TITLE_ATTENDANCE_LOG='attendance log'

TITLE_SALARY='salary'
TITLE_ALLOWANCE='allowance'
TITLE_PAYROLL='payroll'
TITLE_HOLIDAY='holiday'



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

    # Current data
    today = date.today()
    
    # Set html page menus
    menus=[{'link': '/hr/config', 'text': ' ❱ Configurations'},
           {'link': '/hr/employee/list', 'text': ' ❱ Employees'},
           {'link': f'/hr/payroll/{today.year}/{today.month}', 'text': ' ❱ Payroll'},
           {'link': f'/hr/holidays/{today.year}/{today.month}', 'text': ' ❱ Holidays'},
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
        flash(f'{TITLE_JOB_STATUS.capitalize()} ID: {obj.status_id} - {obj.title} was successfully added!')
        
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
        flash(f'{TITLE_JOB_STATUS.capitalize()} ID: {obj.status_id} - {obj.title} was successfully edited!')

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
        flash(f'Error - {TITLE_JOB_STATUS.capitalize()} {obj.title} cannot be deleted because it has a dependency ({len(child_obj)}) !')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_JOB_STATUS.capitalize()} ID: {obj.status_id} - {obj.title} successfully deleted!')
        
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
        flash(f'{TITLE_TITLE.capitalize()} ID: {obj.title_id} - {obj.title} was successfully added!')
        
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
        flash(f'{TITLE_TITLE.capitalize()} ID: {obj.title_id} - {obj.title} was successfully edited!')

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
        flash(f'Error - {TITLE_TITLE.capitalize()} ID: {obj.title_id} - {obj.title} cannot be deleted because it has a dependency ({len(child_obj)}) !')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_TITLE.capitalize()} ID: {obj.title_id} - {obj.title} successfully deleted!')
        
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

    # Perform a join query to retrieve data from multiple tables 
    stmt = db.select(Employee_Info).join(Employee_Info.employee).order_by(Employee.employee_id)
    list = db.session.execute(stmt).scalars().all()

    return render_template('hr/employee_list.html', header=HEADER, menus=menus, heading=heading, list=list)
    
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
        flash(f'{TITLE_EMPLOYEE.capitalize()} ID: {obj.employee_id}  - E-{str(obj.employee_id).zfill(7)} was successfully added!')
        
        return redirect(url_for('hr.employee_list'))
    
    return render_template('hr/employee_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Employee edit
@hr.route('/hr/employee/edit/<int:employee_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def employee_edit(employee_id):
    # Set html page menus
    menus=[{'link': '/hr/employee/list', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_EMPLOYEE}'

    # Create model instance with query data
    obj = db.session.get(Employee, employee_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_EMPLOYEE.capitalize()} ID: {employee_id} was not found!')
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    # Create form instance and load it with object data
    form = EmployeeForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_EMPLOYEE.capitalize()} ID: {obj.employee_id} - E-{str(obj.employee_id).zfill(7)} was successfully edited!')

        return redirect(url_for('hr.employee_list'))

    return render_template('hr/employee_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


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
        flash(f'{TITLE_EMPLOYEE.capitalize()} ID: {obj.employee_id} - E-{str(obj.employee_id).zfill(7)} successfully deleted!')
        
    return redirect(url_for('hr.employee_list'))


# Employee payroll history
@hr.route('/hr/employee/<int:employee_id>/payroll_history/<int:year>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def payroll_history(employee_id, year):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'{TITLE_PAYROLL.capitalize()} history'

    # Create object instance
    obj = YearMonth(year, 1)

    # Create form instance and load it with object data
    form = Year_MonthForm(obj=obj)

    # Perform a join query to retrieve data from multiple tables 
    list = db.session.execute(db
                              .select(Payroll)
                              .join(Payroll.employee)
                              .where(Employee_Info.employee_id == employee_id)
                              .filter(extract('year', Payroll.start_date) == year)
                              .order_by(Payroll.start_date)
                              ).scalars().all()
    
    if request.method == 'POST':
        year = form.year.data

        return redirect(url_for(f'hr.payroll_history', employee_id=employee_id, year=year))

    return render_template('hr/payroll_history.html', header=HEADER, menus=menus, heading=heading, employee_id=employee_id, 
                           list=list, form=form, year=year, month=1)


# ------------------------------------------------
#    Employee information
# ------------------------------------------------

# Employee sheet
@hr.route('/hr/employee/<int:employee_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def employee_sheet(employee_id):
    # Current data
    today = date.today()

    menus=[{'link': '/hr/employee/list', 'text': ' ❰ Back'},
           {'link': f'/hr/employee/{employee_id}/payroll_history/{today.year}', 'text': ' ❱ Payroll history'},
           {'link': f'/hr/employee/{employee_id}/allowances/{today.year}', 'text': ' ❱ Allowances'},
           {'link': f'/hr/employee/{employee_id}/attendance_log/{today.year}/{today.month}', 'text': ' ❱ Attendance log'},
           {'link': f'/hr/employee/{employee_id}/leave_history', 'text': ' ❱ Leave history'}]

    # Set html page heading
    heading=f'{TITLE_EMPLOYEE.capitalize()} sheet'

    # Create model instance with query data
    employee_info_obj = db.session.execute(db
                                           .select(Employee_Info)
                                           .where(Employee_Info.employee_id == employee_id)
                                           ).scalars().all()
    
    email_obj = db.session.execute(db
                                   .select(Email)
                                   .where(Email.employee_id == employee_id)
                                   ).scalars().all()
    
    phone_obj = db.session.execute(db
                                   .select(Phone)
                                   .where(Phone.employee_id == employee_id)
                                   ).scalars().all()
    
    address_obj = db.session.execute(db
                                     .select(Address)
                                     .where(Address.employee_id == employee_id)
                                     ).scalars().all()
    
    job_history_obj = db.session.execute(db
                                         .select(Job_History)
                                         .where(Job_History.employee_id == employee_id)
                                         ).scalars().all()
    
    leave_balance_obj = db.session.execute(db
                                           .select(Leave_Balance)
                                           .where(Leave_Balance.employee_id == employee_id, Leave_Balance.expiry_date >= date.today())
                                           ).scalars().all()
    
    leave_taken_obj = db.session.execute(db
                                         .select(Leave_Taken)
                                         .where(Leave_Taken.employee_id == employee_id)
                                         ).scalars().all()

    salary_obj = db.session.execute(db
                                    .select(Salary)
                                    .where(Salary.employee_id == employee_id)
                                    ).scalars().all()
    
    allowance_obj = db.session.execute(db
                                     .select(Allowance)
                                     .where(Allowance.employee_id == employee_id)
                                     ).scalars().all()
    
    attendance_log_obj = db.session.execute(db
                                      .select(Attendance_Log)
                                      .where(Attendance_Log.employee_id==employee_id)
                                      .filter(extract('year', Attendance_Log.start_time) == date.today().year, extract('month', Attendance_Log.start_time) == date.today().month)
                                      ).scalars().all()
    
    total_obj = total_amount(salary_obj, allowance_obj, attendance_log_obj)


    return render_template('hr/employee_sheet.html', header=HEADER, menus=menus, heading=heading, employee_id=employee_id, 
                           employee_info=employee_info_obj, email_list=email_obj, phone_list=phone_obj, address_list=address_obj, 
                           job_history_list=job_history_obj, leave_balance_list=leave_balance_obj, leave_taken_list=leave_taken_obj,
                           salary_list=salary_obj, allowance_list=allowance_obj, attendance_log_list=attendance_log_obj, year=today.year, month=today.month,
                           total=total_obj)


# Employee information add
@hr.route('/hr/employee/<int:employee_id>/employee_information/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def employee_info_add(employee_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{db.session.execute(db.select(Employee_Info).where(Employee_Info.employee_id == employee_id)).scalars().all()}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_EMPLOYEE_INFO}'

    # Create model instance with query data
    obj_query = db.session.execute(db.select(Employee_Info).where(Employee_Info.employee_id == employee_id)).scalars().all()

    # Exit if instance already exists
    if len(obj_query) != 0:
        # Report result.        
        flash(f'Error - {TITLE_EMPLOYEE.capitalize()} ID: {employee_id} already contains {TITLE_EMPLOYEE_INFO} ID: {obj_query[0].info_id}!')
        return redirect(url_for('hr.employee_sheet', employee_id=employee_id))

    # Create model instance
    obj = Employee_Info()

    # Create form instance
    form = Employee_InfoForm()

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Define associated parent object
        obj.employee_id=employee_id

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_EMPLOYEE_INFO.capitalize()} ID: {obj.info_id} - {obj.given_name} {obj.surname} was successfully added!')
        
        return redirect(url_for('hr.employee_sheet', employee_id=employee_id))
    
    return render_template('hr/employee_info_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Employee information edit
@hr.route('/hr/employee/<int:employee_id>/employee_information/edit/<int:info_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def employee_info_edit(employee_id, info_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_EMPLOYEE_INFO}'

    # Create model instance with query data
    obj = db.session.get(Employee_Info, info_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_EMPLOYEE_INFO.capitalize()} ID: {info_id} was not found!')
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    # Create form instance and load it with object data
    form = Employee_InfoForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_EMPLOYEE_INFO.capitalize()} ID: {obj.info_id} - {obj.given_name} {obj.surname} was successfully edited!')

        return redirect(url_for('hr.employee_sheet', employee_id=employee_id))

    return render_template('hr/employee_info_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Employee information delete
@hr.route('/hr/employee/<int:employee_id>/employee_information/delete/<int:info_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def employee_info_delete(employee_id, info_id):
    # Create model instance with query data
    obj = db.session.get(Employee_Info, info_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_EMPLOYEE_INFO.capitalize()} ID: {info_id} was not found!')
    
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_EMPLOYEE_INFO.capitalize()} ID: {obj.info_id} - {obj.given_name} {obj.surname} successfully deleted!')
        
    return redirect(url_for('hr.employee_sheet', employee_id=employee_id))


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


# Leave history
@hr.route('/hr/employee/<int:employee_id>/leave_history', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def leave_history(employee_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'{TITLE_LEAVE_BALANCE.capitalize()} history'

    # Create model instance with query data
    leave_balance_obj = db.session.execute(db.select(Leave_Balance).where(Leave_Balance.employee_id == employee_id,Leave_Balance.expiry_date <= date.today())).scalars().all()
    leave_taken_obj = db.session.execute(db.select(Leave_Taken).where(Leave_Taken.employee_id == employee_id)).scalars().all()

    return render_template('hr/leave_history.html', header=HEADER, menus=menus, heading=heading, leave_balance_list=leave_balance_obj, 
                           leave_taken_list=leave_taken_obj, employee_id=employee_id)


# Attendance log
@hr.route('/hr/employee/<int:employee_id>/attendance_log/<int:year>/<int:month>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def attendance_log(employee_id, year, month):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'{TITLE_ATTENDANCE_LOG.capitalize()}s'

    # Create object instance
    obj = YearMonth(year, month)

    # Create form instance and load it with object data
    form = Year_MonthForm(obj=obj)

    # Perform a join query to retrieve data from multiple tables 
    list = db.session.execute(db
                              .select(Attendance_Log)
                              .join(Attendance_Log.employee)
                              .where(Attendance_Log.employee_id==employee_id)
                              .filter(extract('year', Attendance_Log.start_time) == year, extract('month', Attendance_Log.start_time) == month)
                              .order_by(Attendance_Log.start_time)
                              ).scalars().all()
    
    # Cal calculate attendance
    attendance = cal_attendance(list, 20, 3)
    hours_worked = cal_hours_worked(list)

    if request.method == 'POST':
        year = form.year.data
        month = form.month.data

        return redirect(url_for(f'hr.attendance_log', employee_id=employee_id, year=year, month=month))

    return render_template('hr/attendance_log_list.html', header=HEADER, menus=menus, heading=heading, list=list, 
                           attendance=attendance, hours_worked= hours_worked, form=form, employee_id=employee_id)


# Attendance log add
@hr.route('/hr/employee/<int:employee_id>/attendance_log/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def attendance_log_add(employee_id):
    # Current data
    today = date.today()
    
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}/attendance_log/{today.year}/{today.month}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_ATTENDANCE_LOG}'

    # Create model instance
    obj = Attendance_Log()

    # Create form instance
    form = Attendance_LogForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Define associated parent object
        obj.employee_id=employee_id

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_ATTENDANCE_LOG.capitalize()} ID: {obj.log_id} was successfully added!')
        
        return redirect(url_for(f'hr.attendance_log', employee_id=employee_id, year=today.year, month=today.month))
    
    return render_template('hr/attendance_log_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Attendance log edit
@hr.route('/hr/employee/<int:employee_id>/attendance_log/edit/<int:log_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def attendance_log_edit(employee_id, log_id):
    # Current data
    today = date.today()

    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}/attendance_log/{today.year}/{today.month}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_ATTENDANCE_LOG}'

    # Create model instance with query data
    obj = db.session.get(Attendance_Log, log_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_ATTENDANCE_LOG.capitalize()} ID: {log_id} was not found!')
        return redirect(url_for(f'hr.attendance_log', employee_id=employee_id))

    # Create form instance and load it with object data
    form = Attendance_LogForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_ATTENDANCE_LOG.capitalize()} ID: {obj.log_id} was successfully edited!')

        return redirect(url_for(f'hr.attendance_log', employee_id=employee_id, year=today.year, month=today.month))

    return render_template('hr/attendance_log_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Attendance log delete
@hr.route('/hr/employee/<int:employee_id>/attendance_log/delete/<int:log_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def attendance_log_delete(employee_id, log_id):
    # Current data
    today = date.today()
    
    # Create model instance with query data
    obj = db.session.get(Attendance_Log, log_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_ATTENDANCE_LOG.capitalize()} ID: {log_id} was not found!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_ATTENDANCE_LOG.capitalize()} ID: {obj.log_id} successfully deleted!')
        
    return redirect(url_for(f'hr.attendance_log', employee_id=employee_id, year=today.year, month=today.month))


# Salary add
@hr.route('/hr/employee/<int:employee_id>/salary/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def salary_add(employee_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_SALARY}'

    # Create model instance
    obj = Salary()

    # Create model instance with query data
    obj_query = db.session.execute(db.select(Salary).where(Salary.employee_id == employee_id)).scalars().all()

    # Exit if instance already exists
    if len(obj_query) != 0:
        # Report result.        
        flash(f'Error - {TITLE_EMPLOYEE.capitalize()} ID: {employee_id} already contains {TITLE_SALARY} ID: {obj_query[0].salary_id}!')
        return redirect(url_for('hr.employee_sheet', employee_id=employee_id))

    # Create form instance
    form = SalaryForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Define associated parent object
        obj.employee_id=employee_id

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_SALARY.capitalize()} ID: {obj.salary_id} was successfully added!')
        
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))
    
    return render_template('hr/salary_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Salary edit
@hr.route('/hr/employee/<int:employee_id>/salary/edit/<int:salary_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def salary_edit(employee_id, salary_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_SALARY}'

    # Create model instance with query data
    obj = db.session.get(Salary, salary_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_SALARY.capitalize()} ID: {salary_id} was not found!')
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    # Create form instance and load it with object data
    form = SalaryForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_SALARY.capitalize()} ID: {obj.salary_id} was successfully edited!')

        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    return render_template('hr/salary_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Salary delete
@hr.route('/hr/employee/<int:employee_id>/salary/delete/<int:salary_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def salary_delete(employee_id, salary_id):
    # Create model instance with query data
    obj = db.session.get(Salary, salary_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_SALARY.capitalize()} ID: {salary_id} was not found!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_SALARY.capitalize()} ID: {obj.salary_id} successfully deleted!')
        
    return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))


# Allowance list
@hr.route('/hr/employee/<int:employee_id>/allowances/<int:year>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def allowances(employee_id, year):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'{TITLE_ALLOWANCE.capitalize()}s'

    # Create object instance
    obj = YearMonth(year, 1)

    # Create form instance and load it with object data
    form = Year_MonthForm(obj=obj)

    # Perform a join query to retrieve data from multiple tables 
    list = db.session.execute(db
                              .select(Allowance)
                              .join(Allowance.employee)
                              .where(Allowance.employee_id==employee_id)
                              .filter(extract('year', Allowance.start_date) == year)
                              .order_by(Allowance.start_date)
                              ).scalars().all()
    
    if request.method == 'POST':
        year = form.year.data

        return redirect(url_for(f'hr.allowances', employee_id=employee_id, year=year))

    return render_template('hr/allowance_list.html', header=HEADER, menus=menus, heading=heading, list=list, form=form, year=year, employee_id=employee_id)

# Allowance add
@hr.route('/hr/employee/<int:employee_id>/allowance/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def allowance_add(employee_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_ALLOWANCE}'

    # Create model instance
    obj = Allowance()

    # Create form instance
    form = AllowanceForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Define associated parent object
        obj.employee_id=employee_id

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_ALLOWANCE.capitalize()} ID: {obj.allowance_id} was successfully added!')
        
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))
    
    return render_template('hr/allowance_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Allowance edit
@hr.route('/hr/employee/<int:employee_id>/allowance/edit/<int:allowance_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def allowance_edit(employee_id, allowance_id):
    # Set html page menus
    menus=[{'link': f'/hr/employee/{employee_id}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_ALLOWANCE}'

    # Create model instance with query data
    obj = db.session.get(Allowance, allowance_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_ALLOWANCE.capitalize()} ID: {allowance_id} was not found!')
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    # Create form instance and load it with object data
    form = AllowanceForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_ALLOWANCE.capitalize()} ID: {obj.allowance_id} was successfully edited!')

        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    return render_template('hr/allowance_form.html', header=HEADER, menus=menus, heading=heading, form=form, employee_id=employee_id)


# Allowance delete
@hr.route('/hr/employee/<int:employee_id>/allowance/delete/<int:allowance_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def allowance_delete(employee_id, allowance_id):
    # Create model instance with query data
    obj = db.session.get(Allowance, allowance_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_ALLOWANCE.capitalize()} ID: {allowance_id} was not found!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_ALLOWANCE.capitalize()} ID: {obj.allowance_id} successfully deleted!')
        
    return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))


# ------------------------------------------------
#    Payroll
# ------------------------------------------------

# Payroll list
@hr.route('/hr/payroll/<int:year>/<int:month>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def payroll(year, month):
    # Set html page menus
    menus=[{'link': f'/hr/dashboard', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'{TITLE_PAYROLL.capitalize()}s'

    # Create object instance
    obj = YearMonth(year, month)

    # Create form instance and load it with object data
    form = Year_MonthForm(obj=obj)

    # Perform a join query to retrieve data from multiple tables 
    list = db.session.execute(db
                              .select(Payroll)
                              .join(Payroll.employee)
                              .filter(extract('year', Payroll.start_date) == year, extract('month', Payroll.start_date) == month)
                              .order_by(Payroll.start_date)
                              ).scalars().all()
    
    if request.method == 'POST':
        year = form.year.data
        month = form.month.data

        return redirect(url_for(f'hr.payroll', year=year, month=month))

    return render_template('hr/payroll_list.html', header=HEADER, menus=menus, heading=heading, list=list, form=form, year=year, month=month)


# Payroll add
@hr.route('/hr/payroll/<int:year>/<int:month>/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def payroll_add(year, month):
    # Set html page menus
    menus=[{'link': f'/hr/payroll/{year}/{month}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_PAYROLL}'

    # Create model instance
    obj = Payroll()

    # Create form instance
    form = PayrollForm()
    
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Set specific object attribute
        obj.net_income = net_income(obj.gross_income, obj.adjustment, obj.income_tax)
        
        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_PAYROLL.capitalize()} ID: {obj.payroll_id} was successfully added!')
        
        return redirect(url_for(f'hr.payroll', year=year, month=month))
    
    return render_template('hr/payroll_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Payroll edit
@hr.route('/hr/payroll/<int:year>/<int:month>/edit/<int:payroll_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def payroll_edit(payroll_id, year, month):
    # Set html page menus
    menus=[{'link': f'/hr/payroll/{year}/{month}', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_PAYROLL}'

    # Create model instance with query data
    obj = db.session.get(Payroll, payroll_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_PAYROLL.capitalize()} ID: {payroll_id} was not found!')
        return redirect(url_for(f'hr.payroll'))

    # Create form instance and load it with object data
    form = PayrollForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Set specific object attribute
        obj.net_income = net_income(obj.gross_income, obj.adjustment, obj.income_tax)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_PAYROLL.capitalize()} ID: {obj.payroll_id} was successfully edited!')

        return redirect(url_for(f'hr.payroll', year=year, month=month))

    return render_template('hr/payroll_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Payroll delete
@hr.route('/hr/payroll/<int:year>/<int:month>/delete/<int:payroll_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def payroll_delete(payroll_id, year, month):
    # Create model instance with query data
    obj = db.session.get(Payroll, payroll_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_PAYROLL.capitalize()} ID: {payroll_id} was not found!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_PAYROLL.capitalize()} ID: {obj.payroll_id} successfully deleted!')
        
    return redirect(url_for(f'hr.payroll', year=year, month=month))


# ------------------------------------------------
#    Holiday
# ------------------------------------------------

# Holidays
@hr.route('/hr/holidays/<int:year>/<int:month>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def holidays(year, month):
    # Set html page menus
    menus=[{'link': f'/hr/dashboard', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'{TITLE_HOLIDAY.capitalize()}s'

    # Perform a join query to retrieve data from multiple tables 
    list = db.session.execute(db
                              .select(Holiday)
                              .filter(extract('year', Holiday.holiday_date) == year, extract('month', Holiday.holiday_date) == month)
                              .order_by(Holiday.holiday_date)
                              ).scalars().all()
    
    # Get holiday dates
    holidays = [i.holiday_date for i in list]

    # Set calendar header and days according to year and month range
    if 1 <= year <=9999 and 1 <= month <=12:
        calendar_header = YearMonth(year, month)
        calandar = set_calendar_days(datetime(year, month, 1), holidays)
    
    else:
        calendar_header = YearMonth(1980, 1)
        calandar = set_calendar_days(datetime(1980, 1, 1), holidays)

    return render_template('hr/holiday_list.html', header=HEADER, menus=menus, heading=heading, list=list, 
                           calendar_header=calendar_header, calendar=calandar, year=year, month=month)


# Holiday add
@hr.route('/hr/holiday/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def holiday_add():
    # Set html page menus
    menus=[{'link': f'/hr/holidays', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Add {TITLE_HOLIDAY}'

    # Create model instance
    obj = Holiday()

    # Create form instance
    form = HolidayForm()
    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_HOLIDAY.capitalize()} ID: {obj.holiday_id} was successfully added!')
        
        return redirect(url_for(f'hr.holidays', year=datetime.today().year, month=datetime.today().month))
    
    return render_template('hr/holiday_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Holiday edit
@hr.route('/hr/holiday/edit/<int:holiday_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def holiday_edit(holiday_id):
    # Set html page menus
    menus=[{'link': f'/hr/holidays', 'text': ' ❰ Back'}]

    # Set html page heading
    heading=f'Edit {TITLE_HOLIDAY}'

    # Create model instance with query data
    obj = db.session.get(Holiday, holiday_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_HOLIDAY.capitalize()} ID: {holiday_id} was not found!')
        return redirect(url_for(f'hr.holidays', year=datetime.today().year, month=datetime.today().month))

    # Create form instance and load it with object data
    form = HolidayForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_HOLIDAY.capitalize()} ID: {obj.holiday_id} was successfully edited!')

        return redirect(url_for(f'hr.holidays', year=datetime.today().year, month=datetime.today().month))

    return render_template('hr/holiday_form.html', header=HEADER, menus=menus, heading=heading, form=form)


# Holiday delete
@hr.route('/hr/holiday/delete/<int:holiday_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def holiday_delete(holiday_id):
    # Create model instance with query data
    obj = db.session.get(Holiday, holiday_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_HOLIDAY.capitalize()} ID: {holiday_id} was not found!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_HOLIDAY.capitalize()} ID: {obj.holiday_id} successfully deleted!')
        
    return redirect(url_for(f'hr.holidays', year=datetime.today().year, month=datetime.today().month))

