from .. import db
from datetime import datetime


# Currency data-model
class Currency(db.Model):
    # Table name
    __tablename__ = 'currency'
    # Main Fields
    currency_id = db.Column(db.Integer, primary_key=True)
    currency_name = db.Column(db.String(50))
    currency_code = db.Column(db.String(3), nullable=False)
    currency_no = db.Column(db.Integer, nullable=False)
    
    def get_id(self):
        return (self.currency_id)
    
    def __repr__(self):
        return f'Currency: {self.currency_code} ({self.currency_id})'


# Country data-model
class Country(db.Model):
    # Table name
    __tablename__ = 'country'
    # Main Fields
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(50))
    country_no = db.Column(db.Integer, nullable=False)
    alpha2_code = db.Column(db.String(2), nullable=False)
    dial_code = db.Column(db.String(4), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.currency_id'), nullable=False)
    # ForeignKeys
    currency = db.relationship(Currency, foreign_keys=[currency_id])

    def get_id(self):
        return (self.country_id)
    
    def __repr__(self):
        return f'Country: {self.country_name} ({self.country_id})'


# Tax data-model
class Tax(db.Model):
    # Table name
    __tablename__ = 'tax'
    # Main Fields
    tax_id = db.Column(db.Integer, primary_key=True)
    tax_description = db.Column(db.String(50))
    tax_rate = db.Column(db.Numeric, nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    def get_id(self):
        return (self.tax_id)
    
    def __repr__(self):
        return f'Tax: {self.tax_description} ({self.tax_id})'


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


# Job history data-model
class Job_History(db.Model):
    # Table name
    __tablename__ = 'job_history'
    # Main Fields
    event_id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, nullable=False)
    event_description = db.Column(db.String(150))
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    def __init__(self, job_id, event_description):
        self.job_id = job_id
        self.event_description = event_description
    
    def __repr__(self):
        return f'Event: {self.event_description} ({self.event_id})'

