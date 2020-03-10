from datetime import date
import clashroyale
import sqlite3
import logging
import globals

globals.init()

logging.basicConfig(level=logging.INFO)

# Get Client Objects
officialClient = clashroyale.official_api.Client(globals.officialAPIToken)
unofficialClient = clashroyale.royaleapi.Client(globals.unofficialAPIToken)

def get_top_players():
    # Get Client Objects
    officialClient = clashroyale.official_api.Client(globals.officialAPIToken)
    # Get the top x players
    lTopPlayers = officialClient.get_top_players(57000249, limit=5)
    # Add player tags to database
    conn = sqlite3.connect(globals.databasename)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS players(
        player_tag TEXT,
        update_date TEXT,
        max_trophies TEXT,
        UNIQUE(player_tag));''')
    conn.commit()
    dbplayerssbefore = len([i[0] for i in cursor.execute('''SELECT * FROM players''')])
    lTopPlayers = [[i.tag.replace('#', ''), date.today(), -1] for i in lTopPlayers]
    cursor.executemany('''INSERT OR IGNORE INTO players values (?, ?, ?)''', lTopPlayers)
    conn.commit()
    ldbplayers = [i[0] for i in cursor.execute('''SELECT player_tag FROM players''')]
    dbplayerssafter = len(ldbplayers)
    print('Added ' + str(dbplayerssafter - dbplayerssbefore) + ' players to database, which now has ' + str(
        dbplayerssafter) + ' players.')
    cursor.close()
    conn.close()
