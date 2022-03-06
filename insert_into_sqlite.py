import sqlite3

con = sqlite3.connect('bets.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE results1
             (  
               game_id text,
               day_month text,
               team text,
               goal int,
               is_home int,

               constraint pk_results_day_month_team primary key (day_month, team),
               constraint fk_results_game_id foreign key (game_id) references games (id)

              )''')

con.commit()

con.close()

