from seleniumwire import webdriver
from bs4 import BeautifulSoup
url = "https://www.rezultati.com/hokej/sad/nhl/tablica"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
referer = "https://d.rezultati.com/x/feed/proxy-fetch"

options = webdriver.ChromeOptions()
#options.headless = True


def interceptor(request):
    del request.headers["user-agent"]  # Delete the header first
    request.headers["user-agent"] = user_agent
   # request.headers["sec-ch-ua"] = sec_ch_ua
    request.headers["referer"] = referer
    request.headers["x-fsign"]= "SW9D1eZo"


with webdriver.Chrome(options=options) as driver:
    driver.request_interceptor = interceptor
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html")
    soup = BeautifulSoup(driver.page_source, features="html.parser")