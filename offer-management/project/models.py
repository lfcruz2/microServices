#from .server import db
from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Offers
class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer)
    userId = db.Column(db.Integer)
    description = db.Column(db.String(140), nullable=True)
    size = db.Column(db.Text, nullable=True)
    fragile = db.Column(db.Boolean)
    offer = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
 
    def __init__(self, postId, userId, description, size, fragile, offer):
        self.postId = postId
        self.userId = userId
        self.description = description
        self.size = size
        self.fragile = fragile
        self.offer = offer

    def __repr__(self):
        return '<Offer %r>' % self.description

# Offers Serializations
class OfferSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Offer
        include_relationship = True
        load_instance = True