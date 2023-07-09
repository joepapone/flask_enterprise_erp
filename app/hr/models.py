from .. import db
from datetime import datetime
from ..admin.models import Country, Department, Job


# Terms data-model
class Terms(db.Model):
    # Table name
    __tablename__ = 'employee_terms'
    # Main Fields
    terms_id = db.Column(db.Integer, primary_key=True) 
    terms = db.Column(db.String(50), unique=True)
      
    def get_id(self):
        return (self.terms_id)
        
    def __repr__(self):
        return f'Terms: {self.terms} ({self.terms_id})'


# Status data-model
class Status(db.Model):
    # Table name
    __tablename__ = 'employee_status'
    # Main Fields
    status_id = db.Column(db.Integer, primary_key=True) 
    status_title = db.Column(db.String(50), unique=True)
      
    def get_id(self):
        return (self.status_id)
        
    def __repr__(self):
        return f'Status: {self.status_title} ({self.status_id})'
    

# Employee data-model
class Employee(db.Model):
    # Table name
    __tablename__ = 'employee'
    # Main Fields
    employee_id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(50))
    employee_surname = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'), nullable=False)
    terms_id = db.Column(db.Integer, db.ForeignKey('employee_terms.terms_id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('employee_status.status_id'), nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    department = db.relationship(Department, foreign_keys=[department_id])
    job = db.relationship(Job, foreign_keys=[job_id])
    terms = db.relationship(Terms, foreign_keys=[terms_id])
    status = db.relationship(Status, foreign_keys=[status_id])
      
    def get_id(self):
        return (self.employee_id)
        
    def __repr__(self):
        return f'Employee: {self.employee_name} ({self.employee_id})'


# employee history data-model
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
        return f'Event: {self.event_description} ({self.event_id})'


# Email data-model
class Email(db.Model):
    # Table name
    __tablename__ = 'email'
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
        return f'Status: {self.email} ({self.email_id})'


# Phone data-model
class Phone(db.Model):
    # Table name
    __tablename__ = 'phone'
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
        return f'Status: {self.phone_number} ({self.phone_id})'


