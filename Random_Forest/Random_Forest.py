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