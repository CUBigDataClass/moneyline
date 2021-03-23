from datetime import timedelta,datetime
import json
import boto3
from nba_api.stats.endpoints import leaguegamefinder

TABLE_NAME = 'nba'
dynamo_conn = boto3.resource('dynamodb', region_name= 'us-east-2',aws_access_key_id='', aws_secret_access_key='')


def put_daily_data():
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
            print(e)


if __name__ == "__main__":
    put_daily_data()