import json
import boto3
import uuid
from nba_api.stats.endpoints import boxscoretraditionalv2
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams
from datetime import timedelta,datetime

conn = boto3.resource('dynamodb', region_name= 'us-east-2',aws_access_key_id='', aws_secret_access_key='')
TABLE_NAME = 'nba'

def create_table():
    table = conn.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uuid',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
    table.wait_until_exists()
    return table

def init_populate():
    table = create_table()
    try:
        r =  leaguegamefinder.LeagueGameFinder(date_from_nullable='07/22/2020', league_id_nullable='00').get_normalized_dict()
        entries = len(r['LeagueGameFinderResults'])
        counter = 1
        for x in r['LeagueGameFinderResults']:
            uid = str(uuid.uuid4())
            x = json.loads(json.dumps(x), parse_float=str)
            x['uuid'] = uid
            table.put_item(Item=x)
            print("Progress {:2.1%}".format(counter / entries), end="\r")
            counter+=1
            
            
    except Exception as e:
        print(e)

    
def put_nightly_data():
    table = conn.Table(name=TABLE_NAME)
    date = datetime.today() - timedelta(days=1)
    dt_string = str(date.strftime("%m/%d/%Y "))

    #api doesn't like leading 0 in date
    if(dt_string[0] == '0'):
        dt_string = dt_string[1:]
    r =  leaguegamefinder.LeagueGameFinder(date_from_nullable=dt_string, league_id_nullable='00').get_normalized_dict()
    for x in r['LeagueGameFinderResults']:
            uid = str(uuid.uuid4())
            x = json.loads(json.dumps(x), parse_float=str)
            x['uuid'] = uid
            table.put_item(Item=x)


init_populate()





