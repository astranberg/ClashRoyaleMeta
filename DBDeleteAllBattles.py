import sqlite3
import globals

globals.init()

print('=' * 20, 'DELETING ALL BATTLES', '=' * 20)
conn = sqlite3.connect(globals.databasename)
cursor = conn.cursor()
###########################
# before = len([_ for _ in cursor.execute('SELECT * FROM battles')])
cursor.execute("""DELETE FROM battles""")
conn.commit()
# after = len([_ for _ in cursor.execute('SELECT * FROM battles')])
# print('Deleted %s battles. There are now %s remaining' % (after - before, str(after) + '/' + str(before)))
###########################
cursor.close()
conn.close()
