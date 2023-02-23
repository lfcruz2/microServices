from random import randint
from project.server import create_app, db

from flask_cors import CORS
from flask_jwt_extended import JWTManager

import os

app = create_app('default')
app_context = app.app_context()
app_context.push()

# db setup
with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()

# Cors
cors = CORS()

# JWT
jwt = JWTManager(app)

# check-health-component
@app.route('/ping', methods=['GET'])
def ping():
    app_name = os.getenv('FLASK_APP_NAME')
    return {"message":f"pong from {app_name} app"}