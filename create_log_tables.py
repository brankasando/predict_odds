import sqlite3

con = sqlite3.connect('bets.db')
cur = con.cursor()

# SQLite does not have an official datetime type. Instead, it stores dates and times as TEXT, REAL or INTEGER values using Date and Time Functions.
cur.execute('''CREATE TABLE log_inserted_games
             (  
                created_at timestamp,
                nb_of_lines_inserted integer,
                error_message text
              )''')

cur.execute('''CREATE TABLE log_inserted_results
             (  
                created_at timestamp,
                nb_of_lines_inserted integer,
                error_message text
              )''')

cur.execute('''CREATE TABLE log_inserted_scheduled_games
             (  
                created_at timestamp,
                nb_of_lines_inserted integer,
                error_message text
              )''')


con.commit()
con.close()