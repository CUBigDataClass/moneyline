from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import pandas as pd
from prediction import query_games, train_model, extract_features_train, predict_winner
from sklearn.model_selection import train_test_split
#from sklearn.ensemble import RandomForestClassifier
import requests
from datetime import datetime

application = Flask(__name__)
api = Api(application)

class Predictions(Resource):
    def get(self):
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
            preds.append((winner, proba))

        return preds

api.add_resource(Predictions, '/get')

if __name__ == '__main__':
    application.run(debug=True)