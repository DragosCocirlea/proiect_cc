from flask import request, Response
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import models
import requests

class UserRegistration(Resource):
    def post(self):
        req_json = request.get_json()
        user_email = req_json['email']
        user_pass = req_json['password']

        if models.UserModel.find_by_email(user_email):
          return {'msg': 'User {} already exists'. format(user_email)}, 401

        new_user = models.UserModel(
            email = user_email,
            password = models.UserModel.generate_hash(user_pass)
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = user_email)
            refresh_token = create_refresh_token(identity = user_email)

            # add the user to the server db
            requests.post('http://server:5000/user', json = req_json)

            return {
                'msg': 'User {} was created'.format(user_email),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except Exception as e:
            return {'msg': 'Something went wrong : {}'.format(e)}, 500


class UserLogin(Resource):
    def post(self):
        user_email = request.get_json()['email']
        user_pass = request.get_json()['password']

        current_user = models.UserModel.find_by_email(user_email)
        
        if not current_user:
            return {'msg': 'User {} doesn\'t exist'.format(user_email)}, 401
        
        if models.UserModel.verify_hash(user_pass, current_user.password):
            access_token = create_access_token(identity = user_email)
            refresh_token = create_refresh_token(identity = user_email)
            return {
                'msg': 'Logged in as {}'.format(user_email),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'msg': 'Wrong credentials'}, 401
      
      
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = models.RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'msg': 'Access token has been revoked'}
        except:
            return {'msg': 'Something went wrong'}, 500
      
      
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = models.RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'msg': 'Refresh token has been revoked'}
        except:
            return {'msg': 'Something went wrong'}, 500
      
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}

class GetIdentity(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        return {'user_email': current_user}

# class FigaroCall(Resource):
#     @jwt_required
#     def post(self, action):
#         req_json = request.get_json()
#         req_json['email'] = get_jwt_identity()
#         resp = requests.post('http://server:5000/{}'.format(action), json = req_json)
#         excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
#         headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
#         resp = Response(resp.content, resp.status_code, headers)
#         return resp


#     @jwt_required
#     def get(self, action):
#         try:
#             req_json = request.get_json()
#         except:
#             req_json = {}

#         req_json['email'] = get_jwt_identity()
#         resp = requests.get('http://server:5000/{}'.format(action), json = req_json)
#         excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
#         headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
#         resp = Response(resp.content, resp.status_code, headers)
#         return resp


#     @jwt_required
#     def delete(self, action):
#         try:
#             req_json = request.get_json()
#         except:
#             req_json = {}

#         req_json['email'] = get_jwt_identity()
#         resp = requests.delete('http://server:5000/{}'.format(action), json = req_json)

#         if action == 'user':
#             user_email = get_jwt_identity()
#             user = models.UserModel.query.filter_by(email = user_email).first()
#             user.delete_from_db()

#         excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
#         headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
#         resp = Response(resp.content, resp.status_code, headers)
#         return resp
