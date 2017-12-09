#!/usr/bin/env python3

'''Current state: Main.py creates two csvs - stats.csv and games.csv. 
These feed into the Jupyter Notebook. 
Need to add logic operations which will add new columns for win/loss, team points, etc to 
main dataframe.''' 

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
<<<<<<< HEAD
def webpull(url):
    browser.get(url)
=======
def webpull():
    browser.get('http://stats.nba.com/game/0021700001/')
>>>>>>> 1a5925bc261524fe16e3b4f365e1a9239c5c976f
    stats(browser)
    games(browser)


#This function pulls the player stats and adds them to the stats.csv file
def stats(browser):
    stats = browser.find_element_by_class_name('game-view')
<<<<<<< HEAD
    ofile = open('stats.csv', "a", newline='\n')
=======
    ofile = open('stats.csv', "w", newline='\n')
>>>>>>> 1a5925bc261524fe16e3b4f365e1a9239c5c976f
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
<<<<<<< HEAD
    ofile = open('games.csv',"a")
=======
    ofile = open('games.csv',"w")
>>>>>>> 1a5925bc261524fe16e3b4f365e1a9239c5c976f
    writer = csv.writer(ofile)
    gameText = game.text
    gameText = gameText.split('\n')
    for index,i in enumerate(gameText):
        writer.writerow(i)
    ofile.close()

<<<<<<< HEAD
for i in range(2):
    webpull('http://stats.nba.com/game/002170000{}/'.format(i + 1))
=======
webpull()
>>>>>>> 1a5925bc261524fe16e3b4f365e1a9239c5c976f
browser.quit()

#TODO: Create an iterable that will go through the NBA games.
