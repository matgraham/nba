#!/usr/bin/env python3

'''Current state: Main.py creates one csv - data.csv. 
This data file contains info for every game and will serve as the main data
source for the ML model. I need to add a few core features that the ML model will use
for predictions.''' 

# Importing required modules
import time
import requests
import os
import csv
import pandas as pd
import numpy as np
from player_data import main_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

'''
This will initialize the items that need to be initially initialized. 
browser: The webdriver for Selenium
main_dataframe: The blank dataframe where every game's data will append to
game_counter = a counter that will append the game number to the main_dataframe
'''  

browser = webdriver.Firefox() 

#This function will pull up the correct webpage and feed that browser object to the stats and games functions. 
def webpull(url):
    browser.get(url)
    stats(browser)
    #games(browser)
    #dataframe = main_function("stats_csv","games_csv")
    #dataframe_merge(dataframe)
    #print("Game {} successfully written!".format(game_counter))
    #reset("stats.csv", "games.csv")

#This function pulls the player stats and adds them to the stats.csv file
def stats(browser):
    stats = browser.find_element_by_class_name('block-league-content')
    print(stats)
    #ofile = open('stats.csv', "a", newline='\n')
    #writer = csv.writer(ofile)
    #statsText = stats.text
    #statsText = statsText.split('\n')
    #for index,i in enumerate(statsText):
        #if index > 10:
            #writer.writerow(i)
        #else:
            #continue
    #ofile.close()

#This function pulls game data and adds them to the games.csv file

webpull('http://www.nba.com/players/')

#main_dataframe.to_csv('data.csv', index=False)
browser.quit()


