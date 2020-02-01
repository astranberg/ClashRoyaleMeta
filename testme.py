import asyncio
import aiohttp
import ssl
import clashroyale
import sqlite3
import logging
from datetime import date

logging.basicConfig(level=logging.INFO)

# Define Tokens
officialAPIToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9" \
                   ".eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImYyZjUzYmI2LWIyMDQtNGRkYi1" \
                   "iMGZjLTk0ZTE4ZWU3YzQ2ZSIsImlhdCI6MTU3NDYxNDgzMywic3ViIjoiZGV2ZWxvcGVyLzZlYmYzNzdmLWVkNjQtMmFlZC0" \
                   "2MjRhLWE3Nzg5YmM4OGZiNCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZl" \
                   "ciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI5OC4xOTUuMTU5LjgyIl0sInR5cGUiOiJjbGllbnQifV19.H13g" \
                   "VRs6fkSDyKEAAqPJKscx2AtN9sDbHaWNm2GSpgVZTTAe_sJM_yKkibMTCyOLu8kvOw7xcCOxycIydqqeUw"
unofficialAPIToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQ0MywiaWRlbiI6IjIyNzk4NjE5NzM3MTE1ODUyOCIsIm1k" \
                     "Ijp7InVzZXJuYW1lIjoiS2luZ0tvbmciLCJkaXNjcmltaW5hdG9yIjoiOTcxOSIsImtleVZlcnNpb24iOjN9LCJ0cyI6MTU" \
                     "3NjgwMjAxMTk1Mn0.tUBrvk38lBSrg9ilpshqBD9PbzFoOqImLVrM8hUucLg"

# Get Client Objects
officialClient = clashroyale.official_api.Client(officialAPIToken, is_async=True)
unofficialClient = clashroyale.royaleapi.Client(unofficialAPIToken, is_async=True)


async def get_clans(cr, clan_groups):
    return await asyncio.gather(*[
        cr.get_clan(*group)
        for group in clan_groups
    ])


async def main():
    # Add clan tags to database
    conn = sqlite3.connect('clans.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS players(
        player_tag TEXT,
        update_date TEXT,
        UNIQUE(player_tag));''')
    conn.commit()
    dbplayerssbefore = len([i[0] for i in cursor.execute('''SELECT * FROM players''')])
    print(dbplayerssbefore, 'players before')

    # Define Variables
    lClanPlayersTags = []
    iMaxTags = 25
    iMaxRate = 40 - 1

    cr = clashroyale.RoyaleAPI(
        unofficialAPIToken,
        is_async=True,
        timeout=50
    )

    # loop through clans, iMaxTags at a time
    lClans = [i[0] for i in cursor.execute('''SELECT * FROM clans''')]
    lClans = [x for x in lClans if len(x) > 5]  # remove tags if 5 or less characters, as these will error
    print(len(lClans), 'clans')
    for i in range(0, len(lClans), iMaxTags * iMaxRate):
        lClanGroup = [lClans[x:(x + iMaxTags)] for x in range(i, min(len(lClans), i + iMaxTags * iMaxRate), iMaxTags)]
        print(lClanGroup)
        try:
            results = await get_clans(cr, lClanGroup)
            print('Results:', results)
        finally:
            pass
        print('end', i, min(len(lClans), i + iMaxTags * iMaxRate))
        await asyncio.sleep(10)
        for clan in results:  # loop through each clan in the response
            clanmembers = [[members['tag'].replace('#', ''), date.today()] for members in clan]
            cursor.executemany('''INSERT OR IGNORE INTO players values (?, ?)''', clanmembers)
    print('closing')
    await cr.close()
    print('sleeping')
    await asyncio.sleep(4)
    print('finished sleeping')

    ldbplayers = [i[0] for i in cursor.execute('''SELECT * FROM players''')]
    dbplayerssafter = len(ldbplayers)
    print(ldbplayers)
    print('Added ' + str(dbplayerssafter - dbplayerssbefore) + ' players to database, which now has ' + str(
        dbplayerssafter) + ' players.')
    cursor.close()
    conn.close()


asyncio.run(main())
