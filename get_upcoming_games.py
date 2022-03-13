# ideja:
# uzmi meceve na tekuci dan i 2 dana posle
# izracunaj kvotu i upisi u tabelu
# ako danas igra jedna tim i sutra isto, kvota ne bi trebalo da se racuna za drugu
# ali cu izracunati, da ne komplikujem
# Tako da ce u bazi biti i kvote koje su neupotrebljive, kao i za utakmice koje su odlozene
# Ali nema veze, to je bilo stanje kvote na taj dan, sa trenutnim stanjem
# Kada budem radila poredjenje sa stvarnim rezultatom mogu da join-ujem po datumu


from time import sleep

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

options = Options()
# options.binary_location = "//usr/bin/chrome.exe"    #chrome binary location specified here
# options.add_argument("--headless")
options.add_argument("--start-maximized")  # open Browser in maximized mode
options.add_argument("--no-sandbox")  # bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.headless = True
import sqlite3

ser = Service("//home/branka/web_sracp2/chromedriver.exe")
driver = webdriver.Chrome(options=options, service=ser)
driver.get("https://www.rezultati.com/hokej/njemacka/del/raspored/")

WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()

soup = BeautifulSoup(driver.page_source, "html")
soup = BeautifulSoup(driver.page_source, features="html.parser")
div_tags = soup.find_all('div')
ids = []
# uzmi samo id-eve koje se odnose na utakmice
for div in div_tags:
    id = div.get('id')
    if id is not None and id[0] == 'g':
        ids.append(id)

    # nadji id za danasnji datum i 2 dana posle, ako taj id ne postoji u bazi

    upcoming_days = []
    current_day = datetime.datetime.now().day
    current_month = datetime.datetime.now().month
    current_date = (current_day, current_month)
    upcoming_days.append(current_date)

    next_day = (datetime.datetime.now() + datetime.timedelta(days=1)).day
    next_month = (datetime.datetime.now() + datetime.timedelta(days=1)).month
    next_date = (next_day, next_month)
    upcoming_days.append(next_date)

    next_next_day = (datetime.datetime.now() + datetime.timedelta(days=2)).day
    next_next_month = (datetime.datetime.now() + datetime.timedelta(days=2)).month
    next_next_date = (next_next_day, next_next_month)
    upcoming_days.append(next_next_date)

print(upcoming_days)
new_ids = []
for id in ids:
    results = soup.find(id=id)
    t = results.find("div", class_="event__time")
    game_day = int(t.text[:2])
    game_month = int(t.text[3:5])
    game_date = (game_day, game_month)
    is_postponed = 'Odgo' in t.text[-8:]
    if is_postponed:
        print(is_postponed)

    if game_date in upcoming_days and not is_postponed:
        new_ids.append(id)

scheduled_game_home_list = []
scheduled_game_away_list = []

for id in new_ids:
    results = soup.find(id=id)
    team_home = results.find("div", class_=lambda s: "event__participant event__participant--home" in s)
    team_away = results.find("div", class_=lambda s: "event__participant event__participant--away" in s)
    year_month_day_time = results.find("div", class_="event__time")
    year_month_day = int('2022' + year_month_day_time.text[3:5] + year_month_day_time.text[:2])

    scheduled_game_home_list.append(
        (id, 'Hokey', 'DEL', 'Germany', year_month_day, team_home.text, 1, 1, datetime.datetime.now()))
    scheduled_game_away_list.append(
        (id, 'Hokey', 'DEL', 'Germany', year_month_day, team_away.text, 0, 1, datetime.datetime.now()))

# print(games_list)
# print(results_home_list)
# print(results_away_list)

con = sqlite3.connect('bets.db')
cur = con.cursor()

try:

    cur.execute("update scheduled_games set is_current = 0")

    cur.executemany('''
    INSERT INTO scheduled_games (
            id, sport, league, country, year_month_day, team, is_home, is_current, created_at) VALUES 
            (?,?,?,?,?,?,?,?,?)
            ''',
                    scheduled_game_home_list)
    nb_home = cur.rowcount

    cur.executemany('''
    INSERT INTO scheduled_games (
            id, sport, league, country, year_month_day, team, is_home, is_current, created_at) VALUES 
            (?,?,?,?,?,?,?,?,?)
            ''',
                    scheduled_game_away_list)
    nb_away = cur.rowcount

    cur.execute('''
            INSERT INTO log_inserted_scheduled_games (
                    created_at, nb_of_lines_inserted, error_message) VALUES 
                    (?,?,?)
                    ''',
                (datetime.datetime.now(), nb_home + nb_away, 'successfully inserted'))

except Exception as e:
    cur.execute('''
        INSERT INTO log_inserted_scheduled_games (
                created_at, nb_of_lines_inserted, error_message) VALUES 
                (?,?,?)
                ''',
                (datetime.datetime.now(), -1, str(e)))

con.commit()
con.close()

# print(upcoming_days)
# print(new_ids)
