import sqlite3

con = sqlite3.connect('bets.db')
cur = con.cursor()


cur.execute(
    '''
    with 
    goal_per_game as (
        select *, 
        sum(goal) over (partition by game_id) as goal_per_game
        from results 
        )
    
    select s.* 
    from 
    scheduled_games s
    inner join goal_per_game g on s.team = g.team and s.is_home = g.is_home 
    '''
)

records = cur.fetchall()

print("Total rows are:  ", len(records))
print("Printing each row")
for row in records:
    print("Id: ", row[0])
    print("Name: ", row[1])
    print("Email: ", row[2])
    print("Salary: ", row[3])
    print("Salary: ", row[4])
    print("Salary: ", row[5])
    print("Salary: ", row[6])
    print("Salary: ", row[7])


    print("\n")

cur.close()

print(cur)
con.close()
