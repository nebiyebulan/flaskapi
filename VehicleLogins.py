from flask import request, jsonify
from entities import Vehiclelogins, login_schema, token_required
from DatabaseConnect import app, db

# for vehiclelogins
class vehicleloginclass:
    @app.route('/Vehiclelogins/Register', methods=['POST'])
    @token_required
    def add_vehiclelogins(current_login):
        processdate = request.json['processdate']
        isactive = request.json['isactive']
        createddate = request.json['createddate']
        modifieddate = request.json['modifieddate']
        isdeleted = request.json['isdeleted']
        vehicleid = request.json['vehicleid']
        logintypeid = request.json['logintypeid']

        new_login = Vehiclelogins(processdate, isactive, createddate, modifieddate, isdeleted, vehicleid, logintypeid)

        db.session.add(new_login)
        db.session.commit()
        return login_schema.jsonify(new_login)


    @app.route('/Vehiclelogins/GetAll', methods=['GET'])
    @token_required
    def get_all_logins(current_login):
        logins = Vehiclelogins.query.all()
        output = []
        for login in logins:
            if not login.isdeleted:
                output.append({
                    'id': login.id,
                    'isactive': login.isactive,
                    'isdeleted': login.isdeleted,
                    'createddate': login.createddate,
                    'modifieddate': login.modifieddate,
                    'processdate': login.processdate,
                    'vehicleid': login.vehicleid,
                    'logintypeid': login.logintypeid
                })

        return jsonify({'logins': output})

    # get single vehiclelogins
    @app.route('/Vehiclelogins/Get', methods=['GET'])
    @token_required
    def get_login(current_login):
        if 'id' in request.headers:
            id = request.headers['id']
            vehiclelogin = Vehiclelogins.query.get(id)
            if vehiclelogin != None:
                if not vehiclelogin.isdeleted:
                    return login_schema.jsonify(vehiclelogin)
                else:
                    return jsonify({
                        'message': 'User not found !!'
                    }), 200
            else:
                return jsonify({
                    'message': 'There is no such vehicle login !!'
                }), 200


    # update vehiclelogins
    @app.route('/Vehiclelogins/Update', methods=['PUT'])
    @token_required
    def update_login(current_login):
        if 'id' in request.headers:
            id = request.headers['id']
            vehiclelogin = Vehiclelogins.query.get(id)
            if vehiclelogin != None:
                processdate = request.json['processdate']
                isactive = request.json['isactive']
                createddate = request.json['createddate']
                modifieddate = request.json['modifieddate']
                isdeleted = request.json['isdeleted']
                vehicleid = request.json['vehicleid']
                logintypeid = request.json['logintypeid']

                vehiclelogin.processdate = processdate
                vehiclelogin.isactive = isactive
                vehiclelogin.createddate = createddate
                vehiclelogin.modifieddate = modifieddate
                vehiclelogin.isdeleted = isdeleted
                vehiclelogin.vehicleid = vehicleid
                vehiclelogin.logintypeid = logintypeid

                db.session.commit()
                return login_schema.jsonify(vehiclelogin)
            else:
                return jsonify({
                    'message': 'There is no such vehicle login !!'
                }), 200

    # delete vehiclelogins
    @app.route('/Vehiclelogins/Delete', methods=['POST'])
    @token_required
    def delete_login(current_login):
        if 'id' in request.headers:
            id = request.headers['id']
            vehiclelogin = Vehiclelogins.query.get(id)
            if vehiclelogin != None:
                vehiclelogin.isdeleted = True
                db.session.commit()
                return login_schema.jsonify(vehiclelogin)
            else:
                return jsonify({
                    'message': 'There is no such vehicle login !!'
                }), 200

if __name__ == '__main__':
    app.run(debug=True)
