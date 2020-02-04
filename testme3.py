import asyncio
import logging
import csv
import clashroyale
from collections import OrderedDict
from BattleInterpreter import archetype
from interpretbattles import battleDeckPrinter

import sqlite3

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

lDeck = [['Bridge Spam'], ['EGNW'], ['EG Sparky'], ['Giant double prince'], ['Giant GY'], ['Giant Miner NW'],
         ['Giant cycle'], ['Giant sparky'], ['Giant 3M'], ['Goblin giant sparky'], ['Golem balloon'],
         ['Golem Lightning'], ['Golem NW'], ['GY Control'], ['Hog EQ'], ['HogXNado'], ['Hog mortar'],
         ['Hog mortar bait'], ['Hog 2.6'], ['LavaClone'], ['Lavaloon'], ['Lavaminer'], ['Mortar Miner Bait'],
         ['MK miner hog'], ['Miner Hog'], ['Miner Balloon'], ['Miner bait'], ['Miner cycle'], ['Miner WB'],
         ['MK Miner Control'], ['Pekka Miner'], ['Miner Poison'], ['Classic bait'], ['Ram Rider Spam'],
         ['Ram rider 3M Miner'], ['RG Furnace'], ['RG'], ['Royal hogs'], ['Xbow 2.9'], ['Icebow'], ['MK bait'],
         ['Balloon Freeze'], ['Classic 3M Pump'], ['Hog Rocket'], ['Noob Rage'], ['EG Healer'], ['Xbow Misc']]


async def get_battles(cr, player_groups):
    return await asyncio.gather(*[
        cr.get_player_battles(*group)
        for group in player_groups
    ])


async def main():
    cr = clashroyale.RoyaleAPI(
        unofficialAPIToken,
        is_async=True,
        timeout=30
    )

    lPlayerTags = [i[0] for i in cursor.execute('''SELECT * FROM players''')]
    lPlayerTags = [x for x in lPlayerTags if len(x) > 5]  # remove tags if 5 or less characters, as these will error
    print(len(lPlayerTags), 'players')
    # for iPlayerGroup in range(0, len(lPlayerTags), iMaxTags * iMaxRate):
    for iPlayerGroup in range(0, 1, iMaxTags * iMaxRate):
        # Loop through the players, iMaxTags at a time
        # for iPlayerGroup in range(0, len(lPlayerTags), iMaxTags):
        lPlayerGroup = [lPlayerTags[x:(x + iMaxTags)] for x in
                        range(iPlayerGroup, min(len(lPlayerTags), iPlayerGroup + iMaxTags * iMaxRate), iMaxTags)]
        print(lPlayerGroup)
        # get data from all players,* iterates the list into args
        try:
            lPlayerBattles = await get_battles(cr, lPlayerGroup)
            print('Results:', lPlayerBattles)
        finally:
            pass
        print('end', iPlayerGroup, min(len(lPlayerTags), iPlayerGroup + iMaxTags * iMaxRate))
        await asyncio.sleep(10)

    # with open('new_file.csv', 'w+', newline='') as my_csv:
    # csvWriter = csv.writer(my_csv, delimiter=',')
    # csvWriter.writerows(lResults)


# Add clan tags to database
conn = sqlite3.connect(globals.databasename)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS battles(
    battle_time TEXT,
    mode TEXT,
    winner_tag TEXT,
    winner_trophies TEXT,
    winner_crowns INTEGER,
    winner_decktype TEXT,
    winner_archetype TEXT,
    winner_deck BLOB,
    loser_tag TEXT,
    loser_trophies TEXT,
    loser_crowns INTEGER,
    loser_decktype TEXT,
    loser_archetype TEXT,
    loser_deck BLOB,
    UNIQUE(battle_time,winner_tag,loser_tag));''')
conn.commit()

# Define Variables
iMaxTags = 1
iMaxRate = 1

asyncio.run(main())

print(' Player group', iPlayerGroup, 'has', len(lPlayerBattles), 'battles.')
# loop through battles and add to array
lPlayerBattles = lPlayerBattles[0]
print(lPlayerBattles[0]['team'][0]['deck'])
for i in range(0, len(lPlayerBattles)):
    if False:  # eventually if unique or not
        print('Duplicate!', lPlayerBattles[i]['utcTime'] + lPlayerBattles[i]['team'][0]['tag'])
    else:
        lPlyrDeck = archetype(lPlayerBattles[i]['team'][0]['deck'])
        lOppDeck = archetype(lPlayerBattles[i]['opponent'][0]['deck'])
        print(lPlyrDeck)
        print(lOppDeck)
        if lPlayerBattles[i]['winner'] > 0:
            print([lPlayerBattles[i]['utcTime'],
                   lPlayerBattles[i]['mode']['name'],
                   lPlayerBattles[i]['team'][0]['tag'],
                   lPlayerBattles[i]['team'][0]['startTrophies'],
                   lPlayerBattles[i]['teamCrowns'],
                   lPlyrDeck[0][0],
                   lPlyrDeck[1][0],
                   [z['name'].lower() for z in lPlayerBattles[i]['team'][0]['deck']][0],
                   lPlayerBattles[i]['opponent'][0]['tag'],
                   lPlayerBattles[i]['opponent'][0]['startTrophies'],
                   lPlayerBattles[i]['opponentCrowns'],
                   lOppDeck[0][0],
                   lOppDeck[1][0],
                   [z['name'].lower() for z in lPlayerBattles[i]['opponent'][0]['deck']]][0])
            cursor.execute('''INSERT OR IGNORE INTO battles(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                           [lPlayerBattles[i]['utcTime'],
                            lPlayerBattles[i]['mode']['name'],
                            lPlayerBattles[i]['team'][0]['tag'],
                            lPlayerBattles[i]['team'][0]['startTrophies'],
                            lPlayerBattles[i]['teamCrowns'],
                            lPlyrDeck[0][0],
                            lPlyrDeck[1][0],
                            [z['name'].lower() for z in lPlayerBattles[i]['team'][0]['deck']][0],
                            lPlayerBattles[i]['opponent'][0]['tag'],
                            lPlayerBattles[i]['opponent'][0]['startTrophies'],
                            lPlayerBattles[i]['opponentCrowns'],
                            lOppDeck[0][0],
                            lOppDeck[1][0],
                            [z['name'].lower() for z in lPlayerBattles[i]['opponent'][0]['deck']]][0])
            # lResults[lPlyrDeck[2]][lOppDeck[2]] = 1 + lResults[lPlyrDeck[2]][lOppDeck[2]]
        elif lPlayerBattles[i]['winner'] == 0:
            a = a
            # print('draw:', lOppDeck[1], lPlayerBattles[i]['opponentCrowns'], lPlyrDeck[1],
            # lPlayerBattles[i]['teamCrowns'])
        else:
            print('winner:', lOppDeck[1], lPlayerBattles[i]['opponentCrowns'], 'loser:', lPlyrDeck[1])
            cursor.execute('''INSERT OR IGNORE INTO battles(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                           [lPlayerBattles[i]['utcTime'],
                            lPlayerBattles[i]['mode']['name'],
                            lPlayerBattles[i]['team'][0]['tag'],
                            lPlayerBattles[i]['opponent'][0]['tag'],
                            lPlayerBattles[i]['opponent'][0]['startTrophies'],
                            lPlayerBattles[i]['opponentCrowns'],
                            lOppDeck[0],
                            lOppDeck[1],
                            [z['name'].lower() for z in lPlayerBattles[i]['opponent'][0]['deck']],
                            lPlayerBattles[i]['team'][0]['startTrophies'],
                            lPlayerBattles[i]['teamCrowns'],
                            lPlyrDeck[0],
                            lPlyrDeck[1],
                            [z['name'].lower() for z in lPlayerBattles[i]['team'][0]['deck']]])
        conn.commit()
print('Done!', lResults)
ldbplayers = [i[0] for i in cursor.execute('''SELECT * FROM players''')]
dbplayerssafter = len(ldbplayers)
print(ldbplayers)
print('Added ' + str(dbplayerssafter - dbplayerssbefore) + ' players to database, which now has ' + str(
    dbplayerssafter) + ' players.')
cursor.close()
conn.close()
# battleDeckPrinter(lResults,'ladder',4600,8200,600,3,'LadderQ300')
# battleDeckPrinter(lResults,'ladder',4600,8200,3000,3,'LadderALL')
# battleDeckPrinter(lResults,'challenge',4600,8200,3000,3,'challenge')
