from flask import Flask, jsonify
from flask_restful import Resource, Api
import boto3
from boto3.dynamodb.conditions import Key

application = Flask(__name__)
api = Api(application)
TABLE_NAME = 'game_predictions'

class Predictions(Resource):
    def get(self, home_team, away_team):
        dynamo_conn = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id='AKIAU3SZVQWPSL73LGUJ', aws_secret_access_key='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')
        table = dynamo_conn.Table(TABLE_NAME)

        scan_kwargs = {
            'FilterExpression': Key('HOME_TEAM').eq(home_team) & Key('AWAY_TEAM').eq(away_team),
            'ProjectionExpression': "HOME_TEAM, AWAY_TEAM, WINNER, PROBABILITY",
            # 'ExpressionAttributeNames': {"#yr": "year"}
        }

        done = False
        start_key = None
        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = table.scan(**scan_kwargs)
            #display_movies(response.get('Items', []))
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

        preds = response['Items']
        
        return preds

api.add_resource(Predictions, '/get/<home_team>/<away_team>')

if __name__ == '__main__':
    application.run(debug=True)