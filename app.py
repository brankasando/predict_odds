# pip3 install flask-sqlachemy in terminal

from flask import Flask, render_template, request #iz flask biblioteke importujemo flask objekat
import sqlite3
import config_environment as ce

app = Flask(__name__) #zovemo flask konsturktor, ovo __name__ referencuje ovaj fajl

@app.route('/')
def hello():
    return('hello')

@app.route('/predictions', methods=['GET','POST'])
def show_predicions():

    con = sqlite3.connect('bets.db')
    cur = con.cursor()

    # uzmi sport
    cur.execute(
        '''
        select 'All' as sport
        union
        select distinct 'Football' from scheduled_games 
        where is_current = 1 
        ''')
    ddl_fetched_sport = cur.fetchall()

    sport_value = request.args.get('sport')

    if sport_value is None:
        sport_value = 'All'


    # uzmi ligu
    cur.execute(
        '''
        select 'All' as league
        union
        select distinct league from scheduled_games 
        where is_current = 1 
        ''')
    ddl_fetched_league = cur.fetchall()

    league_value = request.args.get('league')

    if league_value is None:
        league_value = 'All'

    # uzmi zemlju
    cur.execute(
        '''
        select 'All' as country
        union
        select distinct
        case 
		when country = 'spanjolska' then 'Spain'
		when country = 'italija' then 'Italy'
		when country = 'engleska' then 'England'
	end as country 
	from scheduled_games 
        where is_current = 1 
        ''')
    ddl_fetched_country = cur.fetchall()

    country_value = request.args.get('country')

    if country_value is None:
        country_value = 'All'

    # uzmi over
    cur.execute(
        '''
        select distinct over from predictions where over is not null 
        ''')
    ddl_fetched_over = cur.fetchall()

    over_value = request.args.getlist('over')
    over_value_tuple = tuple(over_value) # za slanje u sqlite query


    if len(over_value) == 0:
        new_list = [x[0] for x in ddl_fetched_over]
        over_value_tuple = tuple(new_list)
    elif len(over_value) == 1:
        over_value_tuple = (over_value[0],1000) # kada je izabrana jedna vrednost, vraca se u formatu (vrednost,) jer je tupple
        # i potrebna mu je par, zato zadajem lazni par da bi proslo u sql-u


    cur.execute(
        '''
        select distinct
            case when sg.sport = 'nogomet' then 'Football' end  as sport, 
            sg.league as league,
	    case 
            	when sg.country = 'spanjolska' then 'Spain'
		when sg.country = 'italija' then 'Italy'
		when sg.country = 'engleska' then 'England'
	    end as country,
            p.year_month_day as year_month_day, 
            p.over as over, 
            p.team_home as team_home,
            p.team_away as team_away,
            round(p.odds_last_6, 5) as odds_last_6,
            round(p.avg_goal_team_home_plus, 5) as avg_goal_team_home_plus,
            round(p.avg_goal_team_home_minus, 5) as avg_goal_team_home_minus,
            round(p.avg_goal_team_away_plus, 5) as avg_goal_team_away_plus,
            round(p.avg_goal_team_away_minus, 5) as avg_goal_team_away_minus 
        from 
        scheduled_games sg
        inner join predictions p on p.game_id = sg.id and sg.is_current = 1
        where 
        p.is_current = 1 and
        ('Football' = ? or 'All' = ?) and
        (sg.league = ? or 'All' = ?) and
        ('Italy' = ? or 'All' = ?) and
        (p.over in {}) and
        p.odds_last_6 is not null
        order by 
            sg.sport,
            sg.league,
            p.year_month_day, 
            p.team_home,
            p.over
        '''.format(over_value_tuple),
        (sport_value, sport_value, league_value, league_value, country_value, country_value)) #, over_value, over_value
    rows_fetched= cur.fetchall()

    return render_template \
            (
            'predictions.html',
            ddl_sport=ddl_fetched_sport,
            ddl_league=ddl_fetched_league,
            ddl_country=ddl_fetched_country,
            ddl_over=ddl_fetched_over,
            rows=rows_fetched,
            sport_value=sport_value,
            league_value = league_value,
            country_value=country_value
        )

#if __name__ == '__main__':
 #     app.run(host='0.0.0.0', port=80)


if __name__ == "__main__":
    app.run(host=ce.host, port=ce.port) #ako zovemo program iz komande linije da ukljuci debug mode
