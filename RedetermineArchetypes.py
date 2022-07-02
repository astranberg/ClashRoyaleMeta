import sqlite3
import globals

globals.init()

print('=' * 20, 'REDETERMINING DECKTYPES', '=' * 20)
conn = sqlite3.connect(globals.databasename)
cursor = conn.cursor()
###########################
cursor.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS winners USING fts4(cards)""")
conn.commit()
cursor.execute("""INSERT INTO winners SELECT winner_cards FROM battles""")
conn.commit()
for i in range(0, len(globals.l_deck)):
    match_phrase = ""
    # print(globals.l_include[i])
    for include in globals.l_include[i]:
        # print(include)
        if len(include) > 0:
            if (len(match_phrase) == 0):
                match_phrase += '"%s"' % (include)
            else:
                match_phrase += ' AND "%s"' % (include)
    # print(globals.l_exclude[i])
    for exclude in globals.l_exclude[i]:
        # print(exclude)
        if len(exclude) > 0:
            match_phrase += ' NOT "%s"' % (exclude)
    # print(match_phrase)
    sql_text = """UPDATE battles SET winner_decktype = "%s" WHERE ROWID IN (SELECT ROWID FROM winners WHERE cards MATCH '%s')""" % (
        globals.l_deck[i], match_phrase.strip())
    print(sql_text)
    cursor.execute(sql_text)
    conn.commit()
cursor.execute("""DROP TABLE winners""")
conn.commit()
print('Done!')
###########################
cursor.close()
conn.close()
