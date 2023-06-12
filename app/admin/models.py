from .. import db
from datetime import datetime


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
        return f'Job: {self.department_name} ({self.department_id})'


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
