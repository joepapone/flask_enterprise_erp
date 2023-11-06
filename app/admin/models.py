from flask_login import UserMixin
from datetime import datetime
from os import urandom
from hashlib import pbkdf2_hmac
from hmac import compare_digest
from sqlalchemy.ext.hybrid import hybrid_property
from .. import db


# Role data-model
class Role(db.Model):
    # Table name
    __tablename__ = 'role'
    # Main Fields
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True)
             
    def get_id(self):
        return (self.role_id)

    def __repr__(self):
        #return f'Role ({self.role_id}): {self.role_name}'
        return self.role_name

# User data-model
class User(UserMixin, db.Model):
    # Table name
    __tablename__ = 'user'
    # Main Fields
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    user_name = db.Column(db.String(50))
    _hash = db.Column(db.LargeBinary(255))
    _salt = db.Column(db.LargeBinary(255))
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    # ForeignKeys
    role = db.relationship(Role, foreign_keys=[role_id])
    
    @hybrid_property
    def password(self):
        return self._hash

    # hash and salt passwords stored in database
    @password.setter
    def password(self, value):
        # create salt for first time user
        if self._salt is None:
            self._salt = urandom(16)
        self._hash = self._hash_password(value)

    def is_valid_password(self, password):
        """Ensure that the provided password is valid.

        Using this instead of ``sqlalchemy.types.TypeDecorator``
        (which would let us write ``User.password == password`` and have the incoming
        ``password`` be automatically hashed in a SQLAlchemy query)
        because ``compare_digest`` properly compares **all***
        the characters of the hash even when they do not match in order to
        avoid timing oracle side-channel attacks."""
        new_hash = self._hash_password(password)
        return compare_digest(new_hash, self._hash)

    def _hash_password(self, password):
        pwd = password.encode("utf-8")
        salt = bytes(self._salt)
        buff = pbkdf2_hmac("sha256", pwd, salt, iterations=100000)
        print('salt-{0}--pw{1}'.format(salt.hex,bytes(buff).hex))
        return bytes(buff)
    
    def get_id(self):
        return (self.user_id)
    
    def __repr__(self):
        return f'User: ({self.user_id}): {self.user_name}'
    

    '''
    class ProfileForm(Form):
    birthday  = DateTimeField('Your Birthday', format='%m/%d/%y')
    signature = TextAreaField('Forum Signature')

    class AdminProfileForm(ProfileForm):
    username = StringField('Username', [validators.Length(max=40)])
    level    = IntegerField('User Level', [validators.NumberRange(min=0, max=10)])
    '''

# Currency data-model
class Currency(db.Model):
    # Table name
    __tablename__ = 'currency'
    # Main Fields
    currency_id = db.Column(db.Integer, primary_key=True)
    currency_name = db.Column(db.String(50))
    currency_code = db.Column(db.String(3), nullable=False)
    currency_no = db.Column(db.Integer, nullable=False)
    currency_symbol = db.Column(db.String(10), nullable=False)
    
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

