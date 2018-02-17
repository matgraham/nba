#!/usr/bin/env python3

'''Current state: Main.py creates two csvs - stats.csv and games.csv. 
These feed into the Jupyter Notebook. The jupyter notebook is good to go. Need to update 
the loop below so it will loop through the entire season.''' 

# Importing required modules
import time
import requests
import csv
import pandas as pd
import numpy as np
import player_data
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox() 

#This function will pull up the correct webpage and feed that browser object to the stats and games functions. 
def webpull(url):
    browser.get(url)
    stats(browser)
    games(browser)



#This function pulls the player stats and adds them to the stats.csv file
def stats(browser):
    stats = browser.find_element_by_class_name('game-view')
    ofile = open('stats.csv', "a", newline='\n')
    writer = csv.writer(ofile)
    statsText = stats.text
    statsText = statsText.split('\n')
    for index,i in enumerate(statsText):
        if index > 10:
            writer.writerow(i)
        else:
            continue
    ofile.close()

#This function pulls game data and adds them to the games.csv file
def games(browser):
    game = browser.find_element_by_class_name('stats-game-summary')
    ofile = open('games.csv',"a")
    writer = csv.writer(ofile)
    gameText = game.text
    gameText = gameText.split('\n')
    for index,i in enumerate(gameText):
        writer.writerow(i)
    ofile.close()

webpull('http://stats.nba.com/game/0021700001/')

# for i in range(1):
#     if i < 9:
#         webpull('http://stats.nba.com/game/002170000{}/'.format(i + 1))
#     else:
#         webpull('http://stats.nba.com/game/00217000{}/'.format(i + 1))
browser.quit()


