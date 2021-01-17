from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
import math

db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = 'Users'
    id = db.Column('id', db.String(50), primary_key = True)
    name = db.Column('name', db.String(50))
    phone = db.Column('phone', db.String(12))
    birthday = db.Column('birthday', db.String(11))
    rating = db.Column('rating', db.Float)
    ratings_recv = db.Column('ratings_recv', db.Integer)

    def __init__(self, json_client):
        self.id = json_client['email']
        self.name = json_client['name']
        self.phone = json_client['phone']
        self.birthday = json_client['birthday']
        self.rating = 0
        self.ratings_recv = 0

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_in_db(self, json_client):
        self.name = json_client['name']
        self.phone = json_client['phone']
        self.birthday = json_client['birthday']
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        final_json = {
            'id' : self.id,
            'name' : self.name,
            'phone' : self.phone,
            'birthday' : self.birthday,
            'rating' : self.rating
        }
        return final_json


class BarbershopModel(db.Model):
    __tablename__ = 'Barbershops'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(40), unique=True)
    address = db.Column('address', db.String(50))
    rating = db.Column('rating', db.Float)
    ratings_recv = db.Column('ratings_recv', db.Integer)
    coordX = db.Column('coordX', db.Float)
    coordY = db.Column('coordY', db.Float)

    def __init__(self, json_bbs):
        self.name = json_bbs['name']
        self.address = json_bbs['address']
        self.rating = json_bbs['rating']
        self.ratings_recv = json_bbs['ratings_recv']
        self.coordX = json_bbs['coordX']
        self.coordY = json_bbs['coordY']

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'address' : self.address,
            'rating' : self.rating,
            'coordX' : self.coordX,
            'coordY' : self.coordY
        }


class BarberModel(db.Model):
    __tablename__ = 'Barbers'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(30))
    rating = db.Column('rating', db.Float)
    ratings_recv = db.Column('ratings_recv', db.Integer)
    bbs_id = db.Column('bbs_id', db.Integer, db.ForeignKey('Barbershops.id'))

    def __init__(self, json_barber):
        self.name = json_barber['name']
        self.rating = json_barber['rating']
        self.ratings_recv = json_barber['ratings_recv']
        self.bbs_id = json_barber['bbs_id']

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
                'id' : self.id,
                'name' : self.name,
                'rating' : self.rating,
                'bbs_id' : self.bbs_id
        }
           

class ServiceModel(db.Model):
    __tablename__ = 'Services'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(50))
    price = db.Column('price', db.Integer)
    bbs_id = db.Column('bbs_id', db.Integer, db.ForeignKey('Barbershops.id'))

    def __init__(self, json_service):
        self.name = json_service['name']
        self.price = json_service['price']
        self.bbs_id = json_service['bbs_id']

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
                'id' : self.id,
                'name' : self.name,
                'price' : self.price,
                'bbs_id' : self.bbs_id
        }

class AppointmentModel(db.Model):
    __tablename__ = 'Appointments'
    id = db.Column('id', db.Integer, primary_key = True)
    date = db.Column('date', db.String(50))
    time = db.Column('time', db.String(50))
    barber_id = db.Column('barber_id', db.Integer, db.ForeignKey('Barbers.id'))
    client_id = db.Column('client_id', db.String(50), db.ForeignKey('Users.id'))
    service_id = db.Column('service_id', db.Integer, db.ForeignKey('Services.id'))

    def __init__(self, json_appointment):
        self.date = json_appointment['date']
        self.time = json_appointment['time']
        self.barber_id = json_appointment['barber_id']
        self.client_id = json_appointment['email']
        self.service_id = json_appointment['service_id']

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
                'id' : self.id,
                'date' : self.date,
                'time' : self.time,
                'barber_id' : self.barber_id,
                'client_id' : self.client_id,
                'service_id' : self.service_id
        }