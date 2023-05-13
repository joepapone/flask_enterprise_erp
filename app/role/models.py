from .. import db


# Define the Role data-model
class Role(db.Model):
    # Table name
    __tablename__ = 'role'
    # Main Fields
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True)
    
    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name = role_name

    def __repr__(self):
        return self.role_name
        #return f'({self.role_id},"{self._name}")'