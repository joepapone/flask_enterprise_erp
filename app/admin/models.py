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

