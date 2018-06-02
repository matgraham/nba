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
from PlayerDataCleanup import main_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

'''
This will initialize the items that need to be initially initialized. 
browser: The webdriver for Selenium
main_dataframe: The blank dataframe where every game's data will append to
game_counter = a counter that will append the game number to the main_dataframe
'''  

browser = webdriver.Chrome() 

#This function will pull up the correct webpage and feed that browser object to the stats and games functions. 
def webpull(url):
    browser.get(url)
    browser.execute_script("window.scrollTo(0, 40000)")
    stats(browser)
    
    
#This function pulls the player stats and adds them to the stats.csv file
def stats(browser):
    stats = browser.find_element_by_class_name('block-league-content')
    teams = browser.find_elements_by_class_name('nba-player-index__team-image')
    ofile = open('players.csv', "a", newline='\n')
    writer = csv.writer(ofile)
    statsText = stats.text
    teamsList = [x.get_attribute("href") for x in teams]
    print(teamsList)
    statsText = statsText.split('\n')
    team_index =  0
    for index,i in enumerate(statsText):
        if index > 1752:
            writer.writerow(i)
            if (index + 1) % 5 == 0:
                writer.writerow(teamsList[team_index])
                team_index += 1
        elif index > 0:
            writer.writerow(i)
            if index % 5 == 0:
                writer.writerow(teamsList[team_index])
                team_index += 1
        else:
            continue
    ofile.close()



webpull('http://www.nba.com/players/')


browser.quit()


