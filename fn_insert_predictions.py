import sqlite3
import pandas as pd

con = sqlite3.connect('bets.db')
cur = con.cursor()


#cur.execute(
q =   '''
with per_game as (
        select r.game_id,
        sum(r.goal - r.is_winner * r.is_extra_time) as goals_all_per_game
    from results r
    inner join games g on r.game_id = g.id
    where g.country = 'norveska' 
    group by game_id
), 

fixed_goal as (
    select 
        r.game_id, 
        r.team,
        r.is_home,
        g.goals_all_per_game, 
        r.goal - r.is_winner * r.is_extra_time as nb_goals_fixed,
        row_number() over (partition by r.team order by r.year_month_day desc) as rn

    from
    results r
    inner join per_game g on r.game_id = g.game_id
),

goals_per_team as (
select 
    team, 
    is_home,
    count(*)                                                  as nb_games_all, 
    sum(case when is_home = 1 then 1 else 0 end)              as nb_games_home,
    sum(case when is_home = 0 then 1 else 0 end)              as nb_games_away,
    
    sum(goals_all_per_game)                                     as nb_goals_all_per_game, 
    
    sum(nb_goals_fixed)                                         as nb_goals_all_plus, /*how many goals team gives overall*/
    sum(goals_all_per_game) - sum(nb_goals_fixed)               as nb_goals_all_minus,/*how many goals team receives overall*/
    
    sum(case when is_home = 1 then nb_goals_fixed else 0 end)                                                                   as nb_goals_home_plus, /* how many goals team gives as host*/
    sum(case when is_home = 1 then goals_all_per_game else 0 end) - sum(case when is_home = 1 then nb_goals_fixed else 0 end)   as nb_goals_home_minus,/* how many goals team receives as host*/

    sum(case when is_home = 0 then nb_goals_fixed else 0 end)                                                                 as nb_goals_away_plus, /* how many goals team gives as away*/
    sum(case when is_home = 0 then goals_all_per_game else 0 end) - sum(case when is_home = 0 then nb_goals_fixed else 0 end) as nb_goals_away_minus /* how many goals team receives as away*/
from 
fixed_goal
/*where team = 'Sandnes'*/
group by team
),

over_0_5 as (
select
    team,
    '0.5' as over,
    sum(case when goals_all_per_game > 0.5 then 1 else 0 end)                        as nb_games_over_all,
    sum(case when goals_all_per_game > 0.5 and is_home = 1 then 1 else 0 end)        as nb_games_over_home,
    sum(case when goals_all_per_game > 0.5 and is_home = 0 then 1 else 0 end)        as nb_games_over_away,
    case when goals_all_per_game     > 0.5 and rn <= 6 then 1 else 0 end             as nb_games_over_all_last_6 /*dao golova ili je dato golova?*/
from 
fixed_goal
group by team
),

over_1_5 as (
select
    team,
    '1.5' as over,
    sum(case when goals_all_per_game > 1.5 then 1 else 0 end)                        as nb_games_over_all,
    sum(case when goals_all_per_game > 1.5 and is_home = 1 then 1 else 0 end)        as nb_games_over_home,
    sum(case when goals_all_per_game > 1.5 and is_home = 0 then 1 else 0 end)        as nb_games_over_away,
    case when goals_all_per_game     > 1.5 and rn <= 6 then 1 else 0 end             as nb_games_over_all_last_6 /*dao golova ili je dato golova?*/
from 
fixed_goal
group by team
),

over_2_5 as (
select
    team,
    '2.5' as over,
    sum(case when goals_all_per_game > 2.5 then 1 else 0 end)                        as nb_games_over_all,
    sum(case when goals_all_per_game > 2.5 and is_home = 1 then 1 else 0 end)        as nb_games_over_home,
    sum(case when goals_all_per_game > 2.5 and is_home = 0 then 1 else 0 end)        as nb_games_over_away,
    case when goals_all_per_game     > 2.5 and rn <= 6 then 1 else 0 end             as nb_games_over_all_last_6 /*dao golova ili je dato golova?*/
from 
fixed_goal
group by team
),

over_3_5 as (
select
    team,
    '3.5' as over,
    sum(case when goals_all_per_game > 3.5 then 1 else 0 end)                        as nb_games_over_all,
    sum(case when goals_all_per_game > 3.5 and is_home = 1 then 1 else 0 end)        as nb_games_over_home,
    sum(case when goals_all_per_game > 3.5 and is_home = 0 then 1 else 0 end)        as nb_games_over_away,
    case when goals_all_per_game     > 3.5 and rn <= 6 then 1 else 0 end             as nb_games_over_all_last_6 /*dao golova ili je dato golova?*/
from 
fixed_goal
group by team
),


over_4_5 as (
select
    team,
    '4.5' as over,
    sum(case when goals_all_per_game > 4.5 then 1 else 0 end)                        as nb_games_over_all,
    sum(case when goals_all_per_game > 4.5 and is_home = 1 then 1 else 0 end)        as nb_games_over_home,
    sum(case when goals_all_per_game > 4.5 and is_home = 0 then 1 else 0 end)        as nb_games_over_away,
    case when goals_all_per_game     > 4.5 and rn <= 6 then 1 else 0 end             as nb_games_over_all_last_6 /*dao golova ili je dato golova?*/
from 
fixed_goal
group by team
),


over_5_5 as (
select
    team,
    '5.5' as over,
    sum(case when goals_all_per_game > 5.5 then 1 else 0 end)                        as nb_games_over_all,
    sum(case when goals_all_per_game > 5.5 and is_home = 1 then 1 else 0 end)        as nb_games_over_home,
    sum(case when goals_all_per_game > 5.5 and is_home = 0 then 1 else 0 end)        as nb_games_over_away,
    case when goals_all_per_game     > 5.5 and rn <= 6 then 1 else 0 end             as nb_games_over_all_last_6 /*dao golova ili je dato golova?*/
from 
fixed_goal
group by team
),


over_6_5 as (
select
    team,
    '6.5' as over,
    sum(case when goals_all_per_game > 6.5 then 1 else 0 end)                        as nb_games_over_all,
    sum(case when goals_all_per_game > 6.5 and is_home = 1 then 1 else 0 end)        as nb_games_over_home,
    sum(case when goals_all_per_game > 6.5 and is_home = 0 then 1 else 0 end)        as nb_games_over_away,
    case when goals_all_per_game     > 6.5 and rn <= 6 then 1 else 0 end             as nb_games_over_all_last_6 /*dao golova ili je dato golova?*/
from 
fixed_goal
group by team
),


over_7_5 as (
select
    team,
    '7.5' as over,
    sum(case when goals_all_per_game > 7.5 then 1 else 0 end)                        as nb_games_over_all,
    sum(case when goals_all_per_game > 7.5 and is_home = 1 then 1 else 0 end)        as nb_games_over_home,
    sum(case when goals_all_per_game > 7.5 and is_home = 0 then 1 else 0 end)        as nb_games_over_away,
    case when goals_all_per_game     > 7.5 and rn <= 6 then 1 else 0 end             as nb_games_over_all_last_6 /*dao golova ili je dato golova?*/
from 
fixed_goal
group by team
),

over_8_5 as (
select
    team,
    '8.5' as over,
    sum(case when goals_all_per_game > 8.5 then 1 else 0 end)                        as nb_games_over_all,
    sum(case when goals_all_per_game > 8.5 and is_home = 1 then 1 else 0 end)        as nb_games_over_home,
    sum(case when goals_all_per_game > 8.5 and is_home = 0 then 1 else 0 end)        as nb_games_over_away,
    case when goals_all_per_game     > 8.5 and rn <= 6 then 1 else 0 end             as nb_games_over_all_last_6 /*dao golova ili je dato golova?*/
from 
fixed_goal
group by team
),

union_over as (
 
select * from over_0_5 
union all
select * from over_1_5 
union all
select * from over_2_5 
union all
select * from over_3_5 
union all
select * from over_4_5 
union all
select * from over_5_5 
union all
select * from over_6_5
union all
select * from over_7_5 
union all
select * from over_8_5 
),

all_statistics as (
select 
    sg.id, 
    sg.year_month_day,
    sg.team, 
    sg.is_home,
    gpt.nb_games_all,
    gpt.nb_games_home,
    gpt.nb_games_away,
    gpt.nb_goals_all_per_game,
    gpt.nb_goals_all_plus,
    gpt.nb_goals_all_minus,
    gpt.nb_goals_home_plus,
    gpt.nb_goals_home_minus,
    gpt.nb_goals_away_plus,
    gpt.nb_goals_away_plus,
    uo.over,
    uo.nb_games_over_all,
    uo.nb_games_over_home,
    uo.nb_games_over_away,
    uo.nb_games_over_all_last_6
from 
scheduled_games sg
inner join goals_per_team gpt on gpt.team = sg.team 
inner join union_over uo on uo.team = sg.team
where sg.is_current = 1
)

select
    id as game_id, 
    over, 
   -- year_month_day,
    max(case when is_home = 1 then team end) as team_home, 
    max(case when is_home = 0 then team end) as team_away, 
    --max(case when is_home = 1 then nb_games_over_all end)*1.00000/max(case when is_home = 1 then nb_games_all end) as p1,
    --max(case when is_home = 0 then nb_games_over_all end)*1.00000/max(case when is_home = 1 then nb_games_all end) as prediction_1,
    ((sum((1.00000*nb_games_over_all/nb_games_all)*100)/2) +
    ((sum(iif(is_home = 1, (1.00000*nb_games_over_home/nb_games_home)*100,0)) +
    sum(iif(is_home = 0, (1.00000*nb_games_over_away/nb_games_away)*100,0)))/2))/2 as formula,
    100 /  (((sum((1.00000*nb_games_over_all/nb_games_all)*100)/2) +
    ((sum(iif(is_home = 1, (1.00000*nb_games_over_home/nb_games_home)*100,0)) +
    sum(iif(is_home = 0, (1.00000*nb_games_over_away/nb_games_away)*100,0)))/2))/2) as kvota

   -- 100 / (sum(nb_games_over_all/nb_games_all + is_home*nb_games_over_home*1.00000/nb_games_home + iif(is_home=0,1,0)*nb_games_over_away*1.00000*nb_games_away)/4 ) as kvota_1
from
all_statistics
group by id, over
order by team_home


'''

db_df = pd.read_sql_query(q, con)
pd.options.display.max_columns = None
pd.options.display.max_rows = None
print(db_df)

#records = cur.fetchall()

#print(records)

con.close()