from flask_login import UserMixin
from datetime import datetime

from os import urandom
from hashlib import pbkdf2_hmac
from hmac import compare_digest
from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy.orm import relationship, backref
from .. import db

'''
# define User data-model
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(120), unique=True)
    user_name = db.Column(db.String(50))
    _hash = db.Column(db.LargeBinary(255))
    _salt = db.Column(db.LargeBinary(255))
    role_id = db.Column(db.Integer())
    #role_id = db.Column(db.Integer(), db.ForeignKey('role.role_id'))
    created = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

    
    #role = relationship("user", backref=backref('role'))
    #role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    #FOREIGN KEY (role_id) REFERENCES role(role_id)


    @hybrid_property
    def password(self):
        print('Password: '.format(self._hash))
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
        return "<User #{:d}>".format(self.user_id)

'''
'''
# define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    role_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
'''
