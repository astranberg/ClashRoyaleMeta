import asyncio
import clashroyale
import sqlite3
import logging
from datetime import date
import globals

globals.init()

logging.basicConfig(level=logging.INFO)

# Define Tokens
officialAPIToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjYyNTgwNTVkLTAyMDMtNDFhOS05NTRjLWUwNjNmYzk1ZDQ0ZCIsImlhdCI6MTY1NTE1NDEwMSwic3ViIjoiZGV2ZWxvcGVyLzZlYmYzNzdmLWVkNjQtMmFlZC02MjRhLWE3Nzg5YmM4OGZiNCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3My43Ny41OC42MyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.4wG7WwYjTQQIkd5_czrhLtmh2str4V1OmPLdTSG2RIrMufqJfk_BYmmf_Xz98kASYUfCJxtygn3UuMFHR7y4SA"
unofficialAPIToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQ0MywiaWRlbiI6IjIyNzk4NjE5NzM3MTE1ODUyOCIsIm1k" \
                     "Ijp7InVzZXJuYW1lIjoiS2luZ0tvbmciLCJkaXNjcmltaW5hdG9yIjoiOTcxOSIsImtleVZlcnNpb24iOjN9LCJ0cyI6MTU" \
                     "3NjgwMjAxMTk1Mn0.tUBrvk38lBSrg9ilpshqBD9PbzFoOqImLVrM8hUucLg "


# unofficialClient = clashroyale.royaleapi.Client(unofficialAPIToken)

async def add_clans():
    # Get Client Objects
    officialClient = clashroyale.official_api.Client(officialAPIToken)
    # Get the top x clans
    lTopClans = officialClient.get_top_clans(57000249, limit=1000)
    lBattleClans = officialClient.get_top_clanwar_clans(57000249, limit=1000)
    # Put clans tags in list
    lClanTags = [i.tag.replace('#', '') for i in lTopClans]
    lClanTags.extend([i.tag.replace('#', '') for i in lBattleClans])
    lClanTags = list(set(lClanTags))
    lClanTags = [[i, date.today()] for i in lClanTags if len(i) > 5]
    print('Number of Clans:', len(lClanTags))
    # Add clan tags to database
    conn = sqlite3.connect(globals.databasename)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clans(
        clan_tag STRING,
        update_date TEXT,
        UNIQUE(clan_tag));''')
    conn.commit()
    dbclansbefore = len([i[0] for i in cursor.execute('''SELECT * FROM clans''')])
    cursor.executemany('''INSERT OR IGNORE INTO clans values (?, ?)''', lClanTags)
    conn.commit()
    ldbclans = [i[0] for i in cursor.execute('''SELECT * FROM clans''')]
    dbclansafter = len(ldbclans)
    print('Added ' + str(dbclansafter - dbclansbefore) + ' clans to database, which now has ' + str(
        dbclansafter) + ' clans.')
    cursor.close()
    conn.close()
    await officialClient.close()
