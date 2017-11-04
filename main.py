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
    ofile = open('stats.csv', "w", newline='\n')
    writer = csv.writer(ofile)
    statsText = stats.text
    statsText = statsText.split('\n')
    print(statsText)
    for index,i in enumerate(statsText):
        if index > 11:
            writer.writerow(i)
        else:
            continue
    ofile.close()
        
stats()
browser.quit()

#TODO: Write a seperate CSV export that adds the team name, score, etc to a different csv
