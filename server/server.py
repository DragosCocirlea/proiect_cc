from flask import Flask, render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from models import BarbershopModel, BarberModel, UserModel, ServiceModel, AppointmentModel, db
import init_functions
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@dbserver:3306/figaro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.app_context().push()

api = Api(app)

# create the database and the needed tables if they don't already exist
from sqlalchemy import create_engine
engine = create_engine('mysql://root:root@dbserver:3306/')
engine.execute("CREATE DATABASE IF NOT EXISTS figaro;")
db.app = app
db.init_app(app)
db.create_all()

# add initial data if it's not already there
if BarbershopModel.query.count() == 0:
    init_functions.init_db_data()

import resources
api.add_resource(resources.UserData, '/user')
api.add_resource(resources.BarbershopData, '/barbershop')
api.add_resource(resources.BarberServiceData, '/barbers_services')
api.add_resource(resources.TimeData, '/time')
api.add_resource(resources.AppointmentData, '/appointment')

if __name__ == '__main__':
    app.run(host='0.0.0.0')