from flask import request, jsonify
from entities import Vehicletypes, vehicletype_schema, token_required
from DatabaseConnect import app, db

# for vehicletypes
class vehicletypeclass:
    @app.route('/Vehicletypes/Register', methods=['POST'])
    @token_required
    def add_vehicletypes(current_vehicletype):
        typename = request.json['typename']
        isactive = request.json['isactive']
        createddate = request.json['createddate']
        modifieddate = request.json['modifieddate']
        isdeleted = request.json['isdeleted']

        new_vehicletype = Vehicletypes(typename, isactive, createddate, modifieddate, isdeleted)

        db.session.add(new_vehicletype)
        db.session.commit()
        return vehicletype_schema.jsonify(new_vehicletype)


    # get all vehicletypes
    @app.route('/Vehicletypes/GetAll', methods=['GET'])
    @token_required
    def get_all_vehicletypes(current_vehicletype):
        vehicletype = Vehicletypes.query.all()
        output = []
        for type in vehicletype:
            if not type.isdeleted:
                output.append({
                    'id': type.id,
                    'typename': type.typename,
                    'isactive': type.isactive,
                    'isdeleted': type.isdeleted,
                    'createddate': type.createddate,
                    'modifieddate': type.modifieddate,
                })

        return jsonify({'vehicles': output})

    # get single vehicletypes
    @app.route('/Vehicletypes/Get', methods=['GET'])
    @token_required
    def get_vehicletype(current_vehicletype):
        if 'id' in request.headers:
            id = request.headers['id']
            vehicletype = Vehicletypes.query.get(id)
            if vehicletype != None:
                if not vehicletype.isdeleted:
                    return vehicletype_schema.jsonify(vehicletype)
                else:
                    return jsonify({
                        'message': 'User not found !!'
                    }), 200
            else:
                return jsonify({
                    'message': 'There is no such vehicle type !!'
                }), 200

    # update vehicletypes
    @app.route('/Vehicletypes/Update', methods=['PUT'])
    @token_required
    def update_vehicletype(current_vehicletype):
        if 'id' in request.headers:
            id = request.headers['id']
            vehic = Vehicletypes.query.get(id)
            if vehic != None:
                typename = request.json['typename']
                isactive = request.json['isactive']
                createddate = request.json['createddate']
                modifieddate = request.json['modifieddate']
                isdeleted = request.json['isdeleted']

                vehic.typename = typename
                vehic.isactive = isactive
                vehic.createddate = createddate
                vehic.modifieddate = modifieddate
                vehic.isdeleted = isdeleted

                db.session.commit()
                return vehicletype_schema.jsonify(vehic)
            else:
                return jsonify({
                    'message': 'There is no such vehicle type !!'
                }), 200

    # delete vehicletype
    @app.route('/Vehicletypes/Delete', methods=['POST'])
    @token_required
    def delete_vehicletype(current_vehicletype):
        if 'id' in request.headers:
            id = request.headers['id']
            vehicle = Vehicletypes.query.get(id)
            if vehicle != None:
                vehicle.isdeleted = True
                db.session.commit()
                return vehicletype_schema.jsonify(vehicle)
            else:
                return jsonify({
                    'message': 'There is no such vehicle type !!'
                }), 200
if __name__ == '__main__':
    app.run(debug=True)
