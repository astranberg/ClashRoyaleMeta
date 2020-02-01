import sqlite3

print('=' * 20, 'CLEANING DATABASE OF LOW-LEVEL PLAYERS', '=' * 20)
conn = sqlite3.connect('clans.db')
cursor = conn.cursor()
###########################
before = len([_ for _ in cursor.execute('SELECT * FROM battles')])
sql_query_player = 'SELECT winner_tag FROM battles WHERE winner_trophies BETWEEN 0 AND 4200 OR loser_trophies BETWEEN 0 AND 4200'
cursor.execute("""DELETE from players
                WHERE player_tag IN (%s)""" % sql_query_player)
conn.commit()
after = len([_ for _ in cursor.execute('SELECT * FROM battles')])
print('Deleted %s low-level players. There are now %s remaining' % (after - before, str(after) + '/' + str(before)))
###########################
before = after
cursor.execute("""DELETE from battles
                WHERE datetime(battle_time) < datetime('now', '-7 Day')""")
conn.commit()
after = len([_ for _ in cursor.execute('SELECT * FROM battles')])
print('Deleted %s low-level players. There are now %s remaining' % (after - before, str(after) + '/' + str(before)))
###########################
cursor.close()
conn.close()
