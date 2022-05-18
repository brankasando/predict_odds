import datetime
import time
import sqlite3
import os

print('/' + os.getcwd()+ 'a')

# con = sqlite3.connect('bets.db')
# cur = con.cursor()
#
# # sqlite allows primary key column to contain NULL values
# # Create table
#
# over_list = [1.5, 2.5, 3.5, 4.5]
# over_tupple = tuple(over_list)
#
# team_home = "Manchester Utd"
# cur.execute("select * from predictions where team_home = ? and over in {} ".format(over_tupple), (team_home,))
# rows_fetched = cur.fetchall()
# print(rows_fetched)
#
# con.commit()
# con.close()

