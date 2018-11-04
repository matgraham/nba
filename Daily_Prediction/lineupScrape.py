#!/usr/bin/env python3

# Importing required modules
import time
import requests
import os
import csv
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

'''
This will initialize the items that need to be initially initialized. 
browser: The webdriver for Selenium
'''  

browser = webdriver.Chrome(r'F:\Projects\NBA\chromedriver_win32\chromedriver.exe')
browser.get('https://www.rotowire.com/daily/nba/optimizer.php?site=FanDuel')
time.sleep(2)
lineup = browser.find_elements_by_class_name('salary')
for i in lineup:
    print(lineup.text)
browser.quit()


