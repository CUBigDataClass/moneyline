import json
import boto3
import uuid
from nba_api.stats.endpoints import leaguegamefinder
from datetime import timedelta,datetime


dynamo_conn = boto3.resource('dynamodb', region_name= 'us-east-2',aws_access_key_id='', aws_secret_access_key='')
# conn = boto3.resource('dynamodb', endpoint_url="http://host.docker.internal:8000/")
TABLE_NAME = 'nba'

def create_table():
    try:
        table_names = [table.name for table in dynamo_conn.tables.all()]
        if TABLE_NAME in table_names:
            table = dynamo_conn.Table(TABLE_NAME)
        else:
            table = dynamo_conn.create_table(
                    TableName=TABLE_NAME,
                    KeySchema=[

                        {'AttributeName': 'GAME_ID', 'KeyType': 'HASH'},
                        {'AttributeName': 'TEAM_ID', 'KeyType': 'RANGE'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'GAME_ID', 'AttributeType': 'S'},
                        {'AttributeName': 'TEAM_ID', 'AttributeType': 'N'}
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1
                    }
                )
        table.wait_until_exists()

    except Exception as e:
        raise

    return table

def init_populate():
    table = create_table()
    return
    try:
        r = leaguegamefinder.LeagueGameFinder(date_from_nullable='03/11/2021', league_id_nullable='00').get_normalized_dict()
        entries = len(r['LeagueGameFinderResults'])
        counter = 1
        for x in r['LeagueGameFinderResults']:
            x = json.loads(json.dumps(x), parse_float=str)
            try:
                table.put_item(Item=x)
            except Exception as e:
                #check for duplicate data
                pass
            print("Progress {:2.1%}".format(counter / entries))
            counter += 1

    except Exception as e:
        print(e)

    
def put_nightly_data():
    table = dynamo_conn.Table(name=TABLE_NAME)
    date = datetime.today() - timedelta(days=1)
    dt_string = str(date.strftime("%m/%d/%Y "))

    #api doesn't like leading 0 in date
    if(dt_string[0] == '0'):
        dt_string = dt_string[1:]
    r =  leaguegamefinder.LeagueGameFinder(date_from_nullable=dt_string, league_id_nullable='00').get_normalized_dict()
    for x in r['LeagueGameFinderResults']:
        x = json.loads(json.dumps(x), parse_float=str)
        try:
            table.put_item(Item=x)
        except Exception as e:
            #check for duplicate data
            pass




