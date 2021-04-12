import json
import boto3
from prediction import *
import pandas as pd
from decimal import Decimal
import time

dynamo_conn = boto3.resource('dynamodb', region_name='us-west-2', aws_access_key_id='', aws_secret_access_key='')
# conn = boto3.resource('dynamodb', endpoint_url="http://host.docker.internal:8000/")
TABLE_NAME_PRED = 'nba_prediction'

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


def insert_item(table, data):

    try:
        item = {}
        for home_team, home_list in data.items():
            item['HOME_TEAM'] = home_team
            for away_dict in home_list:
                for away_team, proba in away_dict.items():
                    item[away_team] = round(Decimal(proba),3)
            table.put_item(Item=item)

    except Exception as e:
        print(e)

def build_expression(data):
    pf = 'prefix'
    vals = {}
    exp = 'SET '
    attr_names = {}
    for d in data:
        for key, value in d.items():
            vals[':{}'.format(key)] = round(Decimal(value),3)
            attr_names['#pf_{}'.format(key)] = key
            exp += '#pf_{} = :{},'.format(key, key)
    exp = exp.rstrip(",")
    return vals, exp, attr_names

def is_home_team_exist(table, home_team):
    try:
        x = table.get_item(Key={'HOME_TEAM': home_team})
    except Exception as e:
        print(e)

    if 'Item' not in x:
        return False

    return True

def update_item(table, data):

    for key, value in data.items():
        expression_vals, update_expression, attr_names = build_expression(value)
        table.update_item(
            Key={
                'HOME_TEAM': key
            },
            ExpressionAttributeNames=attr_names,
            ExpressionAttributeValues=expression_vals,
            UpdateExpression=update_expression,
            ReturnValues='NONE'
        )

def get_team_name(games):
    team_name = set()

    for game in games['TEAM_ABBREVIATION']:
        team_name.add(game)

    return team_name

def store_predict(games, model):
    # start = time.time()
    table = create_table()
    teams = get_team_name(games)
    data = {}
    for home_team in teams:
        home_list = []
        for away_team in teams:
            if home_team == away_team:
                winner, proba = home_team, 1
            else:
                winner, proba = predict_winner(games, home_team, away_team, model)

            # print("Prediction: {} will win with {}% probability.".format(winner, proba * 100))
            if winner != home_team:
                proba = 1 - proba
            home_list.append({away_team: proba})

        data = {home_team : home_list}
        if is_home_team_exist(table, home_team):
            update_item(table, data)
        else:
            insert_item(table, data)
    print("Complete")
    # print(data)
    # end = time.time()
    # print(end - start)





