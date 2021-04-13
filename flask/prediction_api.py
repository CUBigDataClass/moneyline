from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import ast
import aws_controller

app = Flask(__name__)
api = Api(app)

class Predictions(Resource):    
    @app.route('/get')
    def get():
        return jsonify(aws_controller.get_items())


api.add_resource(Predictions, '/predictions')

if __name__ == '__main__':
    app.run()