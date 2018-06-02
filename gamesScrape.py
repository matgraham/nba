#!/usr/bin/env python3

'''Current state: Main.py creates one csv - data.csv. 
The web scrape is getting hung up on game 32''' 

# Importing required modules
import time
import requests
import os
import csv
import pandas as pd
import numpy as np
from gameStats import main_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

'''
This will initialize the items that need to be initially initialized. 
browser: The webdriver for Selenium
main_dataframe: The blank dataframe where every game's data will append to
game_counter = a counter that will append the game number to the main_dataframe
'''  

browser = webdriver.Chrome()
main_dataframe = pd.DataFrame()
game_counter =  30

#This function will pull up the correct webpage and feed that browser object to the stats and games functions. 
def webpull(url):
    browser.get(url)
    stats(browser)
    games(browser)
    dataframe = main_function("stats_csv","games_csv")
    dataframe_merge(dataframe)
    print("Game {} successfully written!".format(game_counter))
    stats_csv = '/home/acer/github/nba/stats.csv'
    games_csv = '/home/acer/github/nba/games.csv'
    reset(stats_csv, games_csv)

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

def reset(stats_csv, games_csv):
    os.remove(stats_csv)
    os.remove(games_csv)

'''
This will collect the individual dataframe for each individual game into a master dataframe
and then delete the specific game's dataframe so the next webpull will be empty
'''
def dataframe_merge(dataframe):
    global main_dataframe
    main_dataframe = main_dataframe.append(dataframe, ignore_index=True)
    main_dataframe['Game'] = game_counter
    #dataframe.drop(dataframe.index, inplace=True)
    
for i in range(30,80):
    if i < 9:
        webpull('http://stats.nba.com/game/002170000{}/'.format(i + 1))
        game_counter += 1
    else:
        webpull('http://stats.nba.com/game/00217000{}/'.format(i + 1))
        game_counter += 1

#webpull('http://stats.nba.com/game/0021700035/')

main_dataframe.to_csv('data.csv', index=False)
browser.quit()


