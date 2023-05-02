from ... import db


# define the Role data-model
class Role(db.Model):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True)
    role_attribute = db.Column(db.String(50), unique=True)
    #user_role = db.relationship('Role', backref='user')
    
    def __init__(self, role_id, role_attribute):
        self.role_id = role_id
        self.role_attribute = role_attribute

    def __repr__(self):
        return f'({self.role_id},"{self.role_attribute}")'