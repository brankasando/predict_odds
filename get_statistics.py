from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import datetime

import os

import config_environment as ce

options = Options()
# options.binary_location = "//usr/bin/chrome.exe"    #chrome binary location specified here
# options.add_argument("--headless")
options.add_argument("--start-maximized")  # open Browser in maximized mode
options.add_argument("--no-sandbox")  # bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.headless = ce.headless

ser = Service("/" + ce.path_to_db + "/chromedriver.exe")
driver = webdriver.Chrome(options=options, service=ser)

def get_statistics_per_game_id(game_id):
    website_url = "https://www.rezultati.com/utakmica/" + game_id + "/#/detalji/statistika-utakmice/0"
    website_url_elements = website_url.split("/")
    driver.get(website_url)
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()

    soup = BeautifulSoup(driver.page_source, "html")
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    stat_home = soup.findAll("div", class_="stat__homeValue")
    stat_away = soup.findAll("div", class_="stat__awayValue")
    stat_home_list = []
    stat_away_list = []

    for i in stat_home:
        stat_home_list.append(i.text)

    for i in stat_away:
        stat_away_list.append(i.text)

    print(stat_home_list)
    print(stat_away_list)

get_statistics_per_game_id("AkjzkAnA")