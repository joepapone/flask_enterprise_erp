from datetime import datetime
from ..admin.models import Country, Currency
from .. import db
from .hr import cal_attendance, work_hours, work_time

# Department data-model
class Department(db.Model):
    # Table name
    __tablename__ = 'department'
    # Main Fields
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(50), unique=True)
    
    def get_id(self):
        return (self.department_id)
    
    def __repr__(self):
        return f'Department ({self.department_id}): {self.department_name}'
    
# Job data-model
class Job(db.Model):
    # Table name
    __tablename__ = 'job'
    # Main Fields
    job_id = db.Column(db.Integer, primary_key=True) 
    job_title = db.Column(db.String(50), unique=True)
    job_description = db.Column(db.String(150))
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'), nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    department = db.relationship(Department, foreign_keys=[department_id])
      
    def get_id(self):
        return (self.job_id)
        
    def __repr__(self):
        return f'Job ({self.job_id}): {self.job_title}'

# Job terms data-model
class Job_Terms(db.Model):
    # Table name
    __tablename__ = 'job_terms'
    # Main Fields
    terms_id = db.Column(db.Integer, primary_key=True) 
    terms = db.Column(db.String(50), unique=True)
      
    def get_id(self):
        return (self.terms_id)
        
    def __repr__(self):
        return f'Terms ({self.terms_id}): {self.terms}'

# Job status data-model
class Job_Status(db.Model):
    # Table name
    __tablename__ = 'job_status'
    # Main Fields
    status_id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(50), unique=True)
      
    def get_id(self):
        return (self.status_id)
        
    def __repr__(self):
        return f'Status ({self.status_id}): {self.title}'

# Employee status data-model
class Employee_Status(db.Model):
    # Table name
    __tablename__ = 'employee_status'
    # Main Fields
    status_id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(50), unique=True)
      
    def get_id(self):
        return (self.status_id)
        
    def __repr__(self):
        return f'Status ({self.status_id}): {self.title}'

# Title data-model
class Title(db.Model):
    # Table name
    __tablename__ = 'employee_title'
    # Main Fields
    title_id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(50), unique=True)
      
    def get_id(self):
        return (self.title_id)
        
    def __repr__(self):
        return f'Title ({self.title_id}): {self.title}'

# Gender data-model
class Gender(db.Model):
    # Table name
    __tablename__ = 'employee_gender'
    # Main Fields
    gender_id = db.Column(db.Integer, primary_key=True) 
    gender = db.Column(db.String(50), unique=True)
      
    def get_id(self):
        return (self.gender_id)
        
    def __repr__(self):
        return f'gender ({self.gender_id}): {self.gender}'

# Marital data-model
class Marital(db.Model):
    # Table name
    __tablename__ = 'employee_marital'
    # Main Fields
    marital_id = db.Column(db.Integer, primary_key=True) 
    marital_status = db.Column(db.String(50), unique=True)
      
    def get_id(self):
        return (self.marital_id)
        
    def __repr__(self):
        return f'Marital ({self.marital_id}): {self.marital_status}'

# Employee data-model
class Employee(db.Model):
    # Table name
    __tablename__ = 'employee'
    # Main Fields
    employee_id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('employee_status.status_id'), default=1, nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    status = db.relationship(Employee_Status, foreign_keys=[status_id])
      
    def get_id(self):
        return (self.employee_id)
        
    def __repr__(self):
        return f'Employee ({self.employee_id}): {self.status.title}'

# Employee information data-model
class Employee_Info(db.Model):
    # Table name
    __tablename__ = 'employee_info'
    # Main Fields
    info_id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer, db.ForeignKey('employee_title.title_id'), nullable=False)
    given_name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    passport_no = db.Column(db.String(50))
    id_card_no = db.Column(db.String(50))
    nationality = db.Column(db.String(100))
    place_of_birth_id = db.Column(db.Integer, db.ForeignKey('country.country_id'), nullable=False)
    birthdate= db.Column(db.Date, nullable=False)
    gender_id = db.Column(db.Integer, db.ForeignKey('employee_gender.gender_id'), nullable=False)
    marital_id = db.Column(db.Integer, db.ForeignKey('employee_marital.marital_id'), nullable=False)
    tin = db.Column(db.String(50))
    ssn = db.Column(db.String(50))
    iban = db.Column(db.String(50))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id', ondelete='CASCADE'), nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    title = db.relationship(Title, foreign_keys=[title_id])
    place_of_birth = db.relationship(Country, foreign_keys=[place_of_birth_id])
    gender= db.relationship(Gender, foreign_keys=[gender_id])
    marital = db.relationship(Marital, foreign_keys=[marital_id])
    employee = db.relationship(Employee, foreign_keys=[employee_id])
      
    def get_id(self):
        return (self.info_id)
        
    def __repr__(self):
        return f'Employee info ({self.info_id}): {self.given_name} {self.surname}'

# Email data-model
class Email(db.Model):
    # Table name
    __tablename__ = 'employee_email'
    # Main Fields
    email_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    label = db.Column(db.String(20))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id', ondelete='CASCADE'), nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    employee = db.relationship(Employee, foreign_keys=[employee_id])

    def get_id(self):
        return (self.email_id)
        
    def __repr__(self):
        return f'Email ({self.email_id}): {self.email}'

# Phone data-model
class Phone(db.Model):
    # Table name
    __tablename__ = 'employee_phone'
    # Main Fields
    phone_id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(50))
    dial_code = db.Column(db.String(4), nullable=False)
    label = db.Column(db.String(20))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id', ondelete='CASCADE'), nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    employee = db.relationship(Employee, foreign_keys=[employee_id])

    def get_id(self):
        return (self.phone_id)
        
    def __repr__(self):
        return f'Phone ({self.phone_id}): {self.phone_number}'

# Address data-model
class Address(db.Model):
    # Table name
    __tablename__ = 'employee_address'
    # Main Fields
    address_id = db.Column(db.Integer, primary_key=True)
    address1 = db.Column(db.String(50))
    address2 = db.Column(db.String(50))
    postal_code = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id', ondelete='CASCADE'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id', ondelete='CASCADE'), nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    country = db.relationship(Country, foreign_keys=[country_id])
    employee = db.relationship(Employee, foreign_keys=[employee_id])

    def get_id(self):
        return (self.address_id)
        
    def __repr__(self):
        return f'Address ({self.address_id}): {self.address1}\
            \n{self.address2}\
            \n{self.postal_code} {self.city}\
            \n{self.state}\
            \n{self.country_id}'

# Job history data-model
class Job_History(db.Model):
    # Table name
    __tablename__ = 'job_history'
    # Main Fields
    job_history_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id', ondelete='CASCADE'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id', ondelete='RESTRICT'), nullable=False)
    terms_id = db.Column(db.Integer, db.ForeignKey('job_terms.terms_id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('job_status.status_id'), default=1, nullable=False)
    start_date= db.Column(db.Date, nullable=False)
    end_date= db.Column(db.Date, nullable=True)
    # ForeignKeys
    employee = db.relationship(Employee, foreign_keys=[employee_id])
    department = db.relationship(Department, foreign_keys=[department_id])
    job = db.relationship(Job, foreign_keys=[job_id])
    job_terms = db.relationship(Job_Terms, foreign_keys=[terms_id])
    job_status = db.relationship(Job_Status, foreign_keys=[status_id])
      
    def get_id(self):
        return (self.job_history_id)
    
    def __repr__(self):
        return f'Employee ({self.job_history_id}): {self.employee.employee_name} {self.employee.employee_surname}'

# Leave type data-model
class Leave_Type(db.Model):
    # Table name
    __tablename__ = 'leave_type'
    # Main Fields
    type_id = db.Column(db.Integer, primary_key=True) 
    type_title = db.Column(db.String(50), unique=True)
      
    def get_id(self):
        return (self.type_id)
        
    def __repr__(self):
        return f'Leave type ({self.type_id}): {self.type_title}'

# Leave balance data-model
class Leave_Balance(db.Model):
    # Table name
    __tablename__ = 'leave_balance'
    # Main Fields
    balance_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id', ondelete='CASCADE'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('leave_type.type_id'), nullable=False)
    leave_days = db.Column(db.Numeric(5,2), default=0.00)
    leave_taken = db.Column(db.Numeric(5,2), default=0.00)
    leave_balance = db.Column(db.Numeric(5,2), default=0.00)
    expiry_date = db.Column(db.DateTime)
    modified = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    employee = db.relationship(Employee, foreign_keys=[employee_id])
    leave_type = db.relationship(Leave_Type, foreign_keys=[type_id])

    def leave_remaining(self):
        self.leave_balance = self.leave_days - self.leave_taken
        return (self.leave_balance)
      
    def get_id(self):
        return (self.type_id)
        
    def __repr__(self):
        return f'Leave balance ({self.balance_id})'

# Leave taken data-model
class Leave_Taken(db.Model):
    # Table name
    __tablename__ = 'leave_taken'
    # Main Fields
    taken_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id', ondelete='CASCADE'), nullable=False)
    balance_id = db.Column(db.Integer, db.ForeignKey('leave_balance.balance_id', ondelete='CASCADE'), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    modified = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    employee = db.relationship(Employee, foreign_keys=[employee_id])
    leave_balance = db.relationship(Leave_Balance, foreign_keys=[balance_id])

    def delta(self):
        delta = self.end_date - self.start_date
        return delta.days + 1
      
    def get_id(self):
        return (self.taken_id)
        
    def __repr__(self):
        return f'Leave taken ({self.balance_id})'

# Period data-model
class Period(db.Model):
    # Table name
    __tablename__ = 'period'
    # Main Fields
    period_id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(50), unique=True)
      
    def get_id(self):
        return (self.type_id)
        
    def __repr__(self):
        return f'Period ({self.period_id}): {self.title}'

# Salary data-model
class Salary(db.Model):
    # Table name
    __tablename__ = 'salary'
    # Main Fields
    salary_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id', ondelete='CASCADE'), nullable=False)
    gross_value = db.Column(db.Numeric(10,2), default=0.00)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.currency_id'), nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    employee = db.relationship(Employee, foreign_keys=[employee_id])
    currency = db.relationship(Currency, foreign_keys=[currency_id])

    def get_work_hours(self, work_log):      
        return work_hours(work_log)
    
    def get_work_time(self, work_log):      
        return work_time(work_log, 4)
    
    def get_amount(self, work_log):      
        return work_time(work_log, 4) * self.gross_value
              
    def get_id(self):
        return (self.salary_id)
        
    def __repr__(self):
        return f'Salary ({self.salary_id})'

# Allowance type data-model
class Allowance_Type(db.Model):
    # Table name
    __tablename__ = 'allowance_type'
    # Main Fields
    allowance_type_id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(50), unique=True)
      
    def get_id(self):
        return (self.type_id)
        
    def __repr__(self):
        return f'Allowance type ({self.allowance_type_id}): {self.title}'

# Allowance data-model
class Allowance(db.Model):
    # Table name
    __tablename__ = 'allowance'
    # Main Fields
    allowance_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id', ondelete='CASCADE'), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey('period.period_id'), nullable=False)
    allowance_type_id = db.Column(db.Integer, db.ForeignKey('allowance_type.allowance_type_id'), nullable=False)
    gross_value = db.Column(db.Numeric(10,2), default=0.00)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.currency_id'), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    employee = db.relationship(Employee, foreign_keys=[employee_id])
    period = db.relationship(Period, foreign_keys=[period_id])
    allowance_type = db.relationship(Allowance_Type, foreign_keys=[allowance_type_id])
    currency = db.relationship(Currency, foreign_keys=[currency_id])

    def get_amount(self, work_log):      
        return work_time(work_log, self.period_id) * self.gross_value

    def get_id(self):
        return (self.allowance_id )
        
    def __repr__(self):
        return f'Allowance ({self.allowance_id}): {self.allowance_type.title}'

# Attendance log data-model
class Attendance_Log(db.Model):
    # Table name
    __tablename__ = 'attendance_log'
    # Main Fields
    log_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    employee = db.relationship(Employee, foreign_keys=[employee_id])

    def delta(self):
        delta = self.end_time - self.start_time
        return delta
    
    def get_attendance(self, attendance_log):      
        return cal_attendance(attendance_log, 20, 3)
    
    def get_id(self):
        return (self.log_id )
        
    def __repr__(self):
        return f'Attendance log ({self.log_id})'


# Payroll data-model
class Payroll(db.Model):
    # Table name
    __tablename__ = 'payroll'
    # Main Fields
    payroll_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee_info.employee_id'), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    gross_income = db.Column(db.Numeric(10,2), default=0)
    adjustment = db.Column(db.Numeric(10,2), default=0)
    income_tax = db.Column(db.Numeric(10,2), default=0)
    net_income = db.Column(db.Numeric(10,2), default=0)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.currency_id'), nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    employee = db.relationship(Employee_Info, foreign_keys=[employee_id])
    currency = db.relationship(Currency, foreign_keys=[currency_id])

    def get_id(self):
        return (self.payroll_id )
        
    def __repr__(self):
        return f'Allowance ({self.payroll_id})'
    
# Holiday data-model
class Holiday(db.Model):
    # Table name
    __tablename__ = 'holiday'
    # Main Fields
    holiday_id = db.Column(db.Integer, primary_key=True)
    holiday = db.Column(db.String(50), unique=True)
    holiday_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def get_id(self):
        return (self.holiday_id)
        
    def __repr__(self):
        return f'Holiday ({self.holiday_id}) {self.holiday}'