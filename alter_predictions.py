import sqlite3
import config_environment as ce
import os

os.chmod(ce.path_to_db + 'bets.db', 0o777)

con = sqlite3.connect(ce.path_to_db + 'bets.db')
cur = con.cursor()

cur.execute('''

CREATE TABLE if not exists predictions_temporary
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
);

    '''
            )

cur.execute('''
insert into predictions_temporary
(game_id, year_month_day, over, team_home, team_away, odds_last_6, avg_goal, is_current, created_at)
select 
               game_id,
               year_month_day,
               over,
               team_home,
               team_away,
               odds_last_6,   
               avg_goal,
               is_current,
               created_at
from 
predictions
''')

cur.execute('''
drop table predictions;
'''
            )

cur.execute('''
alter table predictions_temporary rename to predictions
'''
            )

con.commit()
con.close()