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
#options.add_argument("--headless")
options.add_argument("--start-maximized")  # open Browser in maximized mode
options.add_argument("--no-sandbox")  # bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#options.headless = True

ser = Service("//home/branka/web_sracp2/chromedriver.exe")
driver = webdriver.Chrome(options=options, service=ser)
driver.get("https://www.rezultati.com/hokej/njemacka/del/rezultati/")


#id = soup.find(id="tournament-table-tabs-and-content")
#broj_golova = id.find_all('a', href=True)
#broj_golova.click()
#print(broj_golova)
#bg=driver.find_element(By.CLASS_NAME, "tabs__text tabs__text--default").click()
#tabs__text tabs__text--default
#onetrust-accept-btn-handler
#driver.implicitly_wait(5)

WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
#mainWindowHandle = driver.getWindowHandle()
#mainWindowHandle = driver.window_handles


WebDriverWait(driver, 360).until(EC.element_to_be_clickable((By.LINK_TEXT, "Prikaži još mečeva"))).click()
WebDriverWait(driver, 360).until(EC.element_to_be_clickable((By.LINK_TEXT, "Prikaži još mečeva"))).click()

#print(mainWindowHandle)
#print(allWindowHandles)
#driver.switch_to.window(window_after)

#driver.back()
#driver.forward()


soup = BeautifulSoup(driver.page_source, "html")
soup = BeautifulSoup(driver.page_source, features="html.parser")
div_tags = soup.find_all('div')
ids = []
for div in div_tags:
     id = div.get('id')
     if id is not None and id[0] == 'g':
         ids.append(id)

con = sqlite3.connect('bets.db')
cur = con.cursor()

# sqlite allows primary key column to contain NULL values
# Create table


cur.execute('''CREATE TABLE games
             (  
               id text,
               sport text,
               league text,
               country text,
               created_at timestamp,
               
               constraint pk_games_id primary key (id)
              )''')


cur.execute('''CREATE TABLE results
             (  
               game_id text,
               year_month_day int,
               team text,
               goal int,
               is_home int,
               created_at timestamp,
               
               constraint pk_results_year_month_day_team primary key (year_month_day, team),
               constraint fk_results_game_id foreign key (game_id) references games (id)
              )''')

#new_ids = []

#for id in ids:
 #   results = soup.find(id=id)
    #t = results.find("div", class_="event__time")
    #if t.text[0:6] == '21.01.':
  #  new_ids.append(id)

#print(new_ids)


# napravi liste ciji su elementi tuple-i, da bi posle celu listu insertovali u tabeli,
# a ne red po red
games_list = []
results_home_list = []
results_away_list = []

for id in ids:
    results = soup.find(id=id)
    team_home = results.find("div", class_=lambda s: "event__participant event__participant--home" in s)
    team_away = results.find("div", class_=lambda s: "event__participant event__participant--away" in s)
    goal_home = results.find("div", class_="event__score event__score--home")
    goal_away = results.find("div", class_="event__score event__score--away")
    year_month_day_time = results.find("div", class_="event__time")
    if year_month_day_time.text[3:5] in ['01', '02']:
        year_month_day = '2022' + year_month_day_time.text[3:5] + year_month_day_time.text[:2]
    else:
        year_month_day = '2021' + year_month_day_time.text[3:5] + year_month_day_time.text[:2]
    year_month_day = int(year_month_day)

    games_list.append((id, 'Hokey', 'DEL', 'Germany', datetime.datetime.now()))
    results_home_list.append((id, year_month_day, team_home.text, int(goal_home.text), 1, datetime.datetime.now()))
    results_away_list.append((id, year_month_day, team_away.text, int(goal_away.text), 0, datetime.datetime.now()))

print(games_list)
print(results_home_list)
print(results_away_list)

cur.executemany('''
    INSERT INTO games (
            id, sport, league, country, created_at) VALUES 
            (?,?,?,?,?)
            ''',
            (games_list))
con.commit()
#id, 'Hokey', 'DEL', 'Germany', datetime.datetime.now()
cur.executemany('''
    INSERT INTO results (
            game_id, year_month_day, team, goal, is_home, created_at) VALUES 
            (?,?,?,?,?,?)
            ''',
            (results_home_list))
con.commit()
#id, year_month_day, team_home.text, int(goal_home.text), 1, datetime.datetime.now())


cur.executemany('''
    INSERT INTO results (
            game_id, year_month_day, team, goal, is_home, created_at) VALUES 
            (?,?,?,?,?,?)
            ''',
            (results_away_list))
con.commit()
#id, year_month_day, team_away.text, int(goal_away.text), 0, datetime.datetime.now()

con.close()
driver.close()
'''
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
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
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
git remote add origin https://github.com/brankasando/testbsa.git

'''
