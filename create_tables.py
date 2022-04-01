import sqlite3

con = sqlite3.connect('bets.db')
cur = con.cursor()


cur.execute('''CREATE TABLE scheduled_games
             (  
               id text not null,
               sport text not null,
               league text not null,
               country text not null,
               year_month_day int not null,
               team text not null,
               is_home bit not null,
               is_current bit not null,
               created_at timestamp not null,
               
               constraint pk_scheduled_games primary key (id, is_home)
              )''')

# sqlite allows primary key column to contain NULL values
# Create table


cur.execute('''CREATE TABLE games
             (  
               id text not null,
               sport text not null,
               league text not null,
               country text not null,
               created_at timestamp not null,

               constraint pk_games_id primary key (id)
              )''')

cur.execute('''CREATE TABLE results
             (  
               game_id text not null,
               year_month_day int not null,
               team text not null,
               goal int not null,
               is_home bit not null,
               is_winner bit not null,
               is_extra_time bit null,
               created_at timestamp not null,

               constraint pk_results_year_month_day_team primary key (year_month_day, team),
               constraint fk_results_game_id foreign key (game_id) references games (id)
              )''')



con.commit()
con.close()
