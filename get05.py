from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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
driver.get("https://www.rezultati.com/hokej/njemacka/del/tablica/")


#id = soup.find(id="tournament-table-tabs-and-content")
#broj_golova = id.find_all('a', href=True)
#broj_golova.click()
#print(broj_golova)
#bg=driver.find_element(By.CLASS_NAME, "tabs__text tabs__text--default").click()
#tabs__text tabs__text--default
#onetrust-accept-btn-handler
driver.implicitly_wait(5)

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
WebDriverWait(driver, 360).until(EC.element_to_be_clickable((By.LINK_TEXT, "Broj Golova"))).click()
WebDriverWait(driver, 360).until(EC.element_to_be_clickable((By.LINK_TEXT, "0.5"))).click()

#window_after = driver.window_handles[1]
#driver.switch_to.window(window_after)


#driver.close()
'''
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
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
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
git remote add origin https://github.com/brankasando/testbsa.git

'''
