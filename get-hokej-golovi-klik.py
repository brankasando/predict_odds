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
driver.get("https://www.rezultati.com/")

soup = BeautifulSoup(driver.page_source, "html")
soup = BeautifulSoup(driver.page_source, features="html.parser")
#id = soup.find(id="tournament-table-tabs-and-content")
#broj_golova = id.find_all('a', href=True)
#broj_golova.click()
#print(broj_golova)
#bg=driver.find_element(By.CLASS_NAME, "tabs__text tabs__text--default").click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
#tabs__text tabs__text--default
#onetrust-accept-btn-handler
#elements=WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "tabs__text tabs__text--default")))
elements = driver.find_element(By.XPATH,"@class='tabs__text tabs__text--default'")[2]
print(elements)
driver.close()
'''
'''