#!/usr/bin/env python3

'''Current state: Main.py creates two csvs - stats.csv and games.csv. 
These feed into the Jupyter Notebook. 
Need to merge this games data into the stats dataframe, thereby creating the main dataframe
which will be used for data analysis. This dataframe will contain the player's stats as well
as info about whether or not they won, home or away, etc.''' 

# Importing required modules
import time
import requests
import csv
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox() 

#This function will pull up the correct webpage and feed that browser object to the stats and games functions. 
def webpull():
    browser.get('http://stats.nba.com/game/0021700001/')
    stats(browser)
    games(browser)


#This function pulls the player stats and adds them to the stats.csv file
def stats(browser):
    stats = browser.find_element_by_class_name('game-view')
    ofile = open('stats.csv', "w", newline='\n')
    writer = csv.writer(ofile)
    statsText = stats.text
    statsText = statsText.split('\n')
    for index,i in enumerate(statsText):
        if index > 11:
            writer.writerow(i)
        else:
            continue
    ofile.close()

#This function pulls game data and adds them to the games.csv file
def games(browser):
    game = browser.find_element_by_class_name('stats-game-summary')
    ofile = open('games.csv',"w")
    writer = csv.writer(ofile)
    gameText = game.text
    gameText = gameText.split('\n')
    for index,i in enumerate(gameText):
        writer.writerow(i)
    ofile.close()

webpull()
browser.quit()

#TODO: Create an iterable that will go through the NBA games.
