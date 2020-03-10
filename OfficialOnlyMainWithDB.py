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


def makeunique_multi(l):
    check = set()
    res = []
    for i in l:
        x = ''
        for j in i:
            x = x + (j)
        if not x in check:
            res.append(i)
            check.add(x)
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS battles(
        battle_time TEXT,
        battle_type TEXT,
        winner_tag TEXT,
        winner_trophies INTEGER,
        winner_decktype TEXT,
        winner_cards TEXT,
        loser_tag TEXT,
        loser_trophies INTEGER,
        loser_decktype TEXT,
        loser_cards TEXT,
        UNIQUE(battle_time,winner_tag,loser_tag));''')
    conn.commit()
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
                # add a card meta report....maybe change the database so the cards in the deck are laid out?
                # winner then loser: w1, w2, w3...w8, l1, l2, l3...l8
                # card prevalence and win percentage in the meta, broken down by trophies too
                # card vs card matchup and win percentage
                # then use the data to create card suggestions\
                for lPlayerBattles in lAllPlayerBattles:
                    for i in range(0, len(lPlayerBattles)):
                        if lPlayerBattles[i]['type'] == 'PvP' or lPlayerBattles[i]['type'] == 'challenge':
                            ##     ','.join([str(x['name']) for x in lUnknownDecks])
                            print('aa')
                            lPlyrDeck = archetype(lPlayerBattles[i]['team'][0]['cards'])
                            lOppDeck = archetype(lPlayerBattles[i]['opponent'][0]['cards'])
                            print('bb')
                            player_cards = ','.join([str(x['name']) for x in lPlayerBattles[i]['team'][0]['cards']])
                            opponent_cards = ','.join([str(x['name']) for x in lPlayerBattles[i]['opponent'][0]['cards']])
                            print('cc')
                            battle_type = lPlayerBattles[i]['gameMode']['name']
                            if battle_type.lower() == 'challenge':
                                battle_type = lPlayerBattles[i]['challengeTitle']
                            if lPlayerBattles[i]['isLadderTournament'] == True:
                                battle_type = 'global_tournament'
                            print('dd')
                            battle_date = datetime.strptime(lPlayerBattles[i]['battleTime'],
                                                            "%Y%m%dT%H%M%S.%fZ").isoformat()
                            print('g')
                            if len(lPlyrDeck[1]) == 0:
                                lUnknownDecks.append([i['name'].lower() for i in lPlayerBattles[i]['team'][0]['cards']])
                            print('H')
                            if len(lOppDeck[1]) == 0:
                                lUnknownDecks.append(
                                    [i['name'].lower() for i in lPlayerBattles[i]['opponent'][0]['cards']])
                            print('h')
                            try: # sometimes starting trophies is missing
                                player_starting_trophies = lPlayerBattles[i]['team'][0]['startingTrophies']
                            except:
                                player_starting_trophies = -1
                            try: # sometimes starting trophies is missing
                                opponent_starting_trophies = lPlayerBattles[i]['opponent'][0]['startingTrophies']
                            except:
                                opponent_starting_trophies = -1
                            if opponent_starting_trophies > 4600:
                                #print('hh')
                                lOppPlayerTags.append([lPlayerBattles[i]['opponent'][0]['tag'], date.today(), -1])
                            #print('i')
                            if lPlayerBattles[i]['team'][0]['crowns'] > lPlayerBattles[i]['opponent'][0][
                                'crowns']:  # player won
                                lResults.append([battle_date,
                                                 battle_type,
                                                 lPlayerBattles[i]['team'][0]['tag'].replace('#', ''),
                                                 player_starting_trophies,
                                                 lPlyrDeck[1],
                                                 player_cards,
                                                 lPlayerBattles[i]['opponent'][0]['tag'].replace('#', ''),
                                                 opponent_starting_trophies,
                                                 lOppDeck[1],
                                                 opponent_cards])
                            elif lPlayerBattles[i]['team'][0]['crowns'] == lPlayerBattles[i]['opponent'][0][
                                'crowns']:  # its a tie
                                pass
                            else:  # opponent won
                                lResults.append([battle_date,
                                                 battle_type,
                                                 lPlayerBattles[i]['opponent'][0]['tag'].replace('#', ''),
                                                 opponent_starting_trophies,
                                                 lOppDeck[1],
                                                 opponent_cards,
                                                 lPlayerBattles[i]['team'][0]['tag'].replace('#', ''),
                                                 player_starting_trophies,
                                                 lPlyrDeck[1],
                                                 player_cards])
                            #print('j')
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
            #except:
            #    print('Unknown Error')
            #    await asyncio.sleep(5)
            #    continue
        print('T')
        lResults = makeunique(lResults)
        print('U')
        cursor.executemany('''INSERT OR IGNORE INTO battles values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', lResults)
        print('V')
        cursor.executemany('''INSERT OR IGNORE INTO players values (?, ?, ?)''', lOppPlayerTags)
        print('W')
        lResults = []
        lOppPlayerTags = []
        conn.commit()
    print('ACTUALLY DONE')
    # add opposing players to database
    cursor.executemany('''INSERT OR IGNORE INTO battles values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', lResults)
    conn.commit()
    ldbplayers = [i[0] for i in cursor.execute('''SELECT player_tag FROM players''')]
    dbplayerssafter = len(ldbplayers)
    print('Added ' + str(dbplayerssafter - dbplayerssbefore) + ' opposing players to database, which now has ' + str(
        dbplayerssafter) + ' players.')
    cursor.close()
    conn.close()

    # Print unknown decks to CSV
    header_print('PRINTING UNKNOWN DECKS TO CSV', 100)
    print(len(lUnknownDecks), 'unknown decks.')
    arr_unique = makeunique_multi(lUnknownDecks)
    print(len(arr_unique), 'unique unknown decks.')
    arr_print = [i + [(lUnknownDecks.count(i))] for i in arr_unique]
    list.sort(arr_print, key=lambda arr_print: arr_print[len(arr_print) - 1], reverse=True)
    with open('unknown_decks.csv', 'w+', newline='') as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        try:
            csvWriter.writerows(arr_print)
        except:
            pass

    return lResults


async def waitplz():
    await asyncio.sleep(30)


def main(num_runs, b_update_databases, min_player_max_trophies, max_player_tags):
    try:
        while num_runs != 0:
            header_print('STARTING NEW RUN', 100)
            if b_update_databases:
                header_print('ADDING TOP PLAYERS', 100)
                get_top_players()
                header_print('ADDING CLANS', 100)
                add_clans()
                header_print('ADDING CLAN PLAYERS', 100)
                get_clan_players()
            # Select db clan players
            conn = sqlite3.connect(globals.databasename)
            cursor = conn.cursor()
            if max_player_tags > 0:
                sql_query_player = '''SELECT player_tag FROM players WHERE max_trophies >= %s ORDER BY update_date ASC LIMIT %s''' % (
                    min_player_max_trophies, max_player_tags)
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
            #test
            loop = asyncio.get_event_loop()
            loop.run_until_complete(battlefinder(lClanPlayersTags))
            #asyncio.run(battlefinder(lClanPlayersTags))
            cursor.close()
            conn.close()
            loop.close()
    except:
        pass


main(1, False, -1, -1)
# main(-1, True, 500000)

asyncio.run(waitplz())
print('Done!')
