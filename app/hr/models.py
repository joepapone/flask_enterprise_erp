from .. import db
from datetime import datetime
from ..admin.models import Country


# Title data-model
class Title(db.Model):
    # Table name
    __tablename__ = 'employee_title'
    # Main Fields
    title_id = db.Column(db.Integer, primary_key=True) 
    title_name = db.Column(db.String(50), unique=True)
      
    def get_id(self):
        return (self.title_id)
        
    def __repr__(self):
        return f'Tilte ({self.title_id}): {self.title_name}'

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
    title_id = db.Column(db.Integer, db.ForeignKey('employee_title.title_id'), nullable=False)
    employee_name = db.Column(db.String(50))
    employee_surname = db.Column(db.String(50))
    gender_id = db.Column(db.Integer, db.ForeignKey('employee_gender.gender_id'), nullable=False)
    marital_id = db.Column(db.Integer, db.ForeignKey('employee_marital.marital_id'), nullable=False)
    birthdate= db.Column(db.Date, nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    title = db.relationship(Title, foreign_keys=[title_id])
    gender= db.relationship(Gender, foreign_keys=[gender_id])
    marital = db.relationship(Marital, foreign_keys=[marital_id])
      
    def get_id(self):
        return (self.employee_id)
        
    def __repr__(self):
        return f'Employee ({self.employee_id}): {self.employee_name} {self.employee_surname}'

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
        return f'Department: {self.department_name} ({self.department_id})'

# Department history data-model
class Department_History(db.Model):
    # Table name
    __tablename__ = 'department_history'
    # Main Fields
    event_id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, nullable=False)
    event_description = db.Column(db.String(150))
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    def __init__(self, department_id, event_description):
        self.department_id = department_id
        self.event_description = event_description

    def __repr__(self):
        return f'Event: {self.event_description} ({self.event_id})'

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
        return f'Job: {self.job_title} ({self.job_id})'

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
    status_title = db.Column(db.String(50), unique=True)
      
    def get_id(self):
        return (self.status_id)
        
    def __repr__(self):
        return f'Status ({self.status_id}): {self.status_title}'

# Job history data-model
class Job_History(db.Model):
    # Table name
    __tablename__ = 'job_history'
    # Main Fields
    job_history_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'), nullable=False)
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

# Email data-model
class Email(db.Model):
    # Table name
    __tablename__ = 'employee_email'
    # Main Fields
    email_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    label = db.Column(db.String(20))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
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
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
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
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
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



# Employee history data-model
class Employee_History(db.Model):
    # Table name
    __tablename__ = 'employee_history'
    # Main Fields
    event_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    event_description = db.Column(db.String(150))
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    def __init__(self, employee_id, event_description):
        self.employee_id = employee_id
        self.event_description = event_description
    
    def __repr__(self):
        return f'Event ({self.event_id}): {self.event_description}'



