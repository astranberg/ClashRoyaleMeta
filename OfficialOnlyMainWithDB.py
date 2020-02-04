from datetime import datetime
import asyncio
import logging
import csv
import clashroyale
from BattleInterpreter import archetype
import sqlite3
import globals
from datetime import date
from getClans import add_clans
from getClanPlayers import get_clan_players
from getTopPlayers import get_top_players

globals.init()

logging.basicConfig(level=logging.INFO)


def header_print(title, total_len):
    num = round((total_len - len(title)) / 2)
    odd_number = len(title) % 2 != 0
    print('=' * num, title, '=' * (num + odd_number))


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


async def battlefinder(lClanPlayersTags):
    import globals
    globals.init()
    lResults = []
    lUnknownDecks = []
    officialClient = clashroyale.official_api.Client(globals.officialAPIToken, is_async=True, timeout=999)
    # Loop through the players, iMaxTags at a time
    iMaxTags = 1
    iMaxRate = 50  # 12
    lOppPlayerTags = []
    conn = sqlite3.connect(globals.databasename)
    cursor = conn.cursor()
    dbplayerssbefore = len([i[0] for i in cursor.execute('''SELECT * FROM players''')])
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
                            if battle_type.lower() == 'challenge':
                                battle_type = lPlayerBattles[i]['challengeTitle']
                            battle_date = datetime.strptime(lPlayerBattles[i]['battleTime'],
                                                            "%Y%m%dT%H%M%S.%fZ").isoformat()
                            if len(lPlyrDeck[1]) == 0:
                                lUnknownDecks.append([i['name'].lower() for i in lPlayerBattles[i]['team'][0]['cards']])
                            if len(lOppDeck[1]) == 0:
                                lUnknownDecks.append(
                                    [i['name'].lower() for i in lPlayerBattles[i]['opponent'][0]['cards']])
                            # if battle_type == 'Challenge':
                            # battle_type = lPlayerBattles[i]['challengeTitle']
                            if lPlayerBattles[i]['opponent'][0]['startingTrophies'] > 4600:
                                lOppPlayerTags.append([lPlayerBattles[i]['opponent'][0]['tag'], date.today()])
                            if lPlayerBattles[i]['team'][0]['crowns'] > lPlayerBattles[i]['opponent'][0][
                                'crowns']:  # player won
                                lResults.append([battle_date,
                                                 battle_type,
                                                 lPlayerBattles[i]['team'][0]['tag'].replace('#', ''),
                                                 lPlayerBattles[i]['team'][0]['startingTrophies'],
                                                 lPlyrDeck[1],
                                                 lPlayerBattles[i]['opponent'][0]['tag'].replace('#', ''),
                                                 lPlayerBattles[i]['opponent'][0]['startingTrophies'],
                                                 lOppDeck[1]])
                            elif lPlayerBattles[i]['team'][0]['crowns'] == lPlayerBattles[i]['opponent'][0][
                                'crowns']:  # its a tie
                                pass
                            else:  # opponent won
                                lResults.append([battle_date,
                                                 battle_type,
                                                 lPlayerBattles[i]['opponent'][0]['tag'].replace('#', ''),
                                                 lPlayerBattles[i]['opponent'][0]['startingTrophies'],
                                                 lOppDeck[1],
                                                 lPlayerBattles[i]['team'][0]['tag'].replace('#', ''),
                                                 lPlayerBattles[i]['team'][0]['startingTrophies'],
                                                 lPlyrDeck[1]])
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
        lResults = makeunique(lResults)
        cursor.executemany('''INSERT OR IGNORE INTO battles values (?, ?, ?, ?, ?, ?, ?, ?)''', lResults)
        cursor.executemany('''INSERT OR IGNORE INTO players values (?, ?)''', lOppPlayerTags)
        lResults = []
        lOppPlayerTags = []
        conn.commit()
    # add opposing players to database
    cursor.executemany('''INSERT OR IGNORE INTO battles values (?, ?, ?, ?, ?, ?, ?, ?)''', lResults)
    conn.commit()
    ldbplayers = [i[0] for i in cursor.execute('''SELECT player_tag FROM players''')]
    dbplayerssafter = len(ldbplayers)
    print('Added ' + str(dbplayerssafter - dbplayerssbefore) + ' opposing players to database, which now has ' + str(
        dbplayerssafter) + ' players.')
    cursor.close()
    conn.close()

    # Print unknown decks to CSV
    print('=' * 20, 'PRINTING UNKNOWN DECKS TO CSV', '=' * 20)
    with open('unknown_decks.csv', 'w+', newline='') as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        try:
            csvWriter.writerows(lUnknownDecks)
        except:
            pass

    return lResults


async def waitplz():
    await asyncio.sleep(30)


def main(num_runs, b_update_databases, max_player_tags):
    try:
        while num_runs != 0:
            header_print('STARTING NEW RUN', 100)
            if b_update_databases:
                header_print('ADDING CLANS', 100)
                add_clans()
                header_print('ADDING CLAN PLAYERS', 100)
                get_clan_players()
                header_print('ADDING TOP PLAYERS', 100)
                get_top_players()
            # Select db clan players
            conn = sqlite3.connect(globals.databasename)
            cursor = conn.cursor()
            if max_player_tags > 0:
                sql_query_player = '''SELECT player_tag FROM players ORDER BY update_date ASC LIMIT %s''' % (
                    max_player_tags)
            else:
                sql_query_player = '''SELECT player_tag FROM players'''
            lClanPlayersTags = [i[0] for i in cursor.execute(sql_query_player) if len(i[0]) > 5]
            # Update the database for which players we are pulling now
            cursor.execute("""UPDATE players
                            SET update_date = datetime("now")
                            WHERE player_tag IN (%s)""" % sql_query_player)
            conn.commit()
            num_runs -= 1
            # Run the battlefinder script to get battles!
            header_print('GATHERING BATTLES', 100)
            asyncio.run(battlefinder(lClanPlayersTags))
    except:
        pass


main(1, False, 250000)
# main(-1, False, 500000)

cursor.close()
conn.close()
asyncio.run(waitplz())
print('Done!')
