from flask_login import UserMixin
from datetime import datetime
from .. import db
from ..role.models import Role

from os import urandom
from hashlib import pbkdf2_hmac
from hmac import compare_digest
from sqlalchemy.ext.hybrid import hybrid_property


# Define the User data-model
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
        return "<User #{:d}>".format(self.user_id)