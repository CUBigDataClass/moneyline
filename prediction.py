'''
Some help from 
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.04.html
'''
#pylint: disable=E1101

import boto3
from boto3.dynamodb.conditions import Key
import pandas as pd

TABLE_NAME='nba'

def query_games(year):
    #DON'T COMMIT WITH AWS KEYS!!!!
    dynamo_conn = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id='AKIAU3SZVQWPVH3HSIEG', aws_secret_access_key='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')
    table = dynamo_conn.Table(TABLE_NAME)
    scan_kwargs = {
        'FilterExpression': Key('GAME_DATE').begins_with(year)
        # 'ProjectionExpression': "#yr, title, info.rating",
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

    return pd.DataFrame(response['Items'])

if __name__=='__main__':
    query_year = '2020'
    games = query_games(query_year)
    # for game in games:
    #     print(game['MATCHUP'])
    print(games)