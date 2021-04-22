import pandas as pd
from prediction import query_games, train_model, extract_features_train, predict_winner
from sklearn.model_selection import train_test_split
import requests
from datetime import datetime
import boto3
import uuid
#from decimal import Decimal

dynamo_conn = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id='', aws_secret_access_key='')

TABLE_NAME_PRED = 'game_predictions'

def create_table():
    try:
        table_names = [table.name for table in dynamo_conn.tables.all()]
        if TABLE_NAME_PRED in table_names:
            table = dynamo_conn.Table(TABLE_NAME_PRED)
            print("Table already exists. Deleting table and recreating...")
            table.delete()
            table.wait_until_not_exists()
        else:
            print("Table does not exist, creating now...")

        table = dynamo_conn.create_table(
            TableName=TABLE_NAME_PRED,
            KeySchema=[
                {'AttributeName': 'MATCHUP_ID', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'MATCHUP_ID', 'AttributeType': 'S'}
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

def insert_item(table, data):
    #table = create_table()
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

    #List of teams
    teams = games['TEAM_ABBREVIATION'].unique()
    
    #Create all possible home/away matchups
    matchups = []
    for team1 in teams:
        for team2 in teams:
            if team1 != team2:
                matchups.append((team1, team2))

    #For each possible matchup, predict the winner and probability of that winner
    preds = []
    count = 0
    pred_table = create_table()
    for matchup in matchups:
        winner, proba = predict_winner(games, matchup[0], matchup[1], model)
        #proba_dec = Decimal(proba)
        matchup_id = str(uuid.uuid4())
        pred = {'MATCHUP_ID': matchup_id, 'HOME_TEAM': matchup[0], 'AWAY_TEAM': matchup[1], 'WINNER': winner, 'PROBABILITY': str(proba)}
        # Insert 'pred' as row in dynamo table
        insert_item(pred_table, pred)
        count += 1
        if count % 25 == 0:
            print("Matchups inserted: {}".format(count))
        #preds.append((winner, proba))
    
    print("Matchups inserted: {}".format(count))
    print("Complete")