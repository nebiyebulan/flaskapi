from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from entities import Users, user_schema, token_required
from DatabaseConnect import db, app
import jwt

from UserRole import roleclass
from LoginTypes import logintypeclass
from Vehicle import vehicleclass
from VehicleLogins import vehicleloginclass
from VehicleTypes import vehicletypeclass


@app.route('/User/Register', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.json

    # gets name, email and password
    username, email, phonenumber, createddate, modifieddate, isdeleted, isactive, userroleid = data.get(
            'username'), data.get('email'), data.get('phonenumber'), data.get('createddate'), data.get(
            'modifieddate'), data.get('isactive'), data.get('isdeleted'), data.get('userroleid')
    password = data.get('password')

    # checking for existing user
    user = Users.query \
        .filter_by(email=email) \
        .first()
    if not user:
        # database ORM object
        user = Users(
            username=username,
            email=email,
            password=generate_password_hash(password),
            phonenumber=phonenumber,
            createddate=createddate,
            modifieddate=modifieddate,
            isactive=isactive,
            isdeleted=isdeleted,
            userroleid=userroleid,
            )
        # insert user
        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered.', 200)
    else:
        # returns 202 if user already exists
        return make_response('User already exists.', 202)

# get all users
@app.route('/User/GetAll', methods=['GET'])
@token_required
def get_users(current_user):
    all_users = Users.query.all()
    output = []
    for user in all_users:
        if not user.isdeleted:
            output.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'password': user.password,
                'phonenumber': user.phonenumber,
                'isactive': user.isactive,
                'isdeleted': user.isdeleted,
                'created': user.createddate,
                'modifieddate': user.modifieddate,
                'userroleid': user.userroleid
            })

    return jsonify(output)


# get single users
@app.route('/User/Get', methods=['GET'])
@token_required
def get_user(current_user):
    if 'id' in request.headers:
        id = request.headers['id']
        print(type(id))
        user = Users.query.get(id)
        if user != None:
            if not user.isdeleted:
                return user_schema.jsonify(user)
            else:
                return jsonify({
                    'message': 'User not found !!'
                }), 200
        else:
            return jsonify({
                'message': 'There is no such user !!'
            }), 200
# update users
@app.route('/User/Update', methods=['PUT'])
@token_required
def update_users(current_user):
    if 'id' in request.headers:
        id = request.headers['id']
        user = Users.query.get(id)
        if user != None:
            email = request.json['email']
            password = request.json['password']
            username = request.json['username']
            phonenumber = request.json['phonenumber']
            isactive = request.json['isactive']
            createddate = request.json['createddate']
            modifieddate = request.json['modifieddate']
            isdeleted = request.json['isdeleted']
            userroleid = request.json['userroleid']

            user.email = email
            user.password = password
            user.username = username
            user.phonenumber = phonenumber
            user.isactive = isactive
            user.createddate = createddate
            user.modifieddate = modifieddate
            user.isdeleted = isdeleted
            user.userroleid = userroleid

            db.session.commit()
            return user_schema.jsonify(user)
        else:
            return jsonify({
                'message': 'There is no such user !!'
            }), 200

# delete users
@app.route('/User/Delete', methods=['POST'])
@token_required
def delete_users(current_user):
    if 'id' in request.headers:
        id = request.headers['id']
        user = Users.query.get(id)
        if user != None:
            user.isdeleted = True
            db.session.commit()
            return user_schema.jsonify(user)
        else:
            return jsonify({
                'message': 'There is no such user !!'
            }), 200
@app.route('/Values/GetToken', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.json
    if not auth or not auth.get('email') or not auth.get('password') or not auth.get('userroleid'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = Users.query \
        .filter_by(email=auth.get('email')) \
        .first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'id': user.id,
            'email': user.email,
            'userroleid': user.userroleid

        }, app.config['SECRET_KEY'])

        for i in token.decode():
            if user.userroleid >= 3:
                return make_response('Authorization Failed!', 401,
                                     {'WWW-Authenticate': 'Basic realm ="Authorization Failed!!!"'})

        return make_response(jsonify({'data': {"value": token.decode('UTF-8')}}), 200)

    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )

if __name__ == '__main__':
    app.run(debug=True)
