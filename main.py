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
    stats = browser.find_element_by_class_name('nba-stat-table')
    ofile = open('ttest.csv', "w", newline='\n')
    writer = csv.writer(ofile)
    statsText = stats.text
    statsText = statsText.split('\n')
    for i in statsText:
        writer.writerow(i)
        print(statsText)
    ofile.close()
        
stats()
browser.quit()
