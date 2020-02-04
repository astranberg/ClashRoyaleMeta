from datetime import date
import clashroyale
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

# Define Tokens
officialAPIToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9" \
                   ".eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImYyZjUzYmI2LWIyMDQtNGRkYi1" \
                   "iMGZjLTk0ZTE4ZWU3YzQ2ZSIsImlhdCI6MTU3NDYxNDgzMywic3ViIjoiZGV2ZWxvcGVyLzZlYmYzNzdmLWVkNjQtMmFlZC0" \
                   "2MjRhLWE3Nzg5YmM4OGZiNCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZl" \
                   "ciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI5OC4xOTUuMTU5LjgyIl0sInR5cGUiOiJjbGllbnQifV19.H13g" \
                   "VRs6fkSDyKEAAqPJKscx2AtN9sDbHaWNm2GSpgVZTTAe_sJM_yKkibMTCyOLu8kvOw7xcCOxycIydqqeUw "
unofficialAPIToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQ0MywiaWRlbiI6IjIyNzk4NjE5NzM3MTE1ODUyOCIsIm1k" \
                     "Ijp7InVzZXJuYW1lIjoiS2luZ0tvbmciLCJkaXNjcmltaW5hdG9yIjoiOTcxOSIsImtleVZlcnNpb24iOjN9LCJ0cyI6MTU" \
                     "3NjgwMjAxMTk1Mn0.tUBrvk38lBSrg9ilpshqBD9PbzFoOqImLVrM8hUucLg "

# Get Client Objects
officialClient = clashroyale.official_api.Client(officialAPIToken)
unofficialClient = clashroyale.royaleapi.Client(unofficialAPIToken)


def get_top_players():
    # Get Client Objects
    officialClient = clashroyale.official_api.Client(officialAPIToken)
    # Get the top x players
    lTopPlayers = officialClient.get_top_players(57000249, limit=5)
    # Add player tags to database
    conn = sqlite3.connect(globals.databasename)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS players(
        player_tag TEXT,
        update_date TEXT,
        UNIQUE(player_tag));''')
    conn.commit()
    dbplayerssbefore = len([i[0] for i in cursor.execute('''SELECT * FROM players''')])
    lTopPlayers = [[i.tag.replace('#', ''), date.today()] for i in lTopPlayers]
    cursor.executemany('''INSERT OR IGNORE INTO players values (?, ?)''', lTopPlayers)
    conn.commit()
    ldbplayers = [i[0] for i in cursor.execute('''SELECT player_tag FROM players''')]
    dbplayerssafter = len(ldbplayers)
    print('Added ' + str(dbplayerssafter - dbplayerssbefore) + ' players to database, which now has ' + str(
        dbplayerssafter) + ' players.')
    cursor.close()
    conn.close()
