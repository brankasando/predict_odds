import datetime
import time
import sqlite3

website_url = '"https://www.rezultati.com/hokej/njemacka/del/rezultati/"'
website_url_elements = website_url.split("/")
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
print(website_url_elements[3])
print(website_url_elements[5])
print(website_url_elements[4])

print(max_date)