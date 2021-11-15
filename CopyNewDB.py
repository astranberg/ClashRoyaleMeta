import sqlite3
import globals

globals.init()

print('=' * 20, 'CLEANING DATABASE OF ALL BATTLES', '=' * 20)
conn = sqlite3.connect(globals.databasename)
cursor = conn.cursor()
###########################
cursor.execute("""DELETE FROM battles""")
conn.commit()
cursor.execute("""vacuum""")
conn.commit()
