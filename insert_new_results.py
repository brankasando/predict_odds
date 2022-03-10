# ideja:
# proveri da li datum postoji u bazi
# ako ne, onda uzmi za sve datume od tog datum rezultate i upisi u bazu

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


ser = Service("//home/branka/web_sracp2/chromedriver.exe")
driver = webdriver.Chrome(options=options, service=ser)
driver.get("https://www.rezultati.com/hokej/njemacka/del/rezultati/")

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

con = sqlite3.connect('bets.db')
cur = con.cursor()

# sqlite allows primary key column to contain NULL values
# Create table

max_date = cur.execute(''' select max(year_month_day) from results ''')
# use list() to get the details other than the cursor object.
# max_date je bio cursor objekat, sa list vraca tuple
max_date = list(max_date)[0][0]
#print(max_date)
# ako se skripta za insert izvrsava ujutru na dan x
# ako se se neka utakmica zavrsila rano na dan x, pre izvrsenja skipta
# onda ce taj datum uci u bazu i nece uci utakmice odigrane taj dan x, ali kasnije
# kada se sledeci dan bude radio insert

# nadji id za datum koji ne postoji u bazi
new_ids = []
for id in ids:
    results = soup.find(id=id)
    t = results.find("div", class_="event__time")

    if t.text[3:5] in ['09', '10', '11', '12']:
        year_month_day = '2021' + t.text[3:5] + t.text[:2]
    else:
        year_month_day = '2022' + t.text[3:5] + t.text[:2]
    year_month_day = int(year_month_day)
   # print(year_month_day)
    if year_month_day > max_date:
        new_ids.append(id)

games_list = []
results_home_list = []
results_away_list = []

for id in new_ids:
    results = soup.find(id=id)
    team_home = results.find("div", class_=lambda s: "event__participant event__participant--home" in s)
    team_away = results.find("div", class_=lambda s: "event__participant event__participant--away" in s)
    goal_home = results.find("div", class_="event__score event__score--home")
    goal_away = results.find("div", class_="event__score event__score--away")
    year_month_day_time = results.find("div", class_="event__time")
    year_month_day = int('2022' + year_month_day_time.text[3:5] + year_month_day_time.text[:2])

    games_list.append((id, 'Hokey', 'DEL', 'Germany', datetime.datetime.now()))
    results_home_list.append((id, year_month_day, team_home.text, int(goal_home.text), 1, datetime.datetime.now()))
    results_away_list.append((id, year_month_day, team_away.text, int(goal_away.text), 0, datetime.datetime.now()))

print(games_list)
print(results_home_list)
print(results_away_list)


try:

    cur.executemany('''
    INSERT INTO games 
        (
            id, sport, league, country, created_at
        ) VALUES 
            (?,?,?,?,?)
            ''',
            games_list)
    nb = cur.rowcount
    cur.execute('''
                INSERT INTO log_inserted_games 
                (
                    created_at, nb_of_lines_inserted, error_message
                ) VALUES
                  (?,?,?)
                   ''',
                (datetime.datetime.now(), nb, 'successfully inserted'))


except Exception as e:

    cur.execute('''
        INSERT INTO log_inserted_games 
        (
            created_at, nb_of_lines_inserted, error_message
        ) VALUES 
          (?,?,?)
          ''',
          (datetime.datetime.now(), -1, str(e)))

con.commit()


try:
    cur.executemany('''
    INSERT INTO results (
            game_id, year_month_day, team, goal, is_home, created_at) VALUES 
            (?,?,?,?,?,?)
            ''',
            results_home_list)
    nb_home = cur.rowcount

    cur.executemany('''
    INSERT INTO results (
            game_id, year_month_day, team, goal, is_home, created_at) VALUES
            (?,?,?,?,?,?)
            ''',
           results_away_list)
    nb_away = cur.rowcount

    cur.execute('''
            INSERT INTO log_inserted_results (
                    created_at, nb_of_lines_inserted, error_message) VALUES
                    (?,?,?)
                    ''',
                (datetime.datetime.now(), nb_home + nb_away, 'successfully inserted'))
except Exception as e:
    cur.execute('''
        INSERT INTO log_inserted_results (
                created_at, nb_of_lines_inserted, error_message) VALUES 
                (?,?,?)
                ''',
                (datetime.datetime.now(), -1, str(e)))

con.commit()
#print(cur.rowcount)

con.close()
driver.close()

'''
bsando
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
git remote add origin https://github.com/brankasando/testbsa.git

'''

# da namestim da je datum int, ali prvo da ide mesec, da stavim i godinu - DONE
# da kazem da se puni tabela results sa onim rezultatima ciji je datum igranja veci od max-imuma u tabeli - HOCU DA
# PUNI SVE ODJENOM, NE RED PO RED, da bih mogla da logujem gresku ako nece - DONE
# mozda za u svaku tabelu ubacim i created_at -DONE
# da napravim log tabelu koja ce da zapamti svaki put na koji datum koliko se napunilo i koju tabelu -DONE

# try and catch?
# Once the error occurs, you cannot continue -

# da napravim scheduler da okine pajton skripu ujutru i da dopise nove rezultate
# da kreiram tabelu koja sa raporedom za koju treba da izracunam kvote
