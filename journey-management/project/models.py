import hashlib
from datetime import datetime, timedelta
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
Journeys
id  (número)    --> 	identificador del trayecto
sourceAirportCode  (cadena de caracteres)    --> 	código del aeropuerto de origen (ver)
sourceCountry	(cadena de caracteres)    --> 	país de origen
destinyAirportCode	(cadena de caracteres)    --> 	código del aeropuerto de destino (ver)
destinyCountry	(cadena de caracteres)    --> 	país de destino
bagCost	(número)    --> 	costo del envío de una maleta en el trayecto
createdAt	(datetime)    --> 	fecha de creación del trayecto 
'''


class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sourceAirportCode = db.Column(db.String(10), unique=False, nullable=False)
    sourceCountry = db.Column(db.String(80), unique=False, nullable=False)
    destinyAirportCode = db.Column(db.String(10), unique=False, nullable=False)
    destinyCountry = db.Column(db.String(80), unique=False, nullable=False)
    bagCost = db.Column(db.Integer)
    createdAt = db.Column(db.String(80), default=datetime.utcnow)
    expiredAt = db.Column(db.String(80))

    def __init__(self, sourceAirportCode, sourceCountry, destinyAirportCode, destinyCountry, bagCost, createdAt, expiredAt):
        self.sourceAirportCode = sourceAirportCode
        self.sourceCountry = sourceCountry
        self.destinyAirportCode = destinyAirportCode
        self.destinyCountry = destinyCountry
        self.bagCost = bagCost
        self.createdAt = createdAt
        self.expiredAt = expiredAt

    def __repr__(self):
        return f"<Journey sourceAirportCode:{self.sourceAirportCode}, " \
               f"sourceCountry:{self.sourceCountry}, " \
               f"destinyAirportCode:{self.destinyAirportCode}, " \
               f"destinyCountry:{self.destinyCountry}, " \
               f"bagCost:{self.bagCost}, " \
               f"createdAt:{self.createdAt}, " \
               f"expiredAt:{self.expiredAt} >"


# Serializations
# Journeys
class JourneySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Journey
        include_relationship = True
        load_instance = True


class Airport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=False, nullable=False)
    aeropuerto = db.Column(db.String(80), unique=False, nullable=False)
    ciudad = db.Column(db.String(50), unique=False, nullable=False)
    region_estado = db.Column(db.String(50), unique=False, nullable=False)
    pais = db.Column(db.String(50), unique=False, nullable=False)

    def __init__(self, codigo, aeropuerto, ciudad, region_estado, pais):
        self.codigo = codigo
        self.aeropuerto = aeropuerto
        self.ciudad = ciudad
        self.region_estado = region_estado
        self.pais = pais


# Serializations
# Airport
class AirportSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Airport
        include_relationship = True
        load_instance = True
