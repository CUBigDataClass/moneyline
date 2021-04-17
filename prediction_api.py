from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import ast
#import aws_controller
from prediction import query_games

app = Flask(__name__)
api = Api(app)

class Predictions(Resource):    
    #@app.route('/get')
    def get(self, year):
        data = query_games(year).to_json()     
        return data

# @app.route('/')
# def display():
#     return "this is working"

api.add_resource(Predictions, '/get/<year>')

if __name__ == '__main__':
    app.run(debug=True, port=4822)