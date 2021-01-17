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

@app.route('/')
@app.route('/inspect/users')
def show_users():
    columns = ['email', 'name', 'phone', 'birthday', 'rating']
    users = []
    for user in UserModel.query.all():
        users.append([user.id, user.name, user.phone, user.birthday, str(user.rating)])
    return render_template('table.html', records=users, colnames=columns, tablename='USERS', size=len(columns))

@app.route('/inspect/barbershops')
def show_barbershops():
    columns = ['id', 'name', 'address', 'rating', 'coordX', 'coordY']
    barbershops = []
    for bbs in BarbershopModel.query.all():
        barbershops.append([bbs.id, bbs.name, bbs.address, str(bbs.rating), str(bbs.coordX), str(bbs.coordY)])
    return render_template('table.html', records=barbershops, colnames=columns, tablename='BARBERSHOPS', size=len(columns))

@app.route('/inspect/barbers')
def show_barbers():
    columns = ['id', 'name', 'rating', 'bbs_id']
    barbers = []
    for barber in BarberModel.query.all():
        barbers.append([barber.id, barber.name, str(barber.rating), barber.bbs_id])
    return render_template('table.html', records=barbers, colnames=columns, tablename='BARBERS', size=len(columns))

@app.route('/inspect/services')
def show_services():
    columns = ['id', 'name', 'price', 'bbs_id']
    services = []
    for serv in ServiceModel.query.all():
        services.append([serv.id, serv.name, str(serv.price), serv.bbs_id])
    return render_template('table.html', records=services, colnames=columns, tablename='SERVICES', size=len(columns))

@app.route('/inspect/appointments')
def show_appointments():
    columns = ['id', 'date', 'time', 'barber_id', 'client_id', 'service_id']
    appointments = []
    for app in AppointmentModel.query.all():
        appointments.append([app.id, app.date, app.time, app.barber_id, app.client_id, app.service_id])
    return render_template('table.html', records=appointments, colnames=columns, tablename='APPOINTMENTS', size=len(columns))

if __name__ == '__main__':
    app.run(host='0.0.0.0')