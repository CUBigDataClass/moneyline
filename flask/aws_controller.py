import boto3

TABLE_NAME = 'nba_predictions'

#dynamo_client = boto3.client('dynamodb')
dynamo_conn = boto3.resource('dynamodb', region_name='us-west-2', aws_access_key_id='', aws_secret_access_key='')
table = dynamo_conn.Table(TABLE_NAME)

def get_items():
    return table.scan()