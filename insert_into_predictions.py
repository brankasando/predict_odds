import sqlite3

con = sqlite3.connect('bets.db')
cur = con.cursor()


cur.execute(
    '''
with per_game as (
        select game_id,
        sum(goal - is_winner*is_extra_time) as goal_all
    from results group by game_id
)
select t.team,
count(*) as all_nb_games,
sum(case when is_home = 1 then 1 else 0 end) as home_nb_games, 
sum(case when is_home = 0 then 1 else 0 end) as away_nb_games, 
sum(goal - is_winner*is_extra_time) as all_nb_goals,
sum(case when g.goal_all > 1.5 then 1 else 0 end) over_all_1_5,
sum(case when g.goal_all > 2.5 then 1 else 0 end) over_all_2_5,
sum(case when g.goal_all > 3.5 then 1 else 0 end) over_all_3_5,
sum(case when g.goal_all > 4.5 then 1 else 0 end) over_all_4_5,
sum(case when g.goal_all > 5.5 then 1 else 0 end) over_all_5_5,
sum(case when g.goal_all > 6.5 then 1 else 0 end) over_all_6_5,
sum(case when g.goal_all > 7.5 then 1 else 0 end) over_all_7_5,
sum(case when g.goal_all > 8.5 then 1 else 0 end) over_all_8_5,


sum(case when g.goal_all > 1.5 and is_home = 1 then 1 else 0 end) over_home_1_5,
sum(case when g.goal_all > 2.5 and is_home = 1 then 1 else 0 end) over_home_2_5,
sum(case when g.goal_all > 3.5 and is_home = 1 then 1 else 0 end) over_home_3_5,
sum(case when g.goal_all > 4.5 and is_home = 1 then 1 else 0 end) over_home_4_5,
sum(case when g.goal_all > 5.5 and is_home = 1 then 1 else 0 end) over_home_5_5,
sum(case when g.goal_all > 6.5 and is_home = 1 then 1 else 0 end) over_home_6_5,
sum(case when g.goal_all > 7.5 and is_home = 1 then 1 else 0 end) over_home_7_5,
sum(case when g.goal_all > 8.5 and is_home = 1 then 1 else 0 end) over_home_8_5,


sum(case when g.goal_all > 1.5 and is_home = 0 then 1 else 0 end) over_away_1_5,
sum(case when g.goal_all > 2.5 and is_home = 0 then 1 else 0 end) over_away_2_5,
sum(case when g.goal_all > 3.5 and is_home = 0 then 1 else 0 end) over_away_3_5,
sum(case when g.goal_all > 4.5 and is_home = 0 then 1 else 0 end) over_away_4_5,
sum(case when g.goal_all > 5.5 and is_home = 0 then 1 else 0 end) over_away_5_5,
sum(case when g.goal_all > 6.5 and is_home = 0 then 1 else 0 end) over_away_6_5,
sum(case when g.goal_all > 7.5 and is_home = 0 then 1 else 0 end) over_away_7_5,
sum(case when g.goal_all > 8.5 and is_home = 0 then 1 else 0 end) over_away_8_5

from results t
inner join  per_game g on t.game_id = g.game_id group by t.team;
    '''
)

records = cur.fetchall()

print(records)

con.close()