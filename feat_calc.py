import pandas as pd
import numpy as np
from datetime import timedelta,datetime
def avg_ppg(df):
    pts = round(sum(df['PTS'].astype(float)) , 4)
    poss = sum(df['FGA'].astype(float))- sum(df['OREB'].astype(float)) + sum(df['TOV'].astype(float)) + (0.4 * sum(df['FTA'].astype(float)))
    return (pts/poss)*100

def avg_fg_pct(df):
    return round(sum(df['FG_PCT'].astype(float)) / len(df), 4)

def avg_ft_pct(df):
    return round(sum(df['FT_PCT'].astype(float)) / len(df), 4)

def avg_rbpg(df):
    return round(sum(df['REB'].astype(int)) / len(df), 4)

    
def team_form(df):
    team1_id = df.iloc[0]['TEAM_ID']
    date1 = datetime.strptime(df.iloc[0]['GAME_DATE'],'%Y-%m-%d')
    past = date1 - timedelta(days=10)
    past = str(past.strftime('%Y-%m-%d'))
    team1_form = (df.loc[(df['GAME_DATE'] <= df.iloc[0]['GAME_DATE']) & (df['GAME_DATE'] >= past)
    & (df['TEAM_ID'] == team1_id)])
    team1_form = len(team1_form[team1_form.WL == 'W'])/ len(team1_form)
    return(team1_form)

def back_to_back(df):
    date1 = datetime.strptime(df.iloc[0]['GAME_DATE'],'%Y-%m-%d')
    past = date1 - timedelta(days=1)
    past = str(past.strftime('%Y-%m-%d'))
    if(len(df.loc[(df['GAME_DATE'] == past)])):
        return True
    else:
        return False
    