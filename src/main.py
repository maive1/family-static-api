"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Family

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/member', methods=['GET', 'POST'])
def members():
    body = request.get_json()

    if request.method == 'GET':
        family = Family('Doe')
        members = family.get_all_members()
        lucky_numbers = [member['lucky_numbers'] for member in members]
        sum_of_lucky = sum([number for sub in lucky_numbers for number in sub])

        response_body = {
            "family_name": family.last_name,
            "members": family.get_all_members(),
            "lucky_numbers": lucky_numbers,
            "sum_of_lucky": str(sum_of_lucky)
        }

        return jsonify(response_body), 200
    
    if request.method == 'POST':
        if body is not None:
            family = Family('Doe')
            body = request.get_json()
            response_body = family.add_member(body)
            
            return jsonify(response_body),200
        else:
            raise APIException('You need to specify the request body as a json object', status_code=404)

@app.route('/member/<int:member_id>', methods=['GET', 'DELETE'] )
def single_member(member_id=None):

    body = request.get_json()

    if request.method == 'GET':
        family = Family('Doe')
        response_body = family.get_member(member_id)

        return jsonify(response_body), 200

    if request.method == 'DELETE':
        family = Family('Doe')
        family.delete_member(member_id)
        response_body = {"msg": "member was successfully deleted"}
        return jsonify(response_body), 200
    
    return "Invalid Method", 404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
