import sqlite3

con = sqlite3.connect('bets.db')
cur = con.cursor()

cur.execute('''CREATE TABLE log_inserted_scheduled_games
             (
                created_at timestamp not null,
                nb_of_lines_inserted integer not null,
                error_message text not null,
                inserted_by text
              )''')


# SQLite does not have an official datetime type. Instead, it stores dates and times as TEXT, REAL or INTEGER values using Date and Time Functions.
cur.execute('''CREATE TABLE log_inserted_games
             (
                created_at timestamp not null,
                nb_of_lines_inserted integer not null,
                error_message text not null,
                inserted_by text
              )''')

cur.execute('''CREATE TABLE log_inserted_results
             (
                created_at timestamp not null,
                nb_of_lines_inserted integer not null,
                error_message text not null,
                inserted_by text
              )''')


cur.execute('''CREATE TABLE log_inserted_predictions
             (  
                created_at timestamp not null,
                nb_of_lines_inserted integer not null,
                error_message text not null,
                inserted_by text
              )''')


con.commit()
con.close()