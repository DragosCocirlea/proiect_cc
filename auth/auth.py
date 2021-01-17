from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from models import UserModel, RevokedTokenModel, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@dbauth:3306/figaro_auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['PROPAGATE_EXCEPTIONS'] = True
app.app_context().push()

api = Api(app)
jwt = JWTManager(app)

# create the database and the needed tables if they don't already exist
from sqlalchemy import create_engine
engine = create_engine('mysql://root:root@dbauth:3306/')
engine.execute("CREATE DATABASE IF NOT EXISTS figaro_auth;")
db.app = app
db.init_app(app)
db.create_all()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

import resources
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.GetIdentity, '/token/decode')
# api.add_resource(resources.FigaroCall, '/figaro/<string:action>')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
