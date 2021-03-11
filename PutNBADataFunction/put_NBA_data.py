import json
import boto3
import uuid
from nba_api.stats.endpoints import boxscoretraditionalv2
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams

conn = boto3.resource('dynamodb', region_name= 'us-east-2',aws_access_key_id='', aws_secret_access_key='')
TABLE_NAME = 'nba'
table = conn.Table(name=TABLE_NAME)


def init_populate():
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
    
init_populate()



