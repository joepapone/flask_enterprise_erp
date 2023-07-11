from flask import Blueprint, flash, redirect, render_template, url_for, request, current_app, jsonify
from flask_login import login_required
from flask_principal import RoleNeed, Permission, PermissionDenied

from .. import db
from ..app import HEADER
from ..charts import angular_gauge, bullet_gauge, double_bullet_gauge, data_cards, line_chart, area_chart, bar_chart, stack_bar_chart, pie_chart, table_chart
from .models import Terms, Status, Employee, Employee_History, Email, Phone, Address, Gender, Marital
from ..admin.models import Department, Job
from .forms import TermsForm, StatusForm, EmployeeForm, EmailForm, PhoneForm, AddressForm, GenderForm, MaritalForm

hr = Blueprint('hr', __name__,
               template_folder='templates',
               static_folder='static',
               static_url_path='/static')

# Create a permission with a single Need (RoleNeed)
hr_permission = Permission(RoleNeed('Admin'))

# Set titles
TITLE_TERMS='empoyment terms'
TITLE_STATUS='empoyment status'
TITLE_EMPLOYEE='empoyee'
TITLE_EMAIL='email'
TITLE_PHONE='phone'
TITLE_ADDRESS='address'
TITLE_GENDER='gender'
TITLE_MARITAL='maritual status'

# Permission denied error handler
@hr.errorhandler(PermissionDenied)
def handle_error(e):
    flash('Error - Human resource manager privileges required')
    return redirect(url_for('root.home'))


# Dashboard
@hr.route('/hr/dashboard')
@login_required
def dashboard():
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
    return render_template('hr/dashboard.html', header=HEADER, heading=heading, 
                           chart1=plot1, chart2=plot2, chart3=plot3, chart4=plot4, chart5=plot5, chart6=plot6, chart7=plot7, chart8=plot8,
                           chart9=plot9, chart10=plot10, chart11=plot11, chart12=plot12, chart13=plot13, chart14=plot14)


# Employment terms list
@hr.route('/hr/employee/terms/list')
@login_required
def terms_list():
    # Set html page heading
    heading=TITLE_TERMS.capitalize()

    # Create model instance with query data
    list = db.session.execute(db.select(Terms)).scalars().all()

    return render_template('hr/terms_list.html', header=HEADER, heading=heading, list=list)


# Employment terms add
@hr.route('/hr/employee/terms/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def terms_add():
    # Set html page heading
    heading=f'Add {TITLE_TERMS}'

    # Create form instance
    form = TermsForm()
    if form.validate_on_submit():
        # Create model instance
        obj = Terms()

        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_TERMS.capitalize()} {obj.terms} was successfully added!')
        
        return redirect(url_for('hr.terms_list'))
    
    return render_template('hr/terms_form.html', header=HEADER, heading=heading, form=form)


# Employment terms edit
@hr.route('/hr/employee/terms/edit/<int:terms_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def terms_edit(terms_id):
    # Set html page heading
    heading=f'Edit {TITLE_TERMS}'

    # Create model instance with query data
    obj = db.session.get(Terms, terms_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_TERMS.capitalize()} nº{terms_id} was not found!')
        return redirect(url_for('hr.terms_list'))

    # Create form instance and load it with object data
    form = TermsForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_TERMS.capitalize()} {obj.terms} was successfully edited!')

        return redirect(url_for('hr.terms_list'))

    return render_template('hr/terms_form.html', header=HEADER, heading=heading, form=form)


# Employment terms delete
@hr.route('/hr/employee/terms/delete/<int:terms_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def terms_delete(terms_id):
    # Create model instance with query data
    obj = db.session.get(Terms, terms_id)
    # Check for child dependencies
    child_obj = None #db.session.execute(db.select(Employee).filter_by(terms_id=id)).first()

    if obj == None:
        # Report result
        flash(f'Error - The terms nº{terms_id} was not found!')
    
    elif child_obj != None:
        # Report result.
        flash(f'Error - {TITLE_TERMS.capitalize()} {obj.terms} cannot be deleted because it has dependencies!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_TERMS.capitalize()} {obj.terms} successfully deleted!')
        
    return redirect(url_for('hr.terms_list'))


# Employment status list
@hr.route('/hr/employee/status/list')
@login_required
def status_list():
    # Set html page heading
    heading=TITLE_STATUS.capitalize()

    # Create model instance with query data
    list = db.session.execute(db.select(Status)).scalars().all()

    return render_template('hr/status_list.html', header=HEADER, heading=heading, list=list)


# Employment status add
@hr.route('/hr/employee/status/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def status_add():
    # Set html page heading
    heading=f'Add {TITLE_STATUS}'

    # Create form instance
    form = StatusForm()
    if form.validate_on_submit():
        # Create model instance
        obj = Status()

        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_STATUS.capitalize()} {obj.status_title} was successfully added!')
        
        return redirect(url_for('hr.status_list'))
    
    return render_template('hr/status_form.html', header=HEADER, heading=heading, form=form)


# Employment status edit
@hr.route('/hr/employee/status/edit/<int:status_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def status_edit(status_id):
    # Set html page heading
    heading=f'Edit {TITLE_STATUS}'

    # Create model instance with query data
    obj = db.session.get(Status, status_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_STATUS.capitalize()} nº{status_id} was not found!')
        return redirect(url_for('hr.status_list'))

    # Create form instance and load it with object data
    form = StatusForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_STATUS.capitalize()} {obj.status_title} was successfully edited!')

        return redirect(url_for('hr.status_list'))

    return render_template('hr/status_form.html', header=HEADER, heading=heading, form=form)


# Employment status delete
@hr.route('/hr/employee/status/delete/<int:status_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def status_delete(status_id):
    # Create model instance with query data
    obj = db.session.get(Status, status_id)
    # Check for child dependencies
    child_obj = None #db.session.execute(db.select(Employee).filter_by(status_id=id)).first()

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_STATUS.capitalize()} nº{status_id} was not found!')
    
    elif child_obj != None:
        # Report result.        
        flash(f'Error - {TITLE_STATUS.capitalize()} {obj.status_title} cannot be deleted because it has dependencies!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_STATUS.capitalize()} {obj.status_title} successfully deleted!')
        
    return redirect(url_for('hr.status_list'))


# Employee list
@hr.route('/hr/employee/list')
@login_required
def employee_list():
    # Set html page heading
    heading=f'{TITLE_EMPLOYEE.capitalize()}s'

    # Create model instance with query data
    list = db.session.execute(db.select(Employee)).scalars().all()

    return render_template('hr/employee_list.html', header=HEADER, heading=heading, list=list)


# Employee sheet
@hr.route('/hr/employee/sheet/<int:employee_id>', methods=('GET', 'POST'))
@login_required
def employee_sheet(employee_id):
    # Set html page heading
    heading=f'{TITLE_EMPLOYEE.capitalize()} sheet'

    # Create model instance with query data
    employee_obj = db.session.execute(db.select(Employee).where(Employee.employee_id == employee_id)).scalars().all()
    email_obj = db.session.execute(db.select(Email).where(Email.employee_id == employee_id)).scalars().all()
    phone_obj = db.session.execute(db.select(Phone).where(Phone.employee_id == employee_id)).scalars().all()
    address_obj = db.session.execute(db.select(Address).where(Address.employee_id == employee_id)).scalars().all()

    print(employee_obj)

    return render_template('hr/employee_sheet.html', header=HEADER, heading=heading, data_list=employee_obj, email_list=email_obj, phone_list=phone_obj, 
                           address_list=address_obj, employee_id=employee_id)


# Employee add
@hr.route('/hr/employee/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def employee_add():
    # Set html page heading
    heading=f'Add {TITLE_EMPLOYEE}'

    # Create form instance
    form = EmployeeForm()

    # Outside to prevent validation erros during POST
    if request.method == 'POST':
        form.job_id.choices = [(row.job_id, row.job_title) for row in db.session.execute(db.select(Job)).scalars().all()]

    if form.validate_on_submit():
        # Create model instance
        obj = Employee()

        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_EMPLOYEE.capitalize()} {obj.employee_name} {obj.employee_surname} was successfully added!')

        # Record history event
        event = Employee_History(obj.employee_id, f'{TITLE_EMPLOYEE.capitalize()} {obj.employee_name} {obj.employee_surname} was created')
        db.session.add(event)
        db.session.commit()
        
        return redirect(url_for('hr.employee_list'))
    
    return render_template('hr/employee_form.html', header=HEADER, heading=heading, form=form)


# Employee edit
@hr.route('/hr/employee/edit/<int:employee_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def employee_edit(employee_id):
    # Set html page heading
    heading=f'Edit {TITLE_EMPLOYEE}'

    # Create model instance with query data
    obj = db.session.get(Employee, employee_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_EMPLOYEE.capitalize()} nº{employee_id} was not found!')
        return redirect(url_for('hr.employee_list'))

    # Create form instance and load it with object data
    form = EmployeeForm(obj=obj)

    # Outside to prevent validation erros during POST
    if request.method == 'POST':
        form.job_id.choices = [(row.job_id, row.job_title) for row in db.session.execute(db.select(Job)).scalars().all()]

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_EMPLOYEE.capitalize()} {obj.employee_name} {obj.employee_surname} was successfully edited!')

        # Record history event
        event = Employee_History(obj.employee_id, f'{TITLE_EMPLOYEE.capitalize()} {obj.employee_name} was modified')
        db.session.add(event)
        db.session.commit()

        return redirect(url_for('hr.employee_sheet', employee_id=employee_id))

    return render_template('hr/employee_form.html', header=HEADER, heading=heading, form=form)


# Employee delete
@hr.route('/hr/employee/delete/<int:employee_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def employee_delete(employee_id):
    # Create model instance with query data
    obj = db.session.get(Employee, employee_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_EMPLOYEE.capitalize()} nº{employee_id} was not found!')
    
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_EMPLOYEE.capitalize()} {obj.employee_name} {obj.employee_surname} successfully deleted!')

        # Record history event
        event = Employee_History(obj.employee_id, f'{TITLE_EMPLOYEE.capitalize()} {obj.employee_name} {obj.employee_surname} was deleted')
        db.session.add(event)
        db.session.commit()
        
    return redirect(url_for('hr.employee_list'))


# Employee job
@hr.route('/hr/employee/job/<int:job_id>', methods=('GET', 'POST'))
@login_required
def employee_job(job_id):
    # Create a dictionary with query data
    list = [{'id': row.job_id, 'label': row.job_title} for row in db.session.execute(db.select(Job).where(Job.department_id == job_id)).scalars().all()]

    return jsonify({'list': list})


# Employee history
@hr.route('/hr/employee/history')
@login_required
def employee_history():
    # Set html page heading
    heading='Employee history'

    # Create model instance with query data
    list = db.session.execute(db.select(Employee_History)).scalars().all()

    return render_template('hr/employee_history.html', header=HEADER, heading=heading, list=list)


# Employment email add
@hr.route('/hr/employee/<int:employee_id>/email/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def email_add(employee_id):
    # Set html page heading
    heading=f'Add {TITLE_EMAIL}'

    # Create form instance
    form = EmailForm()
    if form.validate_on_submit():
        # Create model instance
        obj = Email()

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
    
    return render_template('hr/email_form.html', header=HEADER, heading=heading, form=form, employee_id=employee_id)


# Employment email edit
@hr.route('/hr/employee/<int:employee_id>/email/edit/<int:email_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def email_edit(employee_id, email_id):
    # Set html page heading
    heading=f'Edit {TITLE_EMAIL}'

    # Create model instance with query data
    obj = db.session.get(Email, email_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_EMAIL.capitalize()} nº{email_id} was not found!')
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

    return render_template('hr/email_form.html', header=HEADER, heading=heading, form=form, employee_id=employee_id)


# Employment email delete
@hr.route('/hr/employee/<int:employee_id>/email/delete/<int:email_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def email_delete(employee_id, email_id):
    # Create model instance with query data
    obj = db.session.get(Email, email_id)
    # Check for child dependencies
    child_obj = None #db.session.execute(db.select(Employee).filter_by(email_id=id)).first()

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_EMAIL.capitalize()} nº{email_id} was not found!')
    
    elif child_obj != None:
        # Report result.        
        flash(f'Error - {TITLE_EMAIL.capitalize()} {obj.email} cannot be deleted because it has dependencies!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_EMAIL.capitalize()} {obj.email} successfully deleted!')
        
    return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))


# Employment phone add
@hr.route('/hr/employee/<int:employee_id>/phone/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def phone_add(employee_id):
    # Set html page heading
    heading=f'Add {TITLE_PHONE}'

    # Create form instance
    form = PhoneForm()
    if form.validate_on_submit():
        # Create model instance
        obj = Phone()

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
    
    return render_template('hr/phone_form.html', header=HEADER, heading=heading, form=form, employee_id=employee_id)


# Employment phone edit
@hr.route('/hr/employee/<int:employee_id>/phone/edit/<int:phone_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def phone_edit(employee_id, phone_id):
    # Set html page heading
    heading=f'Edit {TITLE_PHONE}'

    # Create model instance with query data
    obj = db.session.get(Phone, phone_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_PHONE.capitalize()} nº{phone_id} was not found!')
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

    return render_template('hr/phone_form.html', header=HEADER, heading=heading, form=form, employee_id=employee_id)


# Employment phone delete
@hr.route('/hr/employee/<int:employee_id>/phone/delete/<int:phone_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def phone_delete(employee_id, phone_id):
    # Create model instance with query data
    obj = db.session.get(Phone, phone_id)
    # Check for child dependencies
    child_obj = None #db.session.execute(db.select(Employee).filter_by(phone_id=id)).first()

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_PHONE.capitalize()} nº{phone_id} was not found!')
    
    elif child_obj != None:
        # Report result.        
        flash(f'Error - {TITLE_PHONE.capitalize()} {obj.dial_code} {obj.phone_number} cannot be deleted because it has dependencies!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_PHONE.capitalize()} {obj.dial_code} {obj.phone_number} successfully deleted!')
        
    return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))


# Employment address add
@hr.route('/hr/employee/<int:employee_id>/address/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def address_add(employee_id):
    # Set html page heading
    heading=f'Add {TITLE_ADDRESS}'

    # Create form instance
    form = AddressForm()
    if form.validate_on_submit():
        # Create model instance
        obj = Address()

        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Define associated parent object
        obj.employee_id=employee_id

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_ADDRESS.capitalize()} (ID: {obj.address_id}) - {obj.postal_code} {obj.city} was successfully added!')
        
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))
    
    return render_template('hr/address_form.html', header=HEADER, heading=heading, form=form, employee_id=employee_id)


# Employment address edit
@hr.route('/hr/employee/<int:employee_id>/address/edit/<int:address_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def address_edit(employee_id, address_id):
    # Set html page heading
    heading=f'Edit {TITLE_ADDRESS}'

    # Create model instance with query data
    obj = db.session.get(Address, address_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_ADDRESS.capitalize()} nº{address_id} was not found!')
        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    # Create form instance and load it with object data
    form = AddressForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{TITLE_ADDRESS.capitalize()} (ID: {obj.address_id}) - {obj.postal_code} {obj.city} was successfully edited!')

        return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))

    return render_template('hr/address_form.html', header=HEADER, heading=heading, form=form, employee_id=employee_id)


# Employment address delete
@hr.route('/hr/employee/<int:employee_id>/address/delete/<int:address_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def address_delete(employee_id, address_id):
    # Create model instance with query data
    obj = db.session.get(Address, address_id)
    # Check for child dependencies
    child_obj = None #db.session.execute(db.select(Employee).filter_by(address_id=id)).first()

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_ADDRESS.capitalize()} ({address_id}) was not found!')
    
    elif child_obj != None:
        # Report result.        
        flash(f'Error - {TITLE_ADDRESS.capitalize()} ({address_id}) cannot be deleted because it has dependencies!')

    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_ADDRESS.capitalize()} (ID: {obj.address_id}) - {obj.postal_code} {obj.city} successfully deleted!')
        
    return redirect(url_for(f'hr.employee_sheet', employee_id=employee_id))


# Employment gender list
@hr.route('/hr/employee/gender/list')
@login_required
def gender_list():
    # Set html page heading
    heading=TITLE_GENDER.capitalize()

    # Create model instance with query data
    list = db.session.execute(db.select(Gender)).scalars().all()

    return render_template('hr/gender_list.html', header=HEADER, heading=heading, list=list)


# Employment gender add
@hr.route('/hr/employee/gender/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def gender_add():
    # Set html page heading
    heading=f'Add {TITLE_GENDER}'

    # Create form instance
    form = GenderForm()
    if form.validate_on_submit():
        # Create model instance
        obj = Gender()

        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_GENDER.capitalize()} (ID: {obj.gender_id}) - {obj.gender} was successfully added!')
        
        return redirect(url_for('hr.gender_list'))
    
    return render_template('hr/gender_form.html', header=HEADER, heading=heading, form=form)


# Employment gender edit
@hr.route('/hr/employee/gender/edit/<int:gender_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def gender_edit(gender_id):
    # Set html page heading
    heading=f'Edit {TITLE_GENDER}'

    # Create model instance with query data
    obj = db.session.get(Gender, gender_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_GENDER.capitalize()} (ID: {obj.gender_id}) was not found!')
        return redirect(url_for('hr.gender_list'))

    # Create form instance and load it with object data
    form = GenderForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_GENDER.capitalize()} (ID: {obj.gender_id}) - {obj.gender} was successfully edited!')

        return redirect(url_for('hr.gender_list'))

    return render_template('hr/gender_form.html', header=HEADER, heading=heading, form=form)


# Employment gender delete
@hr.route('/hr/employee/gender/delete/<int:gender_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def gender_delete(gender_id):
    # Create model instance with query data
    obj = db.session.get(Gender, gender_id)
    # Check for child dependencies
    child_obj = None #db.session.execute(db.select(Employee).filter_by(gender_id=id)).first()

    if obj == None:
        # Report result
        flash(f'Error - The gender (ID: {obj.gender_id}) was not found!')
    
    elif child_obj != None:
        # Report result.
        flash(f'Error - {TITLE_GENDER.capitalize()} (ID: {obj.gender_id}) - {obj.gender} cannot be deleted because it has dependencies!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_GENDER.capitalize()} (ID: {obj.gender_id}) - {obj.gender} successfully deleted!')
        
    return redirect(url_for('hr.gender_list'))


# Employment marital list
@hr.route('/hr/employee/marital/list')
@login_required
def marital_list():
    # Set html page heading
    heading=TITLE_MARITAL.capitalize()

    # Create model instance with query data
    list = db.session.execute(db.select(Marital)).scalars().all()

    return render_template('hr/marital_list.html', header=HEADER, heading=heading, list=list)


# Employment marital add
@hr.route('/hr/employee/marital/add', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def marital_add():
    # Set html page heading
    heading=f'Add {TITLE_MARITAL}'

    # Create form instance
    form = MaritalForm()
    if form.validate_on_submit():
        # Create model instance
        obj = Marital()

        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_MARITAL.capitalize()} (ID: {obj.marital_id}) - {obj.marital_status} was successfully added!')
        
        return redirect(url_for('hr.marital_list'))
    
    return render_template('hr/marital_form.html', header=HEADER, heading=heading, form=form)


# Employment marital edit
@hr.route('/hr/employee/marital/edit/<int:marital_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def marital_edit(marital_id):
    # Set html page heading
    heading=f'Edit {TITLE_MARITAL}'

    # Create model instance with query data
    obj = db.session.get(Marital, marital_id)

    if obj == None:
        # Report result.        
        flash(f'Error - {TITLE_MARITAL.capitalize()} (ID: {obj.marital_id}) was not found!')
        return redirect(url_for('hr.marital_list'))

    # Create form instance and load it with object data
    form = MaritalForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_MARITAL.capitalize()} (ID: {obj.marital_id}) - {obj.marital_status} was successfully edited!')

        return redirect(url_for('hr.marital_list'))

    return render_template('hr/marital_form.html', header=HEADER, heading=heading, form=form)


# Employment mariatial delete
@hr.route('/hr/employee/marital/delete/<int:marital_id>', methods=('GET', 'POST'))
@login_required
@hr_permission.require()
def marital_delete(marital_id):
    # Create model instance with query data
    obj = db.session.get(Marital, marital_id)
    # Check for child dependencies
    child_obj = None #db.session.execute(db.select(Employee).filter_by(marital_id=id)).first()

    if obj == None:
        # Report result
        flash(f'Error - The marital nº{marital_id} was not found!')
    
    elif child_obj != None:
        # Report result.
        flash(f'Error - {TITLE_MARITAL.capitalize()} (ID: {obj.marital_id}) - {obj.marital_status} cannot be deleted because it has dependencies!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{TITLE_MARITAL.capitalize()} (ID: {obj.marital_id}) - {obj.marital_status} successfully deleted!')
        
    return redirect(url_for('hr.marital_list'))




'''

// Department
let select_department = document.getElementById('department_id');
let select_job = document.getElementById('job_id');

// Form select department
select_department.onchange = function() {
    // Get form select value
    department_id = select_department.value;
    
    // Get route response
    fetch('/hr/employee/department/' + department_id).then(function(response) {
        // Convert response into json data
        response.json().then(function(data)  {
            console.table(data);

            // Create select option HTML
            let optionHTML = '';
            for (let job of data.jobs) {
                optionHTML += '<option value=' + job.id + '>' + job.title + '</option>';
            }
            // Update form select
            select_job.innerHTML = optionHTML;
        });
    });

}

                        <div class="form-row {% if form.mobile_phone.errors %}error{% endif %}">
                            <div class="label-col">
                                <label class="field-label" for="description">{{ form.mobile_phone.label }}</label>
                            </div>
                            <div class="input-col">
                                {{ form.mobile_phone }}
                                {%- for error in form.mobile_phone.errors %}
                                {%- if form.mobile_phone.errors %}<div class="error-message">{{ error }}</div>{%- endif %}
                                {%- endfor %}
                            </div>
                        </div>
                        <div class="form-row {% if form.home_phone.errors %}error{% endif %}">
                            <div class="label-col">
                                <label class="field-label" for="description">{{ form.home_phone.label }}</label>
                            </div>
                            <div class="input-col">
                                {{ form.home_phone }}
                                {%- for error in form.home_phone.errors %}
                                {%- if form.home_phone.errors %}<div class="error-message">{{ error }}</div>{%- endif %}
                                {%- endfor %}
                            </div>
                        </div>


    print(f' ID: {obj.employee_id }\n Name: {obj.employee_name}\n Department: {obj.department.department_name} \
          \n Job: {obj.job.job_title}\n')
'''