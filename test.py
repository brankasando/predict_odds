import datetime
import time
import sqlite3
import os

#print('/' + os.getcwd()+ 'a')

con = sqlite3.connect('bets.db')
cur = con.cursor()

try:
    cur.execute("insert into test_table values (1, 2, 3)")
    cur.execute("insert into test_table values (5, 50)")

except Exception as e:
    print(str(e))


con.commit()
con.close()

