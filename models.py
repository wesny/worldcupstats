from app import db
from sqlalchemy.dialects.postgresql import JSON

class Team(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    role = db.Column(db.String())

    def __init__(self, name, role):
        self.name = name
        self.role = role

    def __repr__(self):
        return '<id {}>'.format(self.id)