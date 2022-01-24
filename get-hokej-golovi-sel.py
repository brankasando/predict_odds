from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

options = Options()
# options.binary_location = "//usr/bin/chrome.exe"    #chrome binary location specified here
options.add_argument("--headless")
options.add_argument("--start-maximized")  # open Browser in maximized mode
options.add_argument("--no-sandbox")  # bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.headless = True

ser = Service("//home/branka/web_sracp2/chromedriver.exe")
driver = webdriver.Chrome(options=options, service=ser)
driver.get("https://www.rezultati.com/hokej/njemacka/del/rezultati/")

soup = BeautifulSoup(driver.page_source, "html")
soup = BeautifulSoup(driver.page_source, features="html.parser")
div_tags = soup.find_all('div')
ids = []
for div in div_tags:
     id = div.get('id')
     if id is not None and id[0] == 'g':
         ids.append(id)

new_ids = []

for id in ids:
    results = soup.find(id=id)
    t = results.find("div", class_="event__time")
    if t.text[0:6] == '21.01.':
        new_ids.append(id)

print(new_ids)

for id in new_ids:
    results = soup.find(id=id)
    team_home = results.find("div", class_=lambda s: "event__participant event__participant--home" in s)
    team_away = results.find("div", class_=lambda s: "event__participant event__participant--away" in s)
    goal_home = results.find("div", class_="event__score event__score--home")
    goal_away = results.find("div", class_="event__score event__score--away")
    print(team_home.text + ": " + goal_home.text+ ":" + id)
    print(team_away.text + ": " + goal_away.text)

driver.close()
'''
'''