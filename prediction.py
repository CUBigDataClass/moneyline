'''
Some help from 
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.04.html
'''
#pylint: disable=E1101

import boto3
from boto3.dynamodb.conditions import Key
import pandas as pd
import numpy as np
from feat_calc import *

TABLE_NAME='nba'

def query_games(year):
    #DON'T COMMIT WITH AWS KEYS!!!!
    dynamo_conn = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id='', aws_secret_access_key='')
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

    game_data = pd.DataFrame(response['Items'])
    game_data['IS_HOME'] = np.where(game_data['MATCHUP'].str.contains('@'), False, True)
    return game_data
    #return pd.DataFrame(response['Items'])

def extract_features(df, matchup, date):
    #create feature vector given team names
    if '@' in matchup:
        matchup_v2 = matchup[-3:] + ' vs. ' + matchup[:3]
    else:
        matchup_v2 = matchup[-3:] + ' @ ' + matchup[:3]

    game = df.loc[(df['GAME_DATE'] == date) & ((df['MATCHUP'] == matchup) | (df['MATCHUP'] == matchup_v2))]
    home = game.loc[game['IS_HOME'] == True]
    away = game.loc[game['IS_HOME'] == False]

    home_str = list(home['TEAM_NAME'])[0]
    home_past = df.loc[(df['GAME_DATE'] < date) & (df['TEAM_NAME'] == home_str)]
    away_str = list(away['TEAM_NAME'])[0]
    away_past = df.loc[(df['GAME_DATE'] < date) & (df['TEAM_NAME'] == away_str)]

    if list(home['WL'])[0] == 'W':
        label = 1
    else:
        label = 0

    feat_dict = {
        'PPG_HOME': avg_ppg(home_past), #Points per game
        'PPG_AWAY': avg_ppg(away_past),
        'FG_PCT_HOME': avg_fg_pct(home_past), #Field goal percentage
        'FG_PCT_AWAY': avg_fg_pct(away_past),
        'FT_PCT_HOME': avg_ft_pct(home_past), #Free throw percentage
        'FT_PCT_AWAY': avg_ft_pct(away_past),
        'RBPG_HOME': avg_rbpg(home_past), #Rebounds per game
        'RBPG_AWAY': avg_rbpg(away_past),
        'HOME_WIN': label
    }

    return feat_dict

def split_data():
    #split into training and testing
    return 0

def train_model():
    #return a trained classifier
    return 0

def predict_winner():
    #return if home team will win (True) or lose (False)
    return 0

if __name__=='__main__':
    query_year = '2020'
    games = query_games(query_year)
    #test = games.loc[(games['GAME_ID'] == '0022000004') & (games['TEAM_NAME'] == "Phoenix Suns")]
    test = extract_features(games, 'DAL @ PHX', '2020-12-23')
    
    print(test)