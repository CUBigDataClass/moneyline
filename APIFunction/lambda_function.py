import json
import boto3
import base64

TABLE_NAME = 'nba_prediction'
dynamo_conn = boto3.resource('dynamodb')
table = dynamo_conn.Table(TABLE_NAME)

def lambda_handler(event, context):
    print(event)
    body = event['body']
    if event['isBase64Encoded']:
        body = base64.b64decode(body).decode('utf-8')
    payload = json.loads(body)  # For API Gateway
    # payload = event

    response = []

    for input in payload:
        print(input)
        home_team = input['home_team']
        away_team = input['away_team']
        try:
            x = table.get_item(Key={'HOME_TEAM': home_team})
            print(x)
            if 'Item' not in x:
                pred = 0
            else:
                pred = x['Item'].get(away_team, 0)
            data = {
                'home_team': home_team,
                'away_team': away_team,
                'prediction': float(pred)
            }
            print(data)
            response.append(data)

        except Exception as e:
            print(e)

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(response)
    }
