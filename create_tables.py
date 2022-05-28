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
               created_at timestamp not null

              )''')

#sqlite allows primary key column to contain NULL values
#Create table


cur.execute('''CREATE TABLE games
             (
               id text not null,
               sport text not null,
               league text not null,
               country text not null,
               season_year text not null,
               is_season_active bit not null default 1,
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



cur.execute('''CREATE TABLE predictions
             (
               game_id text not null,
               year_month_day int not null,
               over float not null,
               team_home text not null,
               team_away text not null,
               odds_last_6 float, 

               avg_goal_team_home_plus float, 
               avg_goal_team_home_minus float, 
               avg_goal_team_away_plus float, 
               avg_goal_team_away_minus float, 

               avg_goal float float, 

               is_current bit not null,
               created_at timestamp not null   
              )''')


con.commit()
con.close()

