'''Notes:
1. Need to add the previous seasons average to the csv file. After that, the machine learning section should be broken out to its own module and then called on all of the important
features in determining the fan duel fantasy score. The players year should be entered, but this should be a dummy variable
instead of an actual int value. 

3. This should be imported into the flask site with the ability to import all of the days players'''

import pandas as pd
import numpy as np
import os
from regressor import rf_regressor

# Data Cleanup

os.chdir(r'F:\Projects\NBA\DB_Files')
df = pd.read_csv('master.csv')

targets = ['TOV', 'REB', '3PM', 'FGM', 'PTS', 'AST', 'STL', 'BLK']
#Add how well they did in the last game
for i in targets:
    df['Last_Game_' + i] = df.groupby('Name')[i].shift(1)   
    #df['Last_Game_Points'] = df.groupby('Name').PTS.shift(1)

    #The rolling average method returns a multi-index dataframe. This needs to be added to the dataframe with the indexs dropped. 
    average = df.groupby('Name')[i].rolling(5).mean()
    #average = df.groupby('Name')['PTS'].rolling(5).mean()
    df["Average" + i] = average.reset_index(level=0, drop=True)
    #df["Average"] = average.reset_index(level=0, drop=True)

df['Date'] = pd.to_datetime(df['Date'])

#The function to fix the game number issue
def game_number_fix(row):
    if row['Game'] > 800:
        return row['Game'] - 99
    else:
        return row['Game']   

df['game_number'] = df.apply(lambda row: game_number_fix(row),axis=1)

def home(row):
    if row['Home'] == row['Team']:
        return row['Home']
    else: 
        return row['Away']

#Add a column for whether they are home or away
df['Home/Away'] = np.NAN
df['Home/Away'] = df.apply(lambda row: home(row), axis=1)

def opposing_team(row):
    if row['Home'] == row['Team']:
        return row['Away']
    else: 
        return row['Home'] 

#Add a column for their opponent
df['Opponent'] = np.NAN
df['Opponent'] = df.apply(lambda row: opposing_team(row), axis=1)

df.to_csv('Master.csv', index=False)

df.drop(columns=['PTS','Home', 'Away','Game', 'MIN', 'Date','FTM', '3P%', '3PA', 'PF', 'FG%', 'FGA',
       'OREB', 'FT%', 'FTA', 'DREB','+/-', '1QH', '2QH', '3QH', '4QH', '1QA', '2QA', '3QA',
       '4QA', 'Total_H', 'Total_A', 'W/L','Fantasy_Score'], axis=1,inplace=True)


df_dummies = pd.get_dummies(df)

df_dummies = df_dummies.fillna(0)

results = rf_regressor(df_dummies)

def fantasy_points(df):
    score = (df['3PM'] * 3) + (df['FGM'] * 2) + (df['REB'] * 1) + (df['AST'] * 1.5) + (df['BLK'] * 3) + (df['STL'] * 3) + (df['TOV'] * -1)
    return score

results['Fantasy Score'] = results.apply(fantasy_points, axis=1)


print(results)