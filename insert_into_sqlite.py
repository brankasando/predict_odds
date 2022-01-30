import sqlite3

con = sqlite3.connect('bets.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE results
             (  
               game_id,
               team text,
               sport text,
               league text,
               country text,
               goal int,
               is_home int
              )''')
id = 1
team_home = 'a'
goal_home = 1
cur.execute('''
        INSERT INTO results (game_id, team, sport, league, country, goal, is_home) VALUES(?,?,?,?,?,?,?)
    ''',(
        id, team_home, 'Hokey', 'DEL', 'Germany', goal_home, 1
    ))
con.commit()

con.close()
