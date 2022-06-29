from flask import request, jsonify
from entities import Vehicles, vehicle_schema, token_required
from DatabaseConnect import app, db

# for vehicle
class vehicleclass:
    @app.route('/Vehicle/Register', methods=['POST'])
    @token_required
    def add_vehicles(current_vehicle):
        licenceplate = request.json['licenceplate']
        brand = request.json['brand']
        model = request.json['model']
        year = request.json['year']
        isguest = request.json['isguest']
        isactive = request.json['isactive']
        createddate = request.json['createddate']
        modifieddate = request.json['modifieddate']
        isdeleted = request.json['isdeleted']
        vehicletypeid = request.json['vehicletypeid']
        userid = request.json['userid']

        new_vehicle = Vehicles(licenceplate, brand, model, year, isguest, isactive, createddate, modifieddate, isdeleted,
                               vehicletypeid, userid)

        db.session.add(new_vehicle)
        db.session.commit()
        return vehicle_schema.jsonify(new_vehicle)


    # get all vehicle
    @app.route('/Vehicles/GetAll', methods=['GET'])
    @token_required
    def get_all_vehicles(current_vehicle):
        vehicles = Vehicles.query.all()
        output = []
        for vehicle in vehicles:
            if not vehicle.isdeleted:
                output.append({
                    'id': vehicle.id,
                    'licenceplate': vehicle.licenceplate,
                    'brand': vehicle.brand,
                    'model': vehicle.model,
                    'year': vehicle.year,
                    'isguest': vehicle.isguest,
                    'isactive': vehicle.isactive,
                    'isdeleted': vehicle.isdeleted,
                    'createddate': vehicle.createddate,
                    'modifieddate': vehicle.modifieddate,
                    'vehicletypeid': vehicle.vehicletypeid,
                    'userid': vehicle.userid
                })

        return jsonify({'vehicles': output})

    # get single vehicle
    @app.route('/Vehicle/Get', methods=['GET'])
    @token_required
    def get_vehicle(current_vehicle):
        if 'id' in request.headers:
            id = request.headers['id']
            vehicles = Vehicles.query.get(id)
            if vehicles != None:
                if not vehicles.isdeleted:
                    return vehicle_schema.jsonify(vehicles)
                else:
                    return jsonify({
                        'message': 'User not found !!'
                    }), 200
            else:
                return jsonify({
                    'message': 'There is no such vehicle !!'
                }), 200


    # update vehicle
    @app.route('/Vehicle/Update', methods=['PUT'])
    @token_required
    def update_vehicle(current_vehicle):
        if 'id' in request.headers:
            id = request.headers['id']
            vehicle = Vehicles.query.get(id)
            if vehicle != None:
                licenceplate = request.json['licenceplate']
                brand = request.json['brand']
                model = request.json['model']
                year = request.json['year']
                isguest = request.json['isguest']
                isactive = request.json['isactive']
                createddate = request.json['createddate']
                modifieddate = request.json['modifieddate']
                isdeleted = request.json['isdeleted']
                vehicletypeid = request.json['vehicletypeid']
                userid = request.json['userid']

                vehicle.licenceplate = licenceplate
                vehicle.brand = brand
                vehicle.model = model
                vehicle.year = year
                vehicle.isguest = isguest
                vehicle.isactive = isactive
                vehicle.createddate = createddate
                vehicle.modifieddate = modifieddate
                vehicle.isdeleted = isdeleted
                vehicle.vehicletypeid = vehicletypeid
                vehicle.userid = userid

                db.session.commit()
                return vehicle_schema.jsonify(vehicle)
            else:
                return jsonify({
                    'message': 'There is no such vehicle !!'
                }), 200

    # delete vehicle
    @app.route('/Vehicle/Delete', methods=['POST'])
    @token_required
    def delete_vehicle(current_vehicle):
        if 'id' in request.headers:
            id = request.headers['id']
            vehicle = Vehicles.query.get(id)
            if vehicle != None:
                vehicle.isdeleted = True
                db.session.commit()
                return vehicle_schema.jsonify(vehicle)
            else:
                return jsonify({
                    'message': 'There is no such vehicle !!'
                }), 200

if __name__ == '__main__':
    app.run(debug=True)
