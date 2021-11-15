import sqlite3
import globals

globals.init()

conn = sqlite3.connect(globals.databasename)
cursor = conn.cursor()

print('=' * 20, 'OBTAINING STATISTICS', '=' * 20)

num_clans = len([_ for _ in cursor.execute('SELECT * FROM clans')])
print('Database contains %s clans.' % (num_clans))

num_players = len([_ for _ in cursor.execute('SELECT * FROM players')])
print('Database contains %s players.' % (num_players))

num_battles = len([_ for _ in cursor.execute('SELECT * FROM battles')])
print('Database contains %s battles.' % (num_battles))

# by trophy range
num_players = len(
    [_ for _ in cursor.execute('SELECT * FROM players WHERE CAST(max_trophies as int) < 0 OR max_trophies IS NULL')])
print('There are %s players with unknown trophies.' % (num_players))
step = 500
for trophies in range(0, 10000, step):
    num_players = len([_ for _ in cursor.execute(
        'SELECT * FROM players WHERE CAST(max_trophies as int) BETWEEN %s AND %s' % (trophies, trophies + step - 1))])
    print('There are %s players in trophy range %s-%s.' % (num_players, trophies, trophies + step - 1))
