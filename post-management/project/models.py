#from .server import db
from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    routeId = db.Column(db.Integer)
    userId = db.Column(db.Integer)
    plannedStartDate = db.Column(db.DateTime)
    plannedEndDate = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, routeId, userId, plannedStartDate, plannedEndDate):
            self.routeId = routeId
            self.userId = userId
            self.plannedStartDate = plannedStartDate
            self.plannedEndDate = plannedEndDate


# Serializations
# Posts
class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_relationship = True
        load_instance = True