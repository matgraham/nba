
# coding: utf-8

# In[1]:

import pandas as pd
import math
import numpy as np
import itertools


# In[2]:

#statsDF - initial stats dataframe
#gamesDF - initial games dataframe
#newGamesDF - formatted games dataframe with game date as index and rest of record in one row
#finalStats - formatted stats dataframe with player's name as the index
#mainDF: The dataframe where the main analysis will take place.


def main_function(stats,games, date, game_counter):
    stats = 'stats.csv'
    games = 'games.csv'


    # In[33]:

    #Dump the stats dataframe into a csv and clean it up
    cols = ['PLAYER', 'MIN', 'FGM','FGA', 'FG%', '3PM', '3PA','3P%','FTM','FTA','FT%','OREB','DREB','REB','AST','TOV','STL','BLK','PF','PTS','+/-']
    statsDF = pd.read_csv(stats, header= None, names=cols, index_col=False, error_bad_lines=False, delim_whitespace=True)
    statsDF[cols] = statsDF[cols].replace({'\$': '', ',': ''}, regex=True)
    statsDF['PLAYER'] = statsDF['PLAYER'].str.replace('.','')
    statsDF['PLAYER'] = statsDF['PLAYER'].str.replace('-','')
    statsDF['PLAYER'] = statsDF['PLAYER'].str.replace("'",'')
    statsDF['MIN'] = statsDF['MIN'].str.replace("'",'')
    statsDF['MIN'] = statsDF['MIN'].replace({'\$': '', '-': ''}, regex=True)
    
    # In[34]:

    #The nba.com site changed its formatting so this is to remove non-existent rows

    new_format_mask = 0
    for index, row in statsDF.iterrows():
        if new_format_mask == 1:
            statsDF.drop(index, inplace=True)
            if row.iloc[0] == 'Totals:' and math.isnan(row.iloc[1]) == True:
                new_format_mask = 0 
            else:
                continue
        else:
            if row.iloc[0] == 'PLAYER' and row.iloc[1] != "MIN":
                new_format_mask += 1
            else:
                continue

    for index, row in statsDF.iterrows():
        if row.iloc[0][3:4] == ":":
            statsDF.drop(index, inplace=True)

    # In[35]:

    statsDF = statsDF[statsDF.PLAYER != 'PLAYER']
    statsDF = statsDF[statsDF.PLAYER != 'Totals:']
    statsDF = statsDF[statsDF.MIN != 'PLAYERS']
    statsDF = statsDF[statsDF.PLAYER != 'Click']
    statsDF = statsDF[statsDF.PLAYER != 'GLOSSARY']
    statsDF = statsDF[statsDF.MIN != 'Filter']
    statsDF = statsDF.reset_index(drop=True)
    #Drop the first line for the team name
    statsDF.drop(0, inplace=True)
    statsDF = statsDF.reset_index(drop=True)

    # In[36]:

    #This will delete the second time a team is named. 
    for index, row in statsDF.iterrows():
        try: 
            if row.iloc[1].isalpha() and statsDF.iloc[index + 1][1].isalpha() or row.iloc[1] == "76ers":
                home_team_length = index/2
                statsDF.drop(index, inplace=True)
                statsDF = statsDF.reset_index(drop=True)
                break
        except:
            continue

   #Setting up the index on the main stats dataframe
    mainDFIndex = []
    for index, row in statsDF.iterrows():
        if row.iloc[0] == 'Nene':
            mainDFIndex.append(str(row['PLAYER']) + " " + str(row['MIN']))
        elif row.iloc[0].isalpha() == True and row.iloc[1].isalpha() == True:
            mainDFIndex.append(str(row['PLAYER']) + " " + str(row['MIN']))
    
    # In[39]:

    #Setup dicts from the DF
    statsDF_Dict = statsDF.T.to_dict().values()


    # In[40]:

    dict_list = []
    #Iterate through the statsDF and only return lines with stats or lines where players sat
    for index, i in enumerate(statsDF_Dict):
        if index == 1 or index % 2 != 0:
            dict_list.append(i)
        


    # In[41]:

    finalStats = pd.DataFrame(dict_list)
    finalStats.index = mainDFIndex
    finalStats.drop(['+/-'], axis=1, inplace=True)
    finalStats = finalStats.rename(columns={'PLAYER':'MIN','MIN':'FGM', 'FGM':'FGA', 'FGA':'FG%', 'FG%':'3PM', '3PM':'3PA', '3PA':'3P%', '3P%':'FTM', 'FTM':'FTA', 'FTA':'FT%', 'FT%':'OREB', 'OREB':'DREB', 'DREB':'REB', 'REB':'AST', 'AST':'TOV', 'TOV':'BLK', 'BLK':'PF', 'PF':'PTS', 'PTS':'+/-'})
    #This will replace the nan's with DNP
    finalStats = finalStats.fillna('NA')

    finalStats['Date'] = date
    finalStats['Game'] = game_counter
    #GAMES CELL: This prepares the games section into a dataframe
    #Passing in csv file and getting rid of the unused rows
    gamesDF = pd.read_csv(games, header= None, names=['a','b','c','d','e','f','g','h','i'], index_col=False, error_bad_lines=False, delim_whitespace=True)
    gamesDF.columns = [col.replace(',', '') for col in gamesDF.columns]
    #if you want to operate on multiple columns, put them in a list like so:
    games_cols = ['a','b','c','d','e','f','g','h','i']
    # pass them to df.replace(), specifying each char and it's replacement:
    gamesDF[games_cols] = gamesDF[games_cols].replace({'\$': '', ',': ''}, regex=True)
    # This will add the winner to column b of each 26th row
    for index, row in gamesDF.iterrows():
        if index % 26 == 0 or index == 0:
            if int(gamesDF['a'].iloc[index+4]) > int(gamesDF['a'].iloc[index + 8]):
                gamesDF['b'].iloc[index] = gamesDF['a'].iloc[index + 1]
            else:
                gamesDF['b'].iloc[index] = gamesDF['a'].iloc[index + 5]
        else:
            pass


    # In[44]:

    #This cell will arrange the gamesDF into the actual formatted games dataframe, newGamesDF
    #The next lines will pull the data from the cells in the gamesDF and into the newGamesDF dataframe
    gamesData = []
    games = 0
    for index, row in gamesDF.iterrows():
        if index == 0 or index % 26 == 0:
            gamesData.append(gamesDF.iloc[index+11,0])
            gamesData.append(gamesDF.iloc[index+12,0])
            gamesData.append(gamesDF.iloc[index,1])
            gamesData.append(gamesDF.iloc[index+11,1])
            gamesData.append(gamesDF.iloc[index+11,2])
            gamesData.append(gamesDF.iloc[index+11,3])
            gamesData.append(gamesDF.iloc[index+11,4])
            gamesData.append(gamesDF.iloc[index+12,1])
            gamesData.append(gamesDF.iloc[index+12,2])
            gamesData.append(gamesDF.iloc[index+12,3])
            gamesData.append(gamesDF.iloc[index+12,4])
            gamesData.append(gamesDF.iloc[index+8,0])
            gamesData.append(gamesDF.iloc[index+4,0])
            gamesData.append(gamesDF.iloc[index+22,2])
            gamesData.append(gamesDF.iloc[index+22,4])
            gamesData.append(gamesDF.iloc[index+22,6])
            games += 1
            
    gamesData = np.array(gamesData)
    gamesData = gamesData.reshape(games,16)
    #Create an empty dataframe, based on the games date as the index
    newGamesDF = pd.DataFrame(data = gamesData, columns=['Home','Away','W/L','1st Qtr H','2nd Qtr H','3rd Qtr H','4th Qtr H','1st Qtr A','2nd Qtr A','3rd Qtr A','4th Qtr A','Total H','Total A', 'Ref1','Ref2','Ref3'])
    
    for index,row in finalStats.iterrows():
        finalStats['1st Qtr H'] = newGamesDF['1st Qtr H'][0]
        finalStats['2nd Qtr H'] = newGamesDF['2nd Qtr H'][0]
        finalStats['3rd Qtr H'] = newGamesDF['3rd Qtr H'][0]
        finalStats['4th Qtr H'] = newGamesDF['4th Qtr H'][0]
        finalStats['1st Qtr A'] = newGamesDF['1st Qtr A'][0]
        finalStats['2nd Qtr A'] = newGamesDF['2nd Qtr A'][0]
        finalStats['3rd Qtr A'] = newGamesDF['3rd Qtr A'][0]
        finalStats['4th Qtr A'] = newGamesDF['4th Qtr A'][0]
        finalStats['Total H'] = newGamesDF['Total H'][0]
        finalStats['Total A'] = newGamesDF['Total A'][0]
        finalStats['Ref1'] = newGamesDF['Ref1'][0]
        finalStats['Ref2'] = newGamesDF['Ref2'][0]
        finalStats['Ref3'] = newGamesDF['Ref3'][0]
        finalStats['W/L'] = newGamesDF['W/L'][0]
        finalStats['Home'] = newGamesDF['Home'][0]
        finalStats['Away'] = newGamesDF['Away'][0]
        


    # In[46]:

    #This function will calculate the projected fantasy points per game
    def fantasy_points(row):
        try:
            score = (int(row['3PM']) * 3) + (int(row['FGM']) * 2) + (int(row['REB']) * 1) + (int(row['AST']) * 1.5) + (int(row['BLK']) * 3) + (int(row['STL']) * 3) + (int(row['TOV']) * -1)
            return score
        except:
            pass

    finalStats['Fantasy Score'] = finalStats.apply(fantasy_points, axis=1)
    finalStats = finalStats.fillna('NA')
    #finalStats['Player'] = finalStats.index
    return finalStats

# In[47]:




# In[ ]:




# In[ ]:




# In[ ]:



