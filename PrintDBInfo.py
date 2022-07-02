import sqlite3
import globals

globals.init()

conn = sqlite3.connect(globals.databasename)
cursor = conn.cursor()

print('=' * 20, 'OBTAINING STATISTICS', '=' * 20)

num_clans = [i for i in cursor.execute('SELECT coalesce(MAX(ROWID)+1, 0) FROM clans')][0][0]
print('Database contains %s clans.' % (num_clans))

num_players = [i for i in cursor.execute('SELECT coalesce(MAX(ROWID)+1, 0) FROM players')][0][0]
print('Database contains %s players.' % (num_players))

num_battles = [i for i in cursor.execute('SELECT coalesce(MAX(ROWID)+1, 0) FROM battles')][0][0]
print('Database contains %s battles.' % (num_battles))

# print battle types
battle_types = [x for x in cursor.execute('SELECT DISTINCT battle_type FROM battles')]
bt = 'Battle types: '
for types in battle_types:
    bt += types[0] + ', '

print(bt)

# by trophy range
num_players = len(
    [_ for _ in cursor.execute('SELECT * FROM players WHERE CAST(max_trophies as int) < 0 OR max_trophies IS NULL')])
print('There are %s players with unknown trophies.' % (num_players))
step = 500
for trophies in range(0, 10000, step):
    num_players = len([_ for _ in cursor.execute(
        'SELECT * FROM players WHERE CAST(max_trophies as int) BETWEEN %s AND %s' % (trophies, trophies + step - 1))])
    print('There are %s players in trophy range %s-%s.' % (num_players, trophies, trophies + step - 1))
