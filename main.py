from flask import Flask, jsonify, request, abort
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from config import config
import requests

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config['SECURITY']['JWT_SECRET_KEY']
jwt = JWTManager(app)

# Microservices endpoints
AUTH_API_URL = 'http://localhost:5002/auth_api/login'
CUSTOMER_API_URL = 'http://localhost:5001/customer_api/customers'


@app.route('/login', methods=['POST'])
def login():

    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            abort(400)

        response = requests.post(f'{AUTH_API_URL}', json={'username': username, 'password': password})

        if response.status_code == 200:
            access_token = create_access_token(identity=username)
            return jsonify({'access_token': access_token})
        else:
            abort(401)
    except:
        return jsonify({'message': 'Invalid username/password'}), 400


@app.route('/customers/<path:path>', methods=['GET'])
@app.route('/customers', methods=['GET'])
def customers_get_gateway(path=''):
    url = f"{CUSTOMER_API_URL}/{path}"
    print(url)
    response = requests.get(url, headers=request.headers)
    return response.content, response.status_code


@app.route('/customers/<path:path>', methods=['POST'])
def customers_post_gateway(path=''):
    url = f"{CUSTOMER_API_URL}/{path}"
    print(url)
    response = requests.post(url, headers=request.headers)
    return response.content, response.status_code


if __name__ == '__main__':
    app.run(port=5000, debug=True)

