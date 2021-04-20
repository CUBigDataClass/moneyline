import pandas as pd
from prediction import query_games, train_model, extract_features_train, predict_winner
from sklearn.model_selection import train_test_split
import requests
from datetime import datetime
import boto3
#from decimal import Decimal

dynamo_conn = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id='AKIAU3SZVQWPSL73LGUJ', aws_secret_access_key='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')

TABLE_NAME_PRED = 'game_predictions'

def create_table():
    try:
        table_names = [table.name for table in dynamo_conn.tables.all()]
        if TABLE_NAME_PRED in table_names:
            table = dynamo_conn.Table(TABLE_NAME_PRED)
        else:
            table = dynamo_conn.create_table(
                TableName=TABLE_NAME_PRED,
                KeySchema=[
                    {'AttributeName': 'HOME_TEAM', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'HOME_TEAM', 'AttributeType': 'S'}
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

def insert_item(data):
    table = create_table()
    response = table.put_item(
       Item=data
    )

def delete_table():
    table_names = [table.name for table in dynamo_conn.tables.all()]
    if TABLE_NAME_PRED in table_names:
        table = dynamo_conn.Table(TABLE_NAME_PRED)
        table.delete()
    else:
        return 0

if __name__=='__main__':
    #query games from 2020 and 2021 for training data
    games20 = query_games('2020')
    games21 = query_games('2021') 
    games = games20.append(games21)

    #Loop through every row of 2021 games and extract relevant features
    used_ids = []
    feat_dicts = []
    for i, row in games.iterrows():
        if row['GAME_DATE'][:4] == '2021':
            if row['GAME_ID'] not in used_ids:
                #print(row['MATCHUP'])
                new_feats = extract_features_train(games, row['MATCHUP'], row['GAME_DATE'])
                feat_dicts.append(new_feats)
                used_ids.append(row['GAME_ID'])
    
    #Create dataframe of extracted training features
    feat_df = pd.DataFrame(feat_dicts)

    #Separate labels from features
    labels = feat_df['HOME_WIN']
    feats = feat_df.loc[:, feat_df.columns != 'HOME_WIN']

    #Train model on all past data
    model = train_model(feats, labels)

    #Delete predicitons table so we can recreate it and fill it with current predictions
    #delete_table()

    #Construct request to get today's games
    date = datetime.today()
    dt_string = str(date.strftime("%Y-%m-%d "))
    request_string = 'https://www.balldontlie.io/api/v1/games?start_date=' + dt_string + '&end_date=' + dt_string
    response = requests.get(request_string)

    #From today's games, grab the home and away team abbreviation
    todays_games = response.json()
    todays_matchups = []
    for game in todays_games['data']:
        todays_matchups.append((game['home_team']['abbreviation'], game['visitor_team']['abbreviation']))

    #For each of today's games, predict the winner and probability of that winner
    preds = []
    for matchup in todays_matchups:
        winner, proba = predict_winner(games, matchup[0], matchup[1], model)
        #proba_dec = Decimal(proba)
        pred = {'HOME_TEAM': matchup[0], 'AWAY_TEAM': matchup[1], 'WINNER': winner, 'PROBABILITY': str(proba)}
        # Insert 'pred' as row in dynamo table
        insert_item(pred)
        #preds.append((winner, proba))
    
    print("Complete")