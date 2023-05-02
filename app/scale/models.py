from datetime import datetime
from .. import db

class Cal(db.Model):
    __tablename__ = 'cal'
    id = db.Column(db.Integer, primary_key=True) # primary key required by SQLAlchemy
    raw_zero = db.Column(db.Numeric(10,3))
    raw_span = db.Column(db.Numeric(10,3))
    zero = db.Column(db.Numeric(10,2))
    span = db.Column(db.Numeric(10,2))
    offset = db.Column(db.Numeric(10,2))
    comments = db.Column(db.String(200))
    alarm_H = db.Column(db.Numeric(10,2))
    alarm_L = db.Column(db.Numeric(10,2))
    alarm_LL = db.Column(db.Numeric(10,2))
    modified = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return "<Cal #{:d}>".format(self.id)