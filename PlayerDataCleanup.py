
# coding: utf-8

# In[107]:

import pandas as pd
import numpy as np
import itertools


# In[ ]:





def main_function(players_csv):
    #Dump the stats dataframe into a csv and clean it up
    cols = ['Name', 'Team', 'Position','Height', 'Weight']
    statsDF = pd.read_csv(players_csv, header= None, names=cols, index_col=False, error_bad_lines=False, delim_whitespace=True)
    statsDF[cols] = statsDF[cols].replace({'\$': '', ',': ''}, regex=True)


    # In[109]:

    #index 0
    first_name = []
    #index 1
    last_name = []
    #index 2
    position = []
    #index 3
    height = []
    #index 5
    team =[]
    for index, row in statsDF.iterrows():
        if index % 6 == 0:
            first_name.append(statsDF.iloc[index-6][0])
            last_name.append(statsDF.iloc[index-5][0])
            position.append(statsDF.iloc[index-4][0])
            height.append(statsDF.iloc[index-3][0])
            team.append(statsDF.iloc[index-1][0])
                
            


    # In[110]:

    players_dict = {'First Name':first_name,"Last Name":last_name,'Position':position,'Height':height,'Team':team}


    # In[111]:

    playersDf = pd.DataFrame(players_dict)


    # In[112]:

    playersDf


    # In[113]:

    def team_cleanup(string):
        return string[25:-1]    


    # In[118]:

    playersDf['Team'] = playersDf['Team'].apply(team_cleanup)


    # In[119]:

    return playersDf


    # In[ ]:



