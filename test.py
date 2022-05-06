import datetime
import time
import sqlite3


con = sqlite3.connect('bets.db')
cur = con.cursor()

# sqlite allows primary key column to contain NULL values
# Create table

try:
    cur.execute(
    '''  
    insert into test_table
    values
    (4,d) 
    ''')

    cur.execute(
    '''  
    insert into test_table
    values
    (5,50) 
    ''')

except Exception as e:
   print(e)

con.commit()
con.close()