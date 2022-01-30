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

new_ids = []


con = sqlite3.connect('bets.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE results
             (  
               game_id,
               team text,
               sport text,
               league text,
               country text,
               goal int,
               is_home int
              )''')
for id in ids:
    results = soup.find(id=id)
    t = results.find("div", class_="event__time")
    #if t.text[0:6] == '21.01.':
    new_ids.append(id)

#print(new_ids)

for id in new_ids:
    results = soup.find(id=id)
    team_home = results.find("div", class_=lambda s: "event__participant event__participant--home" in s)
    team_away = results.find("div", class_=lambda s: "event__participant event__participant--away" in s)
    goal_home = results.find("div", class_="event__score event__score--home")
    goal_away = results.find("div", class_="event__score event__score--away")
    #t = results.find("div", class_="event__time").text
    print(id)
    print(team_away)
    print(team_home)
    print(goal_home)
    print(goal_away)
    print('----------------------')
    cur.execute('''
        INSERT INTO results (
                game_id, team, sport, league, country, goal, is_home) VALUES 
                (?,?,?,?,?,?,?)
                ''',
                (id, team_home, 'Hokey', 'DEL', 'Germany', goal_home, 1))
    con.commit()
    cur.execute('''
        INSERT INTO results (
                game_id, team, sport, league, country, goal, is_home) VALUES 
                (?,?,?,?,?,?,?)
                ''',
                (id, team_away, 'Hokey', 'DEL', 'Germany', goal_away, 0))
    con.commit()

con.close()
driver.close()
'''
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
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
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
git remote add origin https://github.com/brankasando/testbsa.git

'''
