# pip3 install flask-sqlachemy in terminal

from flask import Flask, render_template, request #iz flask biblioteke importujemo flask objekat
import sqlite3

app = Flask(__name__) #zovemo flask konsturktor, ovo __name__ referencuje ovaj fajl


@app.route('/predictions', methods=['GET','POST'])
def show_predicions():

    con = sqlite3.connect('/home/branka/web_sracp2/bets.db')
    cur = con.cursor()

    # uzmi sport
    cur.execute(
        '''
        select 'All' as sport
        union
        select distinct sport from games 
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
        select distinct league from games 
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
        select country league from games 
        ''')
    ddl_fetched_country = cur.fetchall()

    country_value = request.args.get('country')

    if country_value is None:
        country_value = 'All'



    cur.execute(
        '''
        select  
            g.sport as sport, 
            g.league as league,
            g.country as country,
            p.year_month_day as year_month_day, 
            p.over as over, 
            p.team_home as team_home,
            p.team_away as team_away,
            round(p.odds_last_6, 5) as odds_last_6,
            round(p.avg_goal, 5) as avg_goal   
        from 
        games g
        inner join predictions p on p.game_id = g.id
        where 
        (g.sport = ? or 'All' = ?) and
        (g.league = ? or 'All' = ?) and
        (g.country = ? or 'All' = ?) and
        odds_last_6 is not null
        order by 
            g.sport,
            g.league,
            p.year_month_day, 
            p.over
        ''',
        (sport_value, sport_value, league_value, league_value, country_value, country_value) )
    rows_fetched= cur.fetchall()

    return render_template \
            (
            'predictions.html',
            ddl_sport=ddl_fetched_sport,
            ddl_league=ddl_fetched_league,
            ddl_country=ddl_fetched_country,
            rows=rows_fetched,
            sport_value=sport_value,
            league_value = league_value,
            country_value=country_value
        )


if __name__ == "__main__":
    app.run(debug=True) #ako zovemo program iz komande linije da ukljuci debug mode