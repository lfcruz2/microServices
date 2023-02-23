import os

from flask_cors import CORS
from flask_jwt_extended import JWTManager

from project.models import Airport, AirportSchema
from project.models import db
from project.server import create_app
from project.server.journey import insertionDB

airport_schema = AirportSchema()

app = create_app('default')
app_context = app.app_context()
app_context.push()

# db setup
with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()
    insertionDB.airportInsertionCommands()
    insertionDB.routeInsertionCommands()

# Cors
cors = CORS()
jwt = JWTManager(app)


# check-health-component
@app.route('/ping', methods=['GET'])
def ping():
    app_name = os.getenv('FLASK_APP_NAME')
    return {
                   "message": f"pong from {app_name} app",
                   "status": "success"
           }, 200


# CREATE DATA related with airpots code
@app.route('/createAirportData', methods=['GET'])
def AirportResourceCreation():
    start_all_airport = airport_schema.dump(Airport.query.all(), many=True)
    insertionDB.airportInsertionCommands()
    end_all_airport = airport_schema.dump(Airport.query.all(), many=True)
    return {"message": f"Data created. From {len(start_all_airport)} registers to {len(end_all_airport)}",
            "status": "success"}, 200
