from flask_restful import Resource
from flask import request
from sqlalchemy.sql import text
from models import UserModel, BarbershopModel, BarberModel, ServiceModel, AppointmentModel
import geopy.distance
import requests
import json

def validateJWT(request):
    resp = requests.post('http://auth:5000/token/decode', headers = request.headers)
    response = json.loads(resp.text)
    if 'user_email' not in response:
            raise Exception('Invalid token')
    
    return response['user_email']

class UserData(Resource):
    def get(self):
        user_email = request.get_json()['email']
        try:
            user = UserModel.query.filter_by(id = user_email).first()
            return user.to_json(), 200
        except:
            return {'msg' : 'Couldn\'t get user from server db'}, 500


    def post(self):
        req_json = request.get_json()
        user_email = req_json['email']
        try:
            user = UserModel.query.filter_by(id = user_email).first()
            if user is None:
                user = UserModel(req_json)
                user.save_to_db()
                return {'msg' : 'User {} has been succesfully added to the db'.format(user_email)}, 200
            else:
                user.update_in_db(req_json)
                return user.to_json()
        except:
            return {'msg' : 'Couldn\'t add or update user in the server db'}, 500


    def delete(self):
        try:
            user_email = validateJWT(request)
        except Exception as e:
            return {'msg': str(e)}, 401
        
        try:
            appointments = AppointmentModel.query.filter_by(client_id = user_email).all()
            for appointment in appointments:
                appointment.delete_from_db()
            user = UserModel.query.filter_by(id = user_email).first()
            user.delete_from_db()
            return {'msg' : 'User {} has been succesfully deleted'.format(user_email)}, 200
        except:
            return {'msg' : 'Couldn\'t add or update user in the server db'}, 500
            


class AppointmentData(Resource):
    def get(self):
        try:
            user_email = validateJWT(request)
        except Exception as e:
            return {'msg': str(e)}, 401

        appointments_json = []

        appointments = AppointmentModel.query.filter_by(client_id = user_email).all()
        for appointment in appointments:
            appointment_json = {}
            appointment_json['id'] = appointment.id
            appointment_json['date'] = appointment.date
            appointment_json['time'] = appointment.time

            barber = BarberModel.query.filter_by(id = appointment.barber_id).first()
            appointment_json['barber_name'] = barber.name

            bbs = BarbershopModel.query.filter_by(id = barber.bbs_id).first()
            appointment_json['bbs_name'] = bbs.name
            appointment_json['address'] = bbs.address
            appointment_json['lat'] = bbs.coordX
            appointment_json['long'] = bbs.coordY

            service = ServiceModel.query.filter_by(id = appointment.service_id).first()
            appointment_json['service'] = service.name

            appointments_json.append(appointment_json)

        return appointments_json

    def post(self):
        try:
            user_email = validateJWT(request)
        except Exception as e:
            return {'msg': str(e)}, 401

        req_json = request.get_json()
        barber_id = req_json['barber_id']
        date = req_json['date']
        time = req_json['time']

        req_json['email'] = user_email

        check_appointment = AppointmentModel.query.filter_by(barber_id = barber_id, date = date, time = time).first()
        if check_appointment is not None:
            return {'msg' : 'There already is an appointment at this barber at the specified date and time.', 'code' : 0}

        check_appointment = AppointmentModel.query.filter_by(client_id = user_email, date = date, time = time).first()
        if check_appointment is not None:
            return {'msg' : 'You already have an appointment at the specified date and time.', 'code' : 0}

        new_appointment = AppointmentModel(req_json)
        new_appointment.save_to_db()
        return {'msg' : 'Your appointment has been created!', 'code' : 1}
    
    def delete(self):
        try:
            user_email = validateJWT(request)
        except Exception as e:
            return {'msg': str(e)}, 401

        req_json = request.get_json()
        appointment_id = req_json['appointment_id']

        appointment = AppointmentModel.query.filter_by(id = appointment_id).first()
        if appointment is None:
            return {'msg' : 'This appointment doesn\'t exist', 'code' : 0}
        else:
            # check if it is the users appointment
            if appointment.client_id != user_email:
                return {'msg' : 'You can only delete your own appointments', 'code' : 0}
            
            appointment.delete_from_db()
            return {'msg' : 'Appointment succesfully deleted', 'code' : 1}

class BarbershopData(Resource):
    def post(self):
        req_json = request.get_json()
        
        coordX = req_json['coordX']
        coordY = req_json['coordY']
        criteria = req_json['criteria']

        if criteria == 'name':
            search = '%{}%'.format(req_json['name'])
            barbershops = BarbershopModel.query.filter(BarbershopModel.name.ilike(search)).all()
        else:
            barbershops = BarbershopModel.query.all()

        barbershops_json = []
        for barbershop in barbershops:
            final_json = {}
            final_json["id"] = barbershop.id
            final_json["name"] = barbershop.name
            final_json["rating"] = barbershop.rating
            distance = geopy.distance.geodesic((coordX, coordY), (barbershop.coordX, barbershop.coordY)).km
            final_json['distance'] = distance
            barbershops_json.append(final_json)

        if criteria == 'distance':
            def distanceFunc(bbs):
                return bbs['distance']
            barbershops_json.sort(key=distanceFunc)

        elif criteria == 'rating':
            def ratingFunc(bbs):
                return bbs['rating']
            barbershops_json.sort(key=ratingFunc, reverse=True)

        return barbershops_json


class BarberServiceData(Resource):
    def post(self):
        barbershop_id = request.get_json()['bbs_id']
        services_json = []
        barbers_json = []

        barbers = BarberModel.query.filter_by(bbs_id = barbershop_id).all()
        for barber in barbers:
            barbers_json.append(barber.to_json())

        services = ServiceModel.query.filter_by(bbs_id = barbershop_id).all()
        for service in services:
            services_json.append(service.to_json())

        return {'barbers' : barbers_json, 'services' : services_json}

class TimeData(Resource):
    def post(self):
        try:
            user_email = validateJWT(request)
        except Exception as e:
            return {'msg': str(e)}, 401

        req_json = request.get_json()
        barber_id = req_json['barber_id']
        date = req_json['date']

        possible_times = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
                          '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
                          '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30']

        # remove the timeslots for which the barber isn't free
        appointments_that_day = AppointmentModel.query.filter_by(barber_id = barber_id, date = date).all()
        for appointment in appointments_that_day:
            possible_times.remove(appointment.time)

        # remove the timeslots for which the user has already made an appointment
        appointments_that_day = AppointmentModel.query.filter_by(client_id = user_email, date = date).all()
        for appointment in appointments_that_day:
            if (appointment.time in possible_times):
                possible_times.remove(appointment.time)

        return possible_times