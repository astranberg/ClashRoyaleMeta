import sqlite3
import globals

globals.init()

print('=' * 20, 'UPDATING MAX TROPHIES FROM BATTLES', '=' * 20)
conn = sqlite3.connect(globals.databasename)
cursor = conn.cursor()
###########################
before = len([_ for _ in cursor.execute('SELECT * FROM players WHERE max_trophies IS NULL OR max_trophies < 0')])
cursor.execute("""
                UPDATE
                    players
                SET
                    max_trophies = ifnull(
                        (SELECT
                            max(winner_trophies)
                        FROM
                            battles
                        WHERE
                            winner_tag == players.player_tag
                        AND
                            winner_trophies NOT NULL
                        AND
                                (winner_trophies > max_trophies
                            OR
                                max_trophies IS NULL)
                        GROUP BY
                            winner_tag),
                    max_trophies)""")
conn.commit()
cursor.execute("""
                UPDATE
                    players
                SET
                    max_trophies = ifnull(
                        (SELECT
                            max(loser_trophies)
                        FROM
                            battles
                        WHERE
                            loser_tag == players.player_tag
                        AND
                                (loser_trophies > max_trophies
                            OR
                                max_trophies IS NULL)
                        GROUP BY
                            loser_tag),
                    max_trophies)""")
conn.commit()
after = len([_ for _ in cursor.execute('SELECT * FROM players WHERE max_trophies IS NULL OR max_trophies < 0')])
print('Added max trophies to %s new players. There are now %s unknown max trophies remaining' % (
before - after, str(after) + '/' + str(before)))
###########################
cursor.close()
conn.close()
