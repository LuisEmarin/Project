from os import name
from flask import Blueprint,request,jsonify
from Jordans.helpers import token_required
from Jordans.models import  Jordan, db, jordan_schema, jordans_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 'Coding Temple'}

@api.route('/jordans', methods = ['POST'])
@token_required
def create_jordan(current_user_token):
    name = request.json['name']
    description = request.json['description']
    camera_quality = request.json['camera_quality']
    flight_time = request.json['flight_time']
    max_speed = request.json['max_speed']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    cost_of_prod = request.json['cost_of_prod']
    series = request.json['series']    
    token = current_user_token.token 

    print(f'TEST: {current_user_token.token}')

    jordan = Jordan(name,description,camera_quality,flight_time,max_speed,dimensions, weight,cost_of_prod,series, user_token = token)

    db.session.add(jordan)
    db.session.commit()

    response = jordan_schema.dump(jordan)
    return jsonify(response)

@api.route('/jordans', methods = ['GET'])
@token_required
def get_shoes(current_user_token):
    owner = current_user_token.token
    jordans = Jordan.query.filter_by(user_token = owner).all()
    response = jordans_schema.dump(jordans)
    return jsonify(response)

@api.route('/jordans/<id>', methods = ['GET'])
@token_required
def get_shoe(current_user_token, id):
    jordan = Jordan.query.get(id)
    response = jordans_schema.dump(jordan)
    return jsonify(response)


@api.route('/jordans/<id>', methods = ['POST', 'PUT'])
@token_required
def update_shoe(current_user_token, id):
    jordan = Jordan.query.get(id)
    print (jordan)
    if jordan:
        jordan.name = request.json['name']
        jordan.description = request.json['description']

        db.session.commit()

        response = jordan_schema.dump(jordan)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That Jordan does not exist!!!'})

@api.route('/jordans/<id>', methods = ['DELETE'])
@token_required
def delete_shoe(current_user_token, id):
    jordan = Jordan.querey.get(id)
    if jordan:
        db.session.delete(jordan)
        db.session.commit()

        return jsonify({'Success': f'shoe ID #{jordan.id} has been deleted)'})
    else:
        return jsonify({'Error': 'That shoe does not exist!'})




