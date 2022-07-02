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
                     "3NjgwMjAxMTk1Mn0.tUBrvk38lBSrg9ilpshqBD9PbzFoOqImLVrM8hUucLg"


# Get Client Objects
# officialClient = clashroyale.official_api.Client(globals.officialAPIToken, is_async=True, timeout=30)
# unofficialClient = clashroyale.royaleapi.Client(globals.unofficialAPIToken)


async def get_clans(cr, clan_groups):
    return await asyncio.gather(*[
        cr.get_clan(group)
        for group in clan_groups
    ])


async def get_clan_players():
    # Add clan tags to database
    conn = sqlite3.connect(globals.databasename)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS players(
        player_tag TEXT,
        update_date TEXT,
        max_trophies TEXT,
        UNIQUE(player_tag));''')
    conn.commit()
    dbplayerssbefore = len([i[0] for i in cursor.execute('''SELECT player_tag FROM players''')])

    # Define Variables
    lClanPlayersTags = []
    iMaxTags = 25
    cr = clashroyale.official_api.Client(officialAPIToken, is_async=True, timeout=30)

    # loop through clans, iMaxTags at a time
    lClans = [i[0] for i in cursor.execute('''SELECT * FROM clans''')]
    lClans = [x for x in lClans if len(x) > 5]  # remove tags if 5 of less characters, as these will error
    print('There are', len(lClans), 'clans in the database.')
    for iClanGroup in range(0, len(lClans), iMaxTags):
        lClanGroup = [i for i in
                      lClans[iClanGroup:min(iClanGroup + iMaxTags, len(lClans))]]  # get next 25 (or max) clans
        # print(lClanGroup)
        lClanGroupTags = await get_clans(cr, lClanGroup)
        await asyncio.sleep(1)
        # lClanGroupTags = officialClient.get_clan(*lClanGroup)  # get data from all clans,* iterates the list into args
        # print(lClanGroupTags[0], "hi")
        for clan in lClanGroupTags:  # loop through each clan in the response
            # players = [member['tag'].replace('#', '') for member in clan['members'] for clan in lClanGroupTags]
            clanmembers = [[members['tag'], date.today(), -1] for members in clan['memberList']]
            # print((clanmembers))
            # clanmembers = zip([members['tag'].replace('#','') for members in clan['members']], date.today() * len(clan['members']))
            cursor.executemany('''INSERT OR IGNORE INTO players values (?, ?, ?)''', clanmembers)
        # print('Clan group', iClanGroup, 'has', len(lClanGroupTags), 'of', len(lClans), 'clans and',
        #      len([member['tag'].replace('#', '') for member in clan['memberList'] for clan in lClanGroupTags]),
        #      'players.')

    conn.commit()
    dbplayerssafter = len([i[0] for i in cursor.execute('''SELECT player_tag FROM players''')])
    print('Added ' + str(dbplayerssafter - dbplayerssbefore) + ' players to database, which now has ' + str(
        dbplayerssafter) + ' players.')
    cursor.close()
    conn.close()
    await cr.close()

#asyncio.run(get_clan_players())
