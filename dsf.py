print('=' * 20, 'CLEANING DATABASE OF LOW-LEVEL PLAYERS', '=' * 20)
dbfrom = 'Season9.db'
dbto = 'Season11.db'
connfrom = sqlite3.connect('Season9.db')
cursorfrom = connfrom.cursor()

connto = sqlite3.connect('Season9.db')
cursorto = connto.cursor()
cursorto.execute('''CREATE TABLE IF NOT EXISTS clans(
    clan_tag STRING,
    update_date TEXT,
    UNIQUE(clan_tag));''')
connto.commit()
connto.execute('''CREATE TABLE IF NOT EXISTS players(
    player_tag TEXT,
    update_date TEXT,
    max_trophies TEXT,
    UNIQUE(player_tag));''')
connto.commit()

###########################
connto.execute("""ATTACH DATABASE %s AS new_db""" % dbto)
conn.commit()
