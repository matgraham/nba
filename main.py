#!/usr/bin/env python3

'''Current state: Main.py creates two csvs - stats.csv and games.csv. 
These feed into the Jupyter Notebook. 
Right now the stats.csv formats correctly in the jupyer notebook, but the games csv does not.
Need to format the games csv to remove commas and shrink it so it only contains the data needed. 
Need to merge this games data into the stats dataframe''' 

# Importing required modules
import time
import requests
import csv
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox() 

#This function will pull nba stats
def stats():
    browser.get('http://stats.nba.com/game/0021700001/')
    stats = browser.find_element_by_class_name('game-view')
    game = browser.find_element_by_class_name('stats-game-summary')
    ofile = open('stats.csv', "w", newline='\n')
    ofile2 = open('games.csv',"w")
    writer = csv.writer(ofile)
    writer2 = csv.writer(ofile2)
    statsText = stats.text
    statsText = statsText.split('\n')
    for index,i in enumerate(statsText):
        if index > 11:
            writer.writerow(i)
        else:
            continue
    gameText = game.text
    gameText = gameText.split('\n')
    for index,i in enumerate(gameText):
        writer2.writerow(i)
    print(gameText)
    ofile2.close()    
    ofile.close()
        
stats()
browser.quit()

#TODO: Break out the selenium get operation into its own function. 
#TODO: Seperate the stats and games csv exports into their own functions.
#TODO: Create an iterable that will go through the NBA games.
