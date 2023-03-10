from flask import Flask, request, jsonify
import requests
import json


app = Flask(__name__)


# URL microservicio consulta principal
URL = "http://127.0.0.1:5001"

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_gateway(path):
    # Get the target URL from the request headers
    # target_url = request.headers.get('Target-URL')
    target_url = URL
    print(target_url)
    if not target_url:
        return jsonify({'error': 'Target URL not specified'}), 400

    # Forward the request to the target URL
    target_path = f'{target_url}/{path}'
    print(target_path)
    target_method = request.method
    print(target_method)
    target_data = dict(request.get_data())
    print(target_data)
    target_headers = dict(request.headers)
    print(target_headers)

    response = requests.request(target_method, target_path, data=target_data, headers=target_headers)
    print(response)
    # Return the response from the target server to the client
    headers = dict(response.headers)
    print(headers)
    headers['Access-Control-Allow-Origin'] = '*'

    return response.content, response.status_code, headers

# Cambio de URL segun el estado del microservicio
@app.route('/api/new_url', methods=['POST'])
def valid_URL():
    global URL
    data = request.get_data()
    data_str = data.decode('utf-8')
    data_dict = json.loads(data_str)
    URL = data_dict['new_url']
    print("El microservicio de consulta activo es el: " + URL)
    return "", 200

if __name__ == '__main__':
    app.run()

