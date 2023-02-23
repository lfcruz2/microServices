from datetime import datetime, timedelta

import jwt
from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Resource, Api
from sqlalchemy import Unicode, text, column

from ...models import Journey, JourneySchema, AirportSchema, Airport
from ...server import db

airport_schema = AirportSchema()
journey_schema = JourneySchema()

journey_api = Blueprint("journey_api", __name__, url_prefix="/routes")
api = Api(journey_api)


def validateUser(token_header):
    user_id, respuesta = None, None
    if not token_header or token_header is None:
        respuesta = {
                            "message": "Bearer token is missing in request",
                            "status": "fail"
                    }, 400
        return user_id, respuesta
    token = token_header.split(" ")[1]

    try:
        user_id = jwt.decode(token, 'frase-secreta', algorithms=['HS256'])['sub']
    except (jwt.exceptions.InvalidTokenError, KeyError):
        respuesta = {
                            "message": "Token not valid",
                            "status": "fail"
                    }, 401
        return user_id, respuesta
    return user_id, respuesta


def validateInteger(numero_a_validar):
    try:
        numero_a_validar = int(numero_a_validar)
        if type(numero_a_validar) == int:
            return numero_a_validar
    except Exception as e:
        return {"message": "El id no es un número.", "status": "fail"}, 400


def getJourneyById(entry_id):
    entry_id = validateInteger(entry_id)

    if type(entry_id) != int:
        return {"message": "El id no es un número.", "status": "fail"}, 400

    journeyDB = db.session.query(Journey).filter(Journey.id == entry_id).first()

    if not journeyDB:
        return {"message": "No existe el trayecto con ese identificador.",
                "status": "fail"
                }, 404
    return journey_schema.dump(journeyDB), 200


def getFindByEntrycodeDestinationCodeDate(origin, destination, query_time_date, today_date):
    if today_date is None:
        time_now = datetime.utcnow()
    else:
        time_now = today_date

    stmt = text("SELECT id as id, sourceAirportCode, sourceCountry, destinyAirportCode, "
                "destinyCountry, createdAt, expiredAt, bagCost "
                "FROM Journey WHERE ( (sourceAirportCode like :origin or :origin is null) "
                "AND (destinyAirportCode like :destination or :destination is null) "
                "AND (expiredAt > :query_time_date or :query_time_date is null)  "
                "AND (createdAt < :query_time_date or :query_time_date is null) )  "
                "or ( (sourceAirportCode like :origin or :origin is null)  "
                "AND (destinyAirportCode like :destination or :destination is null)  "
                "AND (expiredAt > :time_now or :time_now is null)  "
                "AND (createdAt < :time_now or :time_now is null) ) "). \
        bindparams(origin=origin, destination=destination, query_time_date=query_time_date, time_now=time_now). \
        columns(column('id', Unicode), column('sourceAirportCode', Unicode), column('sourceCountry', Unicode),
                column('destinyAirportCode', Unicode), column('destinyCountry', Unicode),
                column('createdAt', Unicode),
                column('expiredAt', Unicode), column('bagCost', Unicode))

    result_all = db.session.execute(stmt).fetchall()
    if not result_all:
        return journey_schema.dump(Journey.query.all(), many=True), 200
    return [journey_schema.dump(row) for row in result_all], 200


def postNewJourney(new_journey):
    if new_journey.createdAt is None:
        time_now = datetime.utcnow()
        new_journey.expiredAt = datetime.utcnow() + timedelta(days=30)
    else:
        time_now = new_journey.createdAt

    sourceAirportCode = new_journey.sourceAirportCode
    destinyAirportCode = new_journey.destinyAirportCode

    if len(Airport.query.filter(Airport.codigo.in_([sourceAirportCode,
                                                    destinyAirportCode])).all()) < 2:
        return {
                       "message": "Ingrese codigos de aeropuertos validos",
                       "status": "fail"
               }, 400

    if Journey.query.filter(Journey.sourceAirportCode.like(sourceAirportCode),
                            Journey.destinyAirportCode.like(destinyAirportCode),
                            Journey.expiredAt > time_now,
                            Journey.createdAt < time_now).first():
        print(Journey.query.filter(Journey.sourceAirportCode.like(sourceAirportCode),
                            Journey.destinyAirportCode.like(destinyAirportCode),
                            Journey.expiredAt > time_now,
                            Journey.createdAt < time_now).first())
        return {
                       "message": "El trayecto ya exista y esté activo",
                       "status": "fail"
               }, 412

    new_journey = Journey(sourceAirportCode=sourceAirportCode,
                          sourceCountry=new_journey.sourceCountry,
                          destinyAirportCode=destinyAirportCode,
                          destinyCountry=new_journey.destinyCountry,
                          bagCost=new_journey.bagCost,
                          createdAt=time_now,
                          expiredAt=new_journey.expiredAt
                          )

    db.session.add(new_journey)
    db.session.commit()

    # if (datetime.strptime(new_journey.createdAt, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=1)) and (
    #         new_journey.createdAt != '2023-02-13 01:11:11.000000'):
    #     return {
    #                    "message": "Token expired",
    #                    "status": "fail"
    #            }, 401

    created_journey = journey_schema.dump(new_journey)
    return {
                   "id": created_journey['id'],
                   "createdAt": datetime.strptime(created_journey['createdAt'],
                                                  '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d'),
                   "expiredAt": datetime.strptime(created_journey['expiredAt'],
                                                  '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')
           }, 201


# -------------------------------------------------------------------------------------------------
# /routes/
class JourneyResource(Resource):

    # /routes
    @classmethod
    def get(cls):
        if request.args or 'from' in request.args or 'to' in request.args or 'when' in request.args:
            return cls.buscar_trayectos()
        if not request.args and 'from' not in request.args and 'to' not in request.args and 'when' not in request.args:
            return journey_schema.dump(Journey.query.all(), many=True), 200
        else:
            return {"message": "No existe dicho metodo por favor revise los parametros", "status": "fail"}, 404

    @classmethod
    def buscar_trayectos(cls):

        user_id, respuesta = validateUser(request.headers.get('Authorization', None))

        if respuesta is not None:
            return respuesta

        origin, destination, query_time_date, today_date = None, None, None, None
        if user_id is not None:
            origin = request.args.get('from', type=str)
            if origin is not None and type(origin) != str:
                return {"message": "Alguno de los valores no tiene un formato correcto. [from]", "status": "fail"}, 400
            destination = request.args.get('to', type=str)
            if destination is not None and type(destination) != str:
                return {"message": "Alguno de los valores no tiene un formato correcto. [to]", "status": "fail"}, 400
            try:
                # datetime.strptime("2011-03-07", "%Y-%m-%d")
                query_time_str = request.args.get('when', type=str)
                query_time_date = None
                if query_time_str is not None:
                    query_time_date = datetime.strptime(query_time_str, "%Y-%m-%d")
            except Exception as e:
                return {
                               "message": "Alguno de los valores no tiene un formato incorrecto. [when] use formato 2023-01-01 "
                                          "-- %Y-%m-%d ", "status": "fail"}, 400
            return getFindByEntrycodeDestinationCodeDate(origin, destination, query_time_date, today_date)
        else:
            return {
                           "message": "Usurio no identificado",
                           "status": "fail"
                   }, 400

    # /routes
    def post(self):

        print(request.headers.get('Authorization', None))

        user_id, respuesta = validateUser(request.headers.get('Authorization', None))

        if respuesta is not None:
            return respuesta

        if user_id is not None:

            # verify that all fields are present
            if 'sourceAirportCode' not in request.json \
                    or 'sourceCountry' not in request.json \
                    or 'destinyAirportCode' not in request.json \
                    or 'destinyCountry' not in request.json \
                    or 'bagCost' not in request.json :
                return {
                               "message": "All fields are required",
                               "status": "fail"
                       }, 400

            sourceAirportCode = request.json['sourceAirportCode']
            sourceCountry = request.json['sourceCountry']
            destinyAirportCode = request.json['destinyAirportCode']
            destinyCountry = request.json['destinyCountry']
            bagCost = request.json['bagCost']
            time_now = None
            expiredAt = None

            if not all([sourceAirportCode, sourceCountry, destinyAirportCode, destinyCountry, bagCost]):
                return {
                               "message": "Todos los campos son requeridos",
                               "status": "fail"
                       }, 400

            new_journey = Journey(sourceAirportCode, sourceCountry, destinyAirportCode,
                                  destinyCountry, bagCost, time_now, expiredAt)

            return postNewJourney(new_journey)
        else:
            return {
                           "message": "Usurio no identificado",
                           "status": "fail"
                   }, 400


# -------------------------------------------------------------------------------------------------
# /routes/<int:id_post>
class GetJourneyResource(Resource):

    def get(self, id_journey):

        user_id, respuesta = validateUser(request.headers.get('Authorization', None))

        if respuesta is not None:
            return respuesta

        if user_id is not None:
            return getJourneyById(id_journey)
        else:
            return {
                           "message": "Usurio no identificado",
                           "status": "fail"
                   }, 400


# -------------------------------------------------------------------------------------------------
# /routes/ping
class PingJourneyResource(Resource):

    def get(self):
        return {"message": "pong", "status": "success"}, 200


# ---------------------------------------------- AEROPORT -------------------------------------
# /GET ALL data related with airpots code
class AeroportResource(Resource):

    def get(self):
        return airport_schema.dump(Airport.query.all(), many=True), 200


# /GET ALL data related with airpots code
class AeroportByIdResource(Resource):

    def get(self, airport_id):

        entry_id = validateInteger(airport_id)

        if type(entry_id) != int:
            return {"message": "El id no es un número.", "status": "fail"}, 400

        airport = db.session.query(Airport).filter(Airport.id == airport_id).first()

        if not airport:
            return {"message": "Airport not found", "status": "fail"}, 404
        return {
                       "id": airport.id,
                       "codigo": airport.codigo,
                       "aeropuerto": airport.aeropuerto,
                       "ciudad": airport.ciudad,
                       "region_estado": airport.region_estado,
                       "pais": airport.pais
               }, 200


# /GET BY CODE data related with airpots code
class AeroportByCodeResource(Resource):

    def get(self, code_id):
        airport = db.session.query(Airport).filter(Airport.codigo == code_id).first()
        if not airport:
            return {"message": "Airport not found", "status": "fail"}, 404
        return {
                       "id": airport.id,
                       "codigo": airport.codigo,
                       "aeropuerto": airport.aeropuerto,
                       "ciudad": airport.ciudad,
                       "region_estado": airport.region_estado,
                       "pais": airport.pais
               }, 200


# -------------------------------------------------------------------------------------------------
# journeys_end_points
api.add_resource(JourneyResource, '/')
api.add_resource(GetJourneyResource, '/<id_journey>')
api.add_resource(PingJourneyResource, '/ping')
api.add_resource(AeroportResource, '/airportData')
api.add_resource(AeroportByIdResource, '/airportById/<airport_id>')
api.add_resource(AeroportByCodeResource, '/airportByCode/<code_id>')
