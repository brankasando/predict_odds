# ideja:
# proveri da li datum postoji u bazi
# ako ne, onda uzmi za sve datume od tog datum rezultate i upisi u bazu

def insert_new_results(website_url):

    website_url_elements = website_url.split("/")

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
    import os

    options = Options()
    # options.binary_location = "//usr/bin/chrome.exe"    #chrome binary location specified here
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")  # open Browser in maximized mode
    options.add_argument("--no-sandbox")  # bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.headless = True

    ser = Service("/"+os.getcwd()+"/chromedriver.exe")
    driver = webdriver.Chrome(options=options, service=ser)
    driver.get(website_url)

    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()

    soup = BeautifulSoup(driver.page_source, "html")
    soup = BeautifulSoup(driver.page_source, features="html.parser")


    season_year_txt = soup.find("div", class_="heading__info").text

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

    max_date = cur.execute(
        ''' select max(r.year_month_day) 
        from results r 
        inner join games g on g.id = r.game_id
        where 
        g.sport = ? and g.league = ? and g.country = ? ''',
        (website_url_elements[3], website_url_elements[5], website_url_elements[4])
    )
    # use list() to get the details other than the cursor object.
    # max_date je bio cursor objekat, sa list vraca tuple
    max_date = list(max_date)[0][0]
    # print(max_date)
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
        goal_home_int = int(goal_home.text)
        goal_away = results.find("div", class_="event__score event__score--away")
        goal_away_int = int(goal_away.text)
        year_month_day_time = results.find("div", class_="event__time")
        extra_time = results.find("div", class_="event__stage--block")
        extra_time_bit = 0 if extra_time is None else 1

        if year_month_day_time.text[3:5] in ['08','09', '10', '11', '12']:
            year_month_day = '2021' + year_month_day_time.text[3:5] + year_month_day_time.text[:2]
        else:
            year_month_day = '2022' + year_month_day_time.text[3:5] + year_month_day_time.text[:2]
        year_month_day = int(year_month_day)
                                #sport                  league                  country
        games_list.append((id, website_url_elements[3], website_url_elements[5], website_url_elements[4], season_year_txt, 1, datetime.datetime.now()))

        results_home_list.append((id, year_month_day, team_home.text, goal_home_int, 1,
                                  1 if goal_home_int > goal_away_int else 0, extra_time_bit, datetime.datetime.now()))
        results_away_list.append((id, year_month_day, team_away.text, goal_away_int, 0,
                                  1 if goal_home_int < goal_away_int else 0, extra_time_bit, datetime.datetime.now()))

    #print(games_list)
    #print(results_home_list)
    #print(results_away_list)

    try:

        cur.executemany('''
        INSERT INTO games 
            (
                id, sport, league, country, season_year, is_season_active, created_at
            ) VALUES 
                (?,?,?,?,?,?,?)
                ''',
                        games_list)
        nb = cur.rowcount
        cur.execute('''
                    INSERT INTO log_inserted_games 
                    (
                        created_at, nb_of_lines_inserted, error_message, inserted_by
                    ) VALUES
                      (?,?,?,?)
                       ''',
                    (datetime.datetime.now(), nb, 'successfully inserted', 'fn_insert_new_results'))


    except Exception as e:

        cur.execute('''
            INSERT INTO log_inserted_games 
            (
                created_at, nb_of_lines_inserted, error_message, inserted_by
            ) VALUES 
              (?,?,?,?)
              ''',
                    (datetime.datetime.now(), -1, str(e), 'fn_insert_new_results'))

    con.commit()

    try:
        cur.executemany('''
        INSERT INTO results (
                game_id, year_month_day, team, goal, is_home, is_winner, is_extra_time, created_at) VALUES 
                (?,?,?,?,?,?,?,?)
                ''',
                results_home_list)
        nb_home = cur.rowcount

        cur.executemany('''
        INSERT INTO results (
                game_id, year_month_day, team, goal, is_home, is_winner, is_extra_time, created_at) VALUES
                (?,?,?,?,?,?,?,?)
                ''',
                results_away_list)
        nb_away = cur.rowcount

        cur.execute('''
                INSERT INTO log_inserted_results (
                        created_at, nb_of_lines_inserted, error_message, inserted_by) VALUES
                        (?,?,?,?)
                        ''',
                    (datetime.datetime.now(), nb_home + nb_away, 'successfully inserted', 'fn_insert_new_results'))
    except Exception as e:
        cur.execute('''
            INSERT INTO log_inserted_results (
                    created_at, nb_of_lines_inserted, error_message, inserted_by) VALUES 
                    (?,?,?,?)
                    ''',
                    (datetime.datetime.now(), -1, str(e), 'fn_insert_new_results'))

    con.commit()
    # print(cur.rowcount)

    con.close()
    driver.close()

    '''
    bsando
    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
    git remote add origin https://github.com/brankasando/testbsa.git

    '''
    print("Done!")