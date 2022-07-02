import sqlite3
import globals

globals.init()

print('=' * 20, 'CLEANING DATABASE', '=' * 20)
conn = sqlite3.connect(globals.databasename)
cursor = conn.cursor()
###########################
# before = len([_ for _ in cursor.execute('SELECT * FROM players')])
# sql_query_player = "SELECT winner_tag FROM battles WHERE winner_trophies BETWEEN 0 AND 5200 AND battle_type like 'Ladde%'"
# cursor.execute("""DELETE from players
#                WHERE player_tag IN (%s)""" % sql_query_player)
# conn.commit()
after = len([_ for _ in cursor.execute('SELECT * FROM players')])
# print('Deleted %s low-level winners. There are now %s players remaining' % (before - after, str(after) + '/' + str(before)))
###########################
# before = len([_ for _ in cursor.execute('SELECT * FROM players')])
# sql_query_player = 'SELECT loser_tag FROM battles WHERE loser_trophies BETWEEN 0 AND 5200 AND battle_type like 'Ladde%''
# cursor.execute("""DELETE from players
#                WHERE player_tag IN (%s)""" % sql_query_player)
# conn.commit()
# after = len([_ for _ in cursor.execute('SELECT * FROM players')])
# print('Deleted %s low-level losers. There are now %s players remaining' % (before - after, str(after) + '/' + str(before)))
###########################
# before = len([_ for _ in cursor.execute('SELECT * FROM players')])
# cursor.execute("""DELETE from players
#                WHERE CAST(max_trophies AS INTEGER) < 5200
#                AND CAST(max_trophies AS INTEGER) > 100
#                AND max_trophies NOT NULL""")
# conn.commit()
# after = len([_ for _ in cursor.execute('SELECT * FROM players')])
# print('Deleted %s low-max-trophy players. There are now %s players remaining' % (before - after, str(after) + '/' + str(before)))
###########################
before = len([_ for _ in cursor.execute('SELECT player_tag FROM players WHERE player_tag NOT like "#%"')])
cursor.execute("""UPDATE OR IGNORE players SET player_tag = '#' || player_tag WHERE player_tag NOT like '#%'""")
conn.commit()
after = len([_ for _ in cursor.execute('SELECT player_tag FROM players WHERE player_tag NOT like "#%"')])
print('Updated %s player_tags without #. There are now %s incorrectly formatted tags remaining' % (
before - after, str(after) + '/' + str(before)))
###########################
before = len([_ for _ in cursor.execute('SELECT player_tag FROM players WHERE player_tag NOT like "#%"')])
cursor.execute("""DELETE FROM players WHERE player_tag NOT like '#%'""")
# cursor.execute("""DELETE FROM players WHERE ('#' || player_tag) IN (SELECT player_tag FROM players)""")
conn.commit()
after = len([_ for _ in cursor.execute('SELECT player_tag FROM players WHERE player_tag NOT like "#%"')])
print('Deleted %s duplicate player_tags without #. There are now %s broken tags remaining' % (
before - after, str(after) + '/' + str(before)))
###########################
before = len([_ for _ in cursor.execute('SELECT player_tag FROM players WHERE SUBSTR(player_tag, 1, 1) != "#"')])
cursor.execute("""UPDATE players SET player_tag = ('#' || player_tag) WHERE SUBSTR(player_tag, 1, 1) != '#'""")
conn.commit()
after = len([_ for _ in cursor.execute('SELECT player_tag FROM players WHERE SUBSTR(player_tag, 1, 1) != "#"')])
print('Added # to %s player_tags. There are now %s broken tags remaining' % (
before - after, str(after) + '/' + str(before)))
###########################
before = [i for i in cursor.execute('SELECT coalesce(MAX(ROWID)+1, 0) FROM battles')][0][0]
cursor.execute("""DELETE from battles
                WHERE datetime(battle_time) < datetime('now', '-7 Day')""")
conn.commit()
after = [i for i in cursor.execute('SELECT coalesce(MAX(ROWID)+1, 0) FROM battles')][0][0]
print('Deleted %s old battles. There are now %s remaining' % (before - after, str(after) + '/' + str(before)))
###########################
before = [i for i in cursor.execute('SELECT coalesce(MAX(ROWID)+1, 0) FROM players')][0][0]
cursor.execute("""DELETE from players
                WHERE length(player_tag) < 6""")
conn.commit()
after = [i for i in cursor.execute('SELECT coalesce(MAX(ROWID)+1, 0) FROM players')][0][0]
print('Deleted %s invalidly-tagged players. There are now %s total players remaining' % (
before - after, str(after) + '/' + str(before)))
###########################
cursor.close()
conn.close()
