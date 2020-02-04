from random import sample
import asyncio
import logging
import csv
import clashroyale
from collections import OrderedDict
from BattleInterpreter import archetype
from OldDeckPrinter import battleDeckPrinter
import sqlite3
import globals
from datetime import date
from getClans import add_clans
from getClanPlayers import get_clan_players
from getTopPlayers import get_top_players

globals.init()

logging.basicConfig(level=logging.INFO)


def makeunique(l):
    check = set()
    res = []
    for i in l:
        if str(i[0]) + i[2] not in check:
            res.append(i)
            check.add(str(i[0]) + i[2])
        else:
            pass
    return res


async def get_battles(cr, clan_groups):
    return await asyncio.gather(*[
        cr.get_player_battles(*group)
        for group in clan_groups
    ])


async def main():
    import globals
    globals.init()
    lResults = []
    officialClient = clashroyale.official_api.Client(globals.officialAPIToken, is_async=True, timeout=999)
    # Loop through the players, iMaxTags at a time
    iMaxTags = 1
    iMaxRate = 50  # 12
    lOppPlayerTags = []
    for iPlayerGroup in range(0, len(lClanPlayersTags), iMaxTags * iMaxRate):
        lPlayerGroup = [lClanPlayersTags[x:(x + iMaxTags)] for x in
                        range(iPlayerGroup, min(len(lClanPlayersTags), iPlayerGroup + iMaxTags * iMaxRate), iMaxTags)]
        while True:
            try:
                lAllPlayerBattles = await get_battles(officialClient, lPlayerGroup)
                await asyncio.sleep(2)
                print(' Players', str(iPlayerGroup) + '-' + str(
                    min(len(lClanPlayersTags), iPlayerGroup + iMaxTags * iMaxRate)) + ' of ' + str(
                    len(lClanPlayersTags)),
                      'have', sum([len(_) for _ in lAllPlayerBattles]), 'battles.')
                # loop through battles and add to array
                for lPlayerBattles in lAllPlayerBattles:
                    for i in range(0, len(lPlayerBattles)):
                        if lPlayerBattles[i]['type'] == 'PvP':
                            lPlyrDeck = archetype(lPlayerBattles[i]['team'][0]['cards'])
                            lOppDeck = archetype(lPlayerBattles[i]['opponent'][0]['cards'])
                            battle_type = lPlayerBattles[i]['gameMode']['name']
                            # if battle_type == 'Challenge':
                            # battle_type = lPlayerBattles[i]['challengeTitle']
                            if lPlayerBattles[i]['opponent'][0]['startingTrophies'] > 4600:
                                lOppPlayerTags.append([lPlayerBattles[i]['opponent'][0]['tag'], date.today()])
                            if lPlayerBattles[i]['team'][0]['crowns'] > lPlayerBattles[i]['opponent'][0][
                                'crowns']:  # player won
                                lResults.append([lPlayerBattles[i]['battleTime'], battle_type,
                                                 lPlayerBattles[i]['team'][0]['tag'],
                                                 lPlayerBattles[i]['team'][0]['startingTrophies'],
                                                 lPlayerBattles[i]['team'][0]['crowns'], lPlyrDeck[0], lPlyrDeck[1],
                                                 [z['name'].lower() for z in lPlayerBattles[i]['team'][0]['cards']],
                                                 lPlayerBattles[i]['opponent'][0]['tag'],
                                                 lPlayerBattles[i]['opponent'][0]['startingTrophies'],
                                                 lPlayerBattles[i]['opponent'][0]['crowns'], lOppDeck[0], lOppDeck[1],
                                                 [z['name'].lower() for z in
                                                  lPlayerBattles[i]['opponent'][0]['cards']]])
                            elif lPlayerBattles[i]['team'][0]['crowns'] == lPlayerBattles[i]['opponent'][0][
                                'crowns']:  # its a tie
                                pass
                            else:  # opponent won
                                lResults.append([lPlayerBattles[i]['battleTime'], battle_type,
                                                 lPlayerBattles[i]['opponent'][0]['tag'],
                                                 lPlayerBattles[i]['opponent'][0]['startingTrophies'],
                                                 lPlayerBattles[i]['opponent'][0]['crowns'], lOppDeck[0], lOppDeck[1],
                                                 [z['name'].lower() for z in lPlayerBattles[i]['opponent'][0]['cards']],
                                                 lPlayerBattles[i]['team'][0]['tag'],
                                                 lPlayerBattles[i]['team'][0]['startingTrophies'],
                                                 lPlayerBattles[i]['team'][0]['crowns'], lPlyrDeck[0], lPlyrDeck[1],
                                                 [z['name'].lower() for z in lPlayerBattles[i]['team'][0]['cards']]])
                break
            except asyncio.exceptions.TimeoutError:
                print('Asyncio Timeout Error!')
                await asyncio.sleep(2)
                continue
            except clashroyale.errors.NotResponding:
                print('Clash Royale API Timed Out')
                await asyncio.sleep(2)
                continue
            except clashroyale.errors.RatelimitError or clashroyale.errors.RatelimitErrorDetected:
                print('API Rate Limit Error')
                await asyncio.sleep(2)
                continue
            except clashroyale.errors.NetworkError:
                print('Network Error')
                await asyncio.sleep(5)
                continue
            except clashroyale.errors.ServerError:
                print('Server Error')
                await asyncio.sleep(5)
                continue
                # except:
                print('Unknown Error')
                await asyncio.sleep(5)
                continue
    battles_before = len(lResults)
    lResults = makeunique(lResults)
    battles_after = len(lResults)
    print('Removed', battles_before - battles_after, 'duplicate values!')
    print(str(battles_after) + '/' + str(battles_before) + ' battles remain!')
    # add opposing players to database
    conn = sqlite3.connect(globals.databasename)
    cursor = conn.cursor()
    dbplayerssbefore = len([i[0] for i in cursor.execute('''SELECT * FROM players''')])
    cursor.executemany('''INSERT OR IGNORE INTO players values (?, ?)''', lOppPlayerTags)
    conn.commit()
    ldbplayers = [i[0] for i in cursor.execute('''SELECT player_tag FROM players''')]
    dbplayerssafter = len(ldbplayers)
    print('Added ' + str(dbplayerssafter - dbplayerssbefore) + ' opposing players to database, which now has ' + str(
        dbplayerssafter) + ' players.')
    cursor.close()
    conn.close()

    return lResults


#####################
b_update_databases = False
if b_update_databases:
    add_clans()
    get_clan_players()
    get_top_players()
#####################

# getting db clan players
conn = sqlite3.connect(globals.databasename)
cursor = conn.cursor()
lClanPlayersTags = [i[0] for i in cursor.execute('''SELECT player_tag FROM players''') if len(i[0]) > 5]
max_player_tags = 500

if max_player_tags > 0:
    lClanPlayersTags = sample(lClanPlayersTags, max_player_tags)
    print('lClanPlayersTags:', len(lClanPlayersTags))

# Run the main script to get battles!
lResults = asyncio.run(main())

# Print battles to CSV
with open('new_file.csv', 'w+', newline='') as my_csv:
    csvWriter = csv.writer(my_csv, delimiter=',')
    try:
        csvWriter.writerows(lResults)
    except:
        pass

# Print statistics to .XLSX
battleDeckPrinter(lResults, 'ladder', 5900, 6200, 300, 3)
battleDeckPrinter(lResults, 'ladder', 4600, 8200, 600, 3)
battleDeckPrinter(lResults, 'ladder', 4600, 8200, 200, 3)
battleDeckPrinter(lResults, 'ladder', 4600, 8200, 300, 3)
battleDeckPrinter(lResults, 'ladder', 4600, 8200, 0, 3)
battleDeckPrinter(lResults, 'grand challenge', 4600, 8200, 0, 3)
battleDeckPrinter(lResults, 'classic challenge', 4600, 8200, 0, 3)


async def waitplz():
    await asyncio.sleep(30)


cursor.close()
conn.close()
# asyncio.run(waitplz())
print('Done!')
