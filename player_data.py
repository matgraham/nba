# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import itertools


# In[2]:

#statsDF - initial stats dataframe
#gamesDF - initial games dataframe
#newGamesDF - formatted games dataframe with game date as index and rest of record in one row
#finalStats - formatted stats dataframe with player's name as the index
#mainDF: The dataframe where the main analysis will take place.


# In[3]:
def main_function(stats_csv, games_csv):
    stats_csv = "stats.csv"
    games_csv = "games.csv"
    #Dump the stats dataframe into a csv and clean it up
    cols = ['PLAYER', 'MIN', 'FGM','FGA', 'FG%', '3PM', '3PA','3P%','FTM','FTA','FT%','OREB','DREB','REB','AST','TOV','STL','BLK','PF','PTS','+/-']
    statsDF = pd.read_csv(stats_csv, header= None, names=cols, index_col=False, error_bad_lines=False, delim_whitespace=True)
    statsDF[cols] = statsDF[cols].replace({'\$': '', ',': ''}, regex=True)


    # In[4]:

    statsDF = statsDF[statsDF.PLAYER != 'PLAYER']
    statsDF = statsDF[statsDF.PLAYER != 'Totals:']
    statsDF = statsDF[statsDF.PLAYER != 'INACTIVE']
    statsDF = statsDF.reset_index(drop=True)


    # In[5]:

    home_city = []
    flag = 0
    away_player_count = 0
    for index,row in statsDF.iterrows():
        if index == 26 and flag == 0:
            flag = 1
        else:
            if row[0] == 'DNP' or row[0] == 'NWT':
                flag = 1
            else:
                if statsDF.iloc[index + 1][0] == 'DNP' or statsDF.iloc[index + 1][0] == 'NWT':
                    continue
                elif flag == 1:
                    home_city.append(row[0])
                    if index % 2 == 0:
                        home_city.append(statsDF.iloc[-1][0])
                        away_city = [statsDF.iloc[0][0],statsDF.iloc[-2][0]]
                        statsDF = statsDF[statsDF.PLAYER != home_city[1]]
                        statsDF = statsDF[statsDF.PLAYER != away_city[0]]
                        statsDF = statsDF[statsDF.PLAYER != away_city[1]]
                        statsDF = statsDF.reset_index(drop=True)
                        away_player_count = int(statsDF.index[index] / 2)
                        break
                    else:
                        home_city.append(statsDF.iloc[-1][0])
                        away_city = [statsDF.iloc[0][0],statsDF.iloc[-2][0]]
                        statsDF = statsDF[statsDF.PLAYER != home_city[0]]
                        statsDF = statsDF[statsDF.PLAYER != home_city[1]]
                        statsDF = statsDF[statsDF.PLAYER != away_city[0]]
                        statsDF = statsDF[statsDF.PLAYER != away_city[1]]
                        statsDF = statsDF.reset_index(drop=True)
                        away_player_count = int(statsDF.index[index] / 2)
                        break
                else:
                    continue



    # In[6]:

    #Setting up the index on the main stats dataframe
    mainDFIndex = []
    for index, row in statsDF.iterrows():
        if index % 2 == 0:
            mainDFIndex.append(str(row['PLAYER']) + " " + str(row['MIN']))
    
    # In[9]:

    #Setup dicts with the sub categories
    newDict = dict()
    something = statsDF.T.to_dict().values()
    pos = ''
    for index, i in enumerate(something):
        if index % 2 != 0:
            newDict[index] = i
            newDict[index]['POS'] = pos
        else:
            if i['FGM'] == 'nan':
                continue
            else:
                pos = i['FGM']


    finalStats = pd.DataFrame.from_dict(newDict,orient='index')
    #finalStats.index = mainDFIndex
    finalStats.drop(['+/-'], axis=1, inplace=True)
    finalStats = finalStats.rename(columns={'PLAYER':'MIN','MIN':'FGM', 'FGM':'FGA', 'FGA':'FG%', 'FG%':'3PM', '3PM':'3PA', '3PA':'3P%', '3P%':'FTM', 'FTM':'FTA', 'FTA':'FT%', 'FT%':'OREB', 'OREB':'DREB', 'DREB':'REB', 'REB':'AST', 'AST':'TOV', 'TOV':'BLK', 'BLK':'PF', 'PF':'PTS', 'PTS':'+/-'})
    player_count = len(finalStats.index)
    teams_list = ((away_city[0] + " ") * away_player_count) + ((home_city[0] + " ") * (player_count - away_player_count))
    teams_list = teams_list.split()
    opponent_list = ((home_city[0] + " ") * away_player_count) + ((away_city[0] + " ") * (player_count - away_player_count))
    opponent_list = opponent_list.split()
    finalStats['Player'] = mainDFIndex
    finalStats['TEAM'] = teams_list
    finalStats['OPPONENT'] = opponent_list
    #This will replace the nan's with DNP
    finalStats = finalStats.fillna('NA')


    # In[11]:

    #GAMES CELL: This prepares the games section into a dataframe
    #Passing in csv file and getting rid of the unused rows
    gamesDF = pd.read_csv(games_csv, header= None, names=['a','b','c','d','e','f','g','h','i'], index_col=False, error_bad_lines=False, delim_whitespace=True)
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


    # In[12]:

    #This cell will arrange the gamesDF into the actual formatted games dataframe, newGamesDF
    #Setting up the index on the main stats dataframe
    dateIndex = []
    month = ['OCT', 'NOV', 'DEC', 'JAN', 'FEB']
    for index, row in gamesDF.iterrows():
        for i in month:
            if gamesDF.iloc[index][0] == i:
                dateIndex.append(gamesDF.iloc[9,0] + " " + gamesDF.iloc[9,1][1] + ", " + gamesDF.iloc[9,2])
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

    # In[14]:

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

    # In[15]:

    #This function will calculate the projected fantasy points per game
    def fantasy_points(row):
        try:
            score = (int(row['3PM']) * 3) + (int(row['FGM']) * 2) + (int(row['REB']) * 1) + (int(row['AST']) * 1.5) + (int(row['BLK']) * 3) + (int(row['STL']) * 3) + (int(row['TOV']) * -1)
            return score
        except:
            pass

    finalStats['Fantasy Score'] = finalStats.apply(fantasy_points, axis=1)
    finalStats = finalStats.fillna('NA')
    return finalStats
    


