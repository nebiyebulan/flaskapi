from flask import request, jsonify
from entities import Logintypes, logintype_schema, token_required
from DatabaseConnect import app, db

# for logintypes
class logintypeclass:
    @app.route('/Logintypes/Register', methods=['POST'])
    @token_required
    def add_logintype(current_logintypes):
        typename = request.json['typename']
        isactive = request.json['isactive']
        createddate = request.json['createddate']
        modifieddate = request.json['modifieddate']
        isdeleted = request.json['isdeleted']

        new_logintype = Logintypes(typename, isactive, createddate, modifieddate, isdeleted)

        db.session.add(new_logintype)
        db.session.commit()
        return logintype_schema.jsonify(new_logintype)


    # get all logintype
    @app.route('/Logintypes/GetAll', methods=['GET'])
    @token_required
    def logintypes(current_logintypes):
        logintypes = Logintypes.query.all()
        output = []
        for logintype in logintypes:
            if not logintype.isdeleted:
                output.append({
                    'id': logintype.id,
                    'typename': logintype.typename,
                    'isactive': logintype.isactive,
                    'isdeleted': logintype.isdeleted,
                    'createddate': logintype.createddate,
                    'modifieddate': logintype.modifieddate,
                })

        return jsonify({'logintypes': output})

    @app.route('/Logintypes/Get', methods=['GET'])
    @token_required
    def get_logintypes(current_logintypes):
        if 'id' in request.headers:
            id = request.headers['id']
            logintypes = Logintypes.query.get(id)
            if logintypes != None:
                if not logintypes.isdeleted:
                    return logintype_schema.jsonify(logintypes)
                else:
                    return jsonify({
                        'message': 'User not found !!'
                    }), 200
            else:
                return jsonify({
                    'message': 'There is no such login type !!'
                }), 200

    @app.route('/Logintypes/Update', methods=['PUT'])
    @token_required
    def update_logintype(current_logintypes):
        if 'id' in request.headers:
            id = request.headers['id']
            log = Logintypes.query.get(id)
            if log != None:
                typename = request.json['typename']
                isactive = request.json['isactive']
                createddate = request.json['createddate']
                modifieddate = request.json['modifieddate']
                isdeleted = request.json['isdeleted']

                log.typename = typename
                log.isactive = isactive
                log.createddate = createddate
                log.modifieddate = modifieddate
                log.isdeleted = isdeleted

                db.session.commit()
                return logintype_schema.jsonify(log)
            else:
                return jsonify({
                    'message': 'There is no such login type !!'
                }), 200

    # delete logintype
    @app.route('/Logintypes/Delete', methods=['POST'])
    @token_required
    def delete_logintype(current_logintypes):
        if 'id' in request.headers:
            id = request.headers['id']
            logintype = Logintypes.query.get(id)
            if logintype != None:
                logintype.isdeleted = True
                db.session.commit()
                return logintype_schema.jsonify(logintype)
            else:
                return jsonify({
                    'message': 'There is no such login type !!'
                }), 200

if __name__ == '__main__':
    app.run(debug=True)
