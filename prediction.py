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
#from put_prediction_data import *
from sklearn.model_selection import train_test_split
#from sklearn.ensemble import RandomForestClassifier
from sklearn import svm

from sklearn.metrics import accuracy_score
TABLE_NAME='nba'

def query_games(year):
    #DON'T COMMIT WITH AWS KEYS!!!!
    dynamo_conn = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id='AKIAU3SZVQWPSL73LGUJ', aws_secret_access_key='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')
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
    
def extract_features_train(df, matchup, date):
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
        'FORM_HOME': team_form(home_past), #Team's recent preformances
        'FORM_AWAY': team_form(away_past),
        'HOME_WIN': label
    }
    return feat_dict

def extract_features_predict(df, home, away):
    home_past = df.loc[df['TEAM_ABBREVIATION'] == home]
    home_past = home_past.dropna()
    away_past = df.loc[df['TEAM_ABBREVIATION'] == away]
    away_past = away_past.dropna()

    feat_list = [
        avg_ppg(home_past), #Points per game
        avg_ppg(away_past),
        avg_fg_pct(home_past), #Field goal percentage
        avg_fg_pct(away_past),
        avg_ft_pct(home_past), #Free throw percentage
        avg_ft_pct(away_past),
        avg_rbpg(home_past), #Rebounds per game
        avg_rbpg(away_past),
        team_form(home_past), #Team form 
        team_form(away_past),
    ]
    return feat_list
def train_model(X, y):
    #return a trained classifier
    #clf = RandomForestClassifier(n_estimators=1000, random_state=42)
    clf = svm.SVC(kernel = 'linear', gamma = 'scale', probability= True)
    clf.fit(X, y)
    return clf

def test_model(clf, X, y_true):
    #test a trained model on labeled testing data
    y_pred = clf.predict(X)
    return accuracy_score(y_true, y_pred)

def predict_winner(df, home, away, clf_trained):
    #return if home team will win (1) or lose (0)
    feats = extract_features_predict(df, home, away)
    pred = clf_trained.predict([feats])
    pred_proba = clf_trained.predict_proba([feats])
    if pred:
        return home, round(pred_proba[0][1],3)
    else:
        return away, round(pred_proba[0][0], 3)