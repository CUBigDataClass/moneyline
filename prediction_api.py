from flask import Flask, jsonify
from flask_restful import Resource, Api
import boto3

application = Flask(__name__)
api = Api(application)
TABLE_NAME = 'game_predictions'

class Predictions(Resource):
    def get(self):
        dynamo_conn = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id='AKIAU3SZVQWPSL73LGUJ', aws_secret_access_key='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')
        table = dynamo_conn.Table(TABLE_NAME)

        done = False
        start_key = None
        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = table.scan()
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

        preds = response['Items']
        
        return preds

api.add_resource(Predictions, '/get')

if __name__ == '__main__':
    application.run(debug=True)