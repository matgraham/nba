# Importing important modules required in making of News Machine
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

#This function will pull nba stats
def stats():
    page = driver.get('http://stats.nba.com/game/0021700001/')
    html = page.page_source
    soup = BeautifulSoup(html)
    box = soup.findall("li")
    print(box)
    # for x in range(len(stats.find_all("a"))):
    # 	news = (topstories[0].find_all("a")[x]).get_text().strip()
    # 	time.sleep(12)

stats()
