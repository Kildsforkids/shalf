from os import path
from flask import Flask, render_template, jsonify, request
import json

import app
from iacp import IACP

template_dir = path.join(path.dirname(path.abspath(__file__)), '..', 'client', 'build')
# template_dir = 'template'
static_dir = path.join(template_dir, 'static')

server = Flask(__name__, static_folder=static_dir, template_folder=template_dir)


@server.route('/')
def index():
    return render_template('index.html')


@server.route('/parameters', methods=['GET'])
def parameters():
    result = app.parameters()

    if result:
        response = {'status': 'ok', 'result': result}
    else:
        response = {'status': 'error'}

    return jsonify(response)


@server.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        x = json.loads(request.data)['query']
        result = app.get_model_value(x)

        if result:
            response = {'status': 'ok', 'result': result}
        else:
            response = {'status': 'error'}
        
        return jsonify(response)
    return 'Not a valid request'


@server.route('/iacp/predict', methods=['POST'])
def iacp_predict():
    if request.method == 'POST':
        x = json.loads(request.data)['query']
        x = app.convert_to_iacp(x)
        iacp = IACP(x)
        result = iacp.run()

        if result:
            response = {'status': 'ok', 'result': result}
        else:
            response = {'status': 'error'}
        
        return jsonify(response)
    return 'Not a valid request'