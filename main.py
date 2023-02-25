from flask import Flask, jsonify, request, abort
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from config import config
import requests

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config['SECURITY']['JWT_SECRET_KEY']
jwt = JWTManager(app)

# Microservices endpoints
AUTH_API_URL = 'http://localhost:5002/login_api/customers'
CUSTOMER_API_URL = 'http://localhost:5001/customer_api/customers'


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

