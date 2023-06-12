from flask import Blueprint, flash, redirect, render_template, url_for, request, current_app
from flask_login import login_required
from flask_principal import RoleNeed, Permission, PermissionDenied

from .. import db
from ..app import HEADER
from ..charts import angular_gauge, bullet_gauge, double_bullet_gauge, data_cards, line_chart, area_chart, bar_chart, stack_bar_chart, pie_chart, table_chart
from .models import Department, Department_History, Job, Job_History
from .forms import DepartmentForm, JobForm

admin = Blueprint('admin', __name__,
                  template_folder='templates',
                  static_folder='static',
                  static_url_path='/static')


# Create a permission with a single Need (RoleNeed)
admin_permission = Permission(RoleNeed('Admin'))


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
    return render_template('admin/dashboard.html', header=HEADER, heading=heading, 
                           chart1=plot1, chart2=plot2, chart3=plot3, chart4=plot4, chart5=plot5, chart6=plot6, chart7=plot7, chart8=plot8,
                           chart9=plot9, chart10=plot10, chart11=plot11, chart12=plot12, chart13=plot13, chart14=plot14)


# Department list
@admin.route('/admin/department/list')
@login_required
def department_list():
    # Set html page heading
    heading='Departments'

    # Create model instance with query data
    list = db.session.execute(db.select(Department)).scalars().all()

    return render_template('admin/department_list.html', header=HEADER, heading=heading, list=list)


# Department add
@admin.route('/admin/department/add', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def department_add():
    # Set html page heading
    heading='Add department'

    # Create form instance
    form = DepartmentForm()
    if form.validate_on_submit():
        # Create model instance
        obj = Department()

        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{obj.department_name} department successfully added!')

        # Record event
        event = Department_History(obj.department_id, f'The department "{obj.department_name}" was created')
        db.session.add(event)
        db.session.commit()
        
        return redirect(url_for('admin.department_list'))
    
    return render_template('admin/department_form.html', header=HEADER, heading=heading, form=form)


# Department edit
@admin.route('/admin/department/edit/<int:id>', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def department_edit(id):
    # Set html page heading
    heading='Edit department'

    # Create model instance with query data
    obj = db.session.get(Department, id)

    if obj == None:
        # Report result.        
        flash(f'Error - The department nº{id} was not found!')
        return redirect(url_for('admin.department_list'))

    # Create form instance and load it with object data
    form = DepartmentForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'{obj.department_name} department successfully edited!')

        # Record event
        event = Department_History(obj.department_id, f'The department "{obj.department_name}" was modified')
        db.session.add(event)
        db.session.commit()

        return redirect(url_for('admin.department_list'))

    return render_template('admin/department_form.html', header=HEADER, heading=heading, form=form)


# Department delete
@admin.route('/admin/department/delete/<int:id>', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def department_delete(id):
    # Create model instance with query data
    obj = db.session.get(Department, id)
    # Check for child dependencies
    child_obj = db.session.execute(db.select(Job).filter_by(department_id=id)).first()

    if obj == None:
        # Report result.        
        flash(f'Error - The department nº{id} was not found!')
    
    elif child_obj != None:
        # Report result.        
        flash(f'Error - {obj.department_name} department cannot be deleted because it has dependencies!')
        
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'{obj.department_name} department successfully deleted!')

        # Record event
        event = Department_History(obj.department_id, f'The department "{obj.department_name}" was deleted')
        db.session.add(event)
        db.session.commit()
        
    return redirect(url_for('admin.department_list'))


# Department history
@admin.route('/admin/department/history')
@login_required
def department_history():
    # Set html page heading
    heading='Department history'

    # Create model instance with query data
    list = db.session.execute(db.select(Department_History)).scalars().all()

    return render_template('admin/department_history.html', header=HEADER, heading=heading, list=list)


# Job list
@admin.route('/admin/job/list')
@login_required
def job_list():
    # Set html page heading
    heading='Jobs'

    # Create model instance with query data
    list = db.session.execute(db.select(Job)).scalars().all()

    return render_template('admin/job_list.html', header=HEADER, heading=heading, list=list)


# Job add
@admin.route('/admin/job/add', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def job_add():
    # Set html page heading
    heading='Add job'

    # Create form instance
    form = JobForm()
    if form.validate_on_submit():
        # Create model instance
        obj = Job()

        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Marked for insertion
        db.session.add(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'The job title {obj.job_title} was successfully added!')

        # Record history event
        event = Job_History(obj.job_id, f'The job title "{obj.job_title}" was created')
        db.session.add(event)
        db.session.commit()
        
        return redirect(url_for('admin.job_list'))
    
    return render_template('admin/job_form.html', header=HEADER, heading=heading, form=form)


# Job edit
@admin.route('/admin/job/edit/<int:id>', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def job_edit(id):
    # Set html page heading
    heading='Edit job'

    # Create model instance with query data
    obj = db.session.get(Job, id)

    if obj == None:
        # Report result.        
        flash(f'Error - The job nº{id} was not found!')
        return redirect(url_for('admin.job_list'))

    # Create form instance and load it with object data
    form = JobForm(obj=obj)

    if form.validate_on_submit():
        # Populate object attributes with form data.
        form.populate_obj(obj)

        # Commit changes to database
        db.session.commit() 
        flash(f'The job title {obj.job_title} was successfully edited!')

        # Record history event
        event = Job_History(obj.job_id, f'The job title {obj.job_title} was modified')
        db.session.add(event)
        db.session.commit()

        return redirect(url_for('admin.job_list'))

    return render_template('admin/job_form.html', header=HEADER, heading=heading, form=form)


# Job delete
@admin.route('/admin/job/delete/<int:id>', methods=('GET', 'POST'))
@login_required
@admin_permission.require()
def job_delete(id):
    # Create model instance with query data
    obj = db.session.get(Job, id)

    if obj == None:
        # Report result.        
        flash(f'Error - The job nº{id} was not found!')
    
    else:
        # Marked for deletion
        db.session.delete(obj)

        # Commit changes to database
        db.session.commit()
        flash(f'The job title {obj.job_title} successfully deleted!')

        # Record history event
        event = Job_History(obj.job_id, f'The job "{obj.job_title}" was deleted')
        db.session.add(event)
        db.session.commit()
        
    return redirect(url_for('admin.job_list'))


# Job history
@admin.route('/admin/job/history')
@login_required
def job_history():
    # Set html page heading
    heading='Job history'

    # Create model instance with query data
    list = db.session.execute(db.select(Job_History)).scalars().all()

    return render_template('admin/job_history.html', header=HEADER, heading=heading, list=list)
