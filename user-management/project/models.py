# user-management/project/models.py

from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_sqlalchemy import SQLAlchemy
#import hashlib

# db setup
db = SQLAlchemy()

# Users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    salt = db.Column(db.String(120), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    """ def set_password(self, password):
        self.salt = hashlib.sha256(str(datetime.now()).encode('utf-8')).hexdigest()
        self.password = hashlib.sha256((password + self.salt).encode('utf-8')).hexdigest()

    def check_password(self, password):
        return self.password == hashlib.sha256((password + self.salt).encode('utf-8')).hexdigest() """

    def __init__(self, username, email, password, salt):
        self.username = username
        self.email = email
        self.password = password
        self.salt = salt

    def __repr__(self):
        return '<User %r>' % self.username

# Serializations
# Users
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationship = True
        load_instance = True