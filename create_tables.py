import sqlite3

con = sqlite3.connect('bets.db')
cur = con.cursor()


cur.execute('''CREATE TABLE scheduled_games
             (  
               id text,
               sport text,
               league text,
               country text,
               year_month_day int,
               team text,
               is_home int,
               created_at timestamp,
               
               constraint pk_scheduled_games primary key (id, is_home)
              )''')
con.commit()
con.close()
