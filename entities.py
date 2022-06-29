from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime
import jwt
from functools import wraps
from DatabaseConnect import db, app ,ma


class MyDateTime(db.TypeDecorator):
    impl = db.DateTime

    def process_bind_param(self, value, dialect):
        if type(value) is str:
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        return value


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    phonenumber = db.Column(db.String(50))
    isactive = db.Column(db.Boolean(), nullable=False)
    createddate = db.Column(MyDateTime, default=datetime.now(), nullable=False)
    modifieddate = db.Column(MyDateTime, default=datetime.now(), nullable=False)
    isdeleted = db.Column(db.Boolean())
    userroleid = db.Column(db.Integer, db.ForeignKey('userroles.id'), nullable=False)
    vehicles = db.relationship('Vehicles', backref='users')

    def __init__(self, email, password, username, phonenumber, isactive, createddate, modifieddate, isdeleted,
                 userroleid):
        self.email = email
        self.password = password
        self.username = username
        self.phonenumber = phonenumber
        self.isactive = isactive
        self.createddate = createddate
        self.modifieddate = modifieddate
        self.isdeleted = isdeleted
        self.userroleid = userroleid


# create user_role
class Userroles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(50), nullable=False)
    isactive = db.Column(db.Boolean(), nullable=False)
    createddate = db.Column(MyDateTime, default=datetime.now(), nullable=False)
    modifieddate = db.Column(MyDateTime, default=datetime.now(), nullable=False)
    isdeleted = db.Column(db.Boolean(), nullable=False)
    role = db.relationship('Users', backref='userroles', uselist=False)

    def __init__(self, rolename, isactive, createddate, modifieddate, isdeleted):
        self.rolename = rolename
        self.isactive = isactive
        self.createddate = createddate
        self.modifieddate = modifieddate
        self.isdeleted = isdeleted


class RoleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'rolename', 'isactive', 'createddate', 'modifieddate', 'isdeleted')


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'email', 'password', 'username', 'phonenumber', 'isactive', 'createddate', 'modifieddate',
            'isdeleted',
            'userroleid', 'userroles.rolename')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# create vehicles
class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    licenceplate = db.Column(db.String(9), unique=True, nullable=False)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer())
    isguest = db.Column(db.Boolean(), nullable=False)
    isactive = db.Column(db.Boolean(), nullable=False)
    createddate = db.Column(MyDateTime, default=datetime.now(), nullable=False)
    modifieddate = db.Column(MyDateTime, default=datetime.now(), nullable=False)
    isdeleted = db.Column(db.Boolean(), nullable=False)
    vehicletypeid = db.Column(db.Integer, db.ForeignKey('vehicletypes.id'), nullable=False)
    logins = db.relationship('Vehiclelogins', backref='vehicles')
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, licenceplate, brand, model, year, isguest, isactive, createddate, modifieddate, isdeleted,
                 vehicletypeid, userid):
        self.licenceplate = licenceplate
        self.brand = brand
        self.model = model
        self.year = year
        self.isguest = isguest
        self.isactive = isactive
        self.createddate = createddate
        self.modifieddate = modifieddate
        self.isdeleted = isdeleted
        self.vehicletypeid = vehicletypeid
        self.userid = userid


class VehicleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'licenceplate', 'brand', 'model', 'year', 'isguest', 'isactive', 'createddate', 'modifieddate',
                  'isdeleted', 'vehicletypeid', 'userid', 'users.username', 'users.phonenumber',
                  'vehicletypes.typename')


vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)


class Vehicletypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(50), nullable=False)
    isactive = db.Column(db.Boolean(), nullable=False)
    createddate = db.Column(MyDateTime, default=datetime.now(), nullable=False)
    modifieddate = db.Column(MyDateTime, default=datetime.now(), nullable=False)
    isdeleted = db.Column(db.Boolean(), nullable=False)
    vehicle = db.relationship('Vehicles', backref='vehicletypes', uselist=False)

    def __init__(self, typename, isactive, createddate, modifieddate, isdeleted):
        self.typename = typename
        self.isactive = isactive
        self.createddate = createddate
        self.modifieddate = modifieddate
        self.isdeleted = isdeleted


class VehicletypeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'typename', 'isactive', 'createddate', 'modifieddate', 'isdeleted')


vehicletype_schema = VehicletypeSchema()
vehicletypes_schema = VehicletypeSchema(many=True)


class Vehiclelogins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    processdate = db.Column(MyDateTime, default=datetime.now(), nullable=False)
    isactive = db.Column(db.Boolean(), nullable=False)
    createddate = db.Column(MyDateTime, default=datetime.now(), nullable=False)
    modifieddate = db.Column(MyDateTime, default=datetime.now(), nullable=False)
    isdeleted = db.Column(db.Boolean(), nullable=False)
    vehicleid = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    logintypeid = db.Column(db.Integer, db.ForeignKey('logintypes.id'), nullable=False)

    def __init__(self, processdate, isactive, createddate, modifieddate, isdeleted, vehicleid, logintypeid):
        self.processdate = processdate
        self.isactive = isactive
        self.createddate = createddate
        self.modifieddate = modifieddate
        self.isdeleted = isdeleted
        self.vehicleid = vehicleid
        self.logintypeid = logintypeid


class LoginSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'processdate', 'isactive', 'createddate', 'modifieddate', 'isdeleted', 'vehicleid', 'logintypeid',
            'vehicles.licenceplate', 'vehicles.isguest', 'vehicles.brand', 'vehicles.model', 'vehicles.year')


login_schema = LoginSchema()
logins_schema = LoginSchema(many=True)


class Logintypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(50), nullable=False)
    isactive = db.Column(db.Boolean(), nullable=False)
    createddate = db.Column(MyDateTime, default=datetime.now(), nullable=False)
    modifieddate = db.Column(MyDateTime, default=datetime.now(), nullable=False)
    isdeleted = db.Column(db.Boolean(), nullable=False)
    logintyp = db.relationship('Vehiclelogins', backref='logintypes')

    def __init__(self, typename, isactive, createddate, modifieddate, isdeleted):
        self.typename = typename
        self.isactive = isactive
        self.createddate = createddate
        self.modifieddate = modifieddate
        self.isdeleted = isdeleted


class LogintypeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'typename', 'isactive', 'createddate', 'modifieddate', 'isdeleted')


logintype_schema = LogintypeSchema()
logintypes_schema = LogintypeSchema(many=True)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_vehicle = Vehicles.query \
                .filter_by(id=data['id']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(current_vehicle)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            for i in data:
                if i==userroleid and i>=3:

                    current_user = Users.query \
                        .filter_by(id=data['id']) \
                        .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(current_user)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_role = Userroles.query \
                .filter_by(id=data['id']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(current_role)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_vehicletype = Vehicletypes.query \
                .filter_by(id=data['id']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(current_vehicletype)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_login = Vehiclelogins.query \
                .filter_by(id=data['id']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(current_login)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_logintypes = Logintypes.query \
                .filter_by(id=data['id']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(current_logintypes)

    return decorated


if __name__ == '__main__':
    app.run(debug=True)
