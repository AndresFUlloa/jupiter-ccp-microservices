from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_gateway(path):
    # Get the target URL from the request headers
    target_url = request.headers.get('Target-URL')

    if not target_url:
        return jsonify({'error': 'Target URL not specified'}), 400

    # Forward the request to the target URL
    target_path = f'{target_url}/{path}'
    target_method = request.method
    target_data = request.get_data()
    target_headers = dict(request.headers)

    response = requests.request(target_method, target_path, data=target_data, headers=target_headers)

    # Return the response from the target server to the client
    headers = dict(response.headers)
    headers['Access-Control-Allow-Origin'] = '*'

    return response.content, response.status_code, headers

