from flask import request, jsonify
from entities import Userroles, role_schema, token_required
from DatabaseConnect import app, db

class roleclass:
    @app.route('/UserRole/Register', methods=['POST'])
    @token_required
    def add_role(current_role):
        rolename = request.json['rolename']
        isactive = request.json['isactive']
        createddate = request.json['createddate']
        modifieddate = request.json['modifieddate']
        isdeleted = request.json['isdeleted']

        new_role = Userroles(rolename, isactive, createddate, modifieddate, isdeleted)

        db.session.add(new_role)
        db.session.commit()
        return role_schema.jsonify(new_role)


    # get all role
    @app.route('/UserRoles/GetAll', methods=['GET'])
    @token_required
    def get_roles(current_role):
        all_role = Userroles.query.all()
        output = []
        for role in all_role:
            if not role.isdeleted:
                output.append({
                    'id': role.id,
                    'rolename': role.rolename,
                    'isactive': role.isactive,
                    'isdeleted': role.isdeleted,
                    'created': role.createddate,
                    'modifieddate': role.modifieddate,
                })
        return jsonify(output)

    # get single role
    @app.route('/UserRole/Get', methods=['GET'])
    @token_required
    def get_role(current_role):
        if 'id' in request.headers:
            id = request.headers['id']
            role = Userroles.query.get(id)
            if role != None:
                if not role.isdeleted:
                    return role_schema.jsonify(role)
                else:
                    return jsonify({
                        'message': 'User not found !!'
                    }), 200
            else:
                return jsonify({
                    'message': 'There is no such role !!'
                }), 200

    # update role
    @app.route('/UserRole/Update', methods=['PUT'])
    @token_required
    def update_role(current_role):
        if 'id' in request.headers:
            id = request.headers['id']
            role = Userroles.query.get(id)
            if role != None:
                rolename = request.json['rolename']
                isactive = request.json['isactive']
                createddate = request.json['createddate']
                modifieddate = request.json['modifieddate']
                isdeleted = request.json['isdeleted']

                role.rolename = rolename
                role.isactive = isactive
                role.createddate = createddate
                role.modifieddate = modifieddate
                role.isdeleted = isdeleted

                db.session.commit()
                return role_schema.jsonify(role)
            else:
                return jsonify({
                    'message': 'There is no such role !!'
                }), 200

    # delete role
    @app.route('/UserRole/Delete', methods=['POST'])
    @token_required
    def delete_role(current_role):
        if 'id' in request.headers:
            id = request.headers['id']
            role = Userroles.query.get(id)
            if role != None:
                role.isdeleted = True
                db.session.commit()
                return role_schema.jsonify(role)
            else:
                return jsonify({
                    'message': 'There is no such role !!'
                }), 200

if __name__ == '__main__':
    app.run(debug=True)
