import asyncio
import clashroyale
import sqlite3
import globals

globals.init()


async def get_players(cr, clan_groups):
    return await asyncio.gather(*[
        cr.get_player(*group)
        for group in clan_groups
    ])


async def get_players_max_trophies(max_players_to_update):
    # Get Client Objects
    officialClient = clashroyale.official_api.Client(globals.officialAPIToken, is_async=True, timeout=999)
    conn = sqlite3.connect(globals.databasename)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS players(
        player_tag TEXT,
        update_date TEXT,
        max_trophies TEXT,
        UNIQUE(player_tag));''')
    conn.commit()
    # Loop through the players, iMaxTags at a time
    iMaxTags = 1
    iMaxRate = 75
    if max_players_to_update > 0:
        lPlayersTags = [i[0] for i in cursor.execute(
            '''SELECT player_tag FROM players WHERE (max_trophies < 100 OR max_trophies IS NULL) AND length(player_tag) > 5 ORDER BY update_date ASC LIMIT %s''' % max_players_to_update)]
    else:
        lPlayersTags = [i[0] for i in cursor.execute(
            '''SELECT player_tag FROM players WHERE (max_trophies < 100 OR max_trophies IS NULL) AND length(player_tag) > 5 ORDER BY update_date ASC''')
                        if len(i[0]) > 5]
    print(lPlayersTags)
    if len(lPlayersTags) == 0:
        lPlayersTags = [i[0] for i in cursor.execute(
            '''SELECT player_tag FROM players WHERE (max_trophies < 100 OR max_trophies IS NULL) AND length(player_tag) > 5 ORDER BY update_date ASC LIMIT %s''' % max_players_to_update)]
    for iPlayerGroup in range(0, len(lPlayersTags), iMaxTags * iMaxRate):
        print('Player group', iPlayerGroup, '-', iPlayerGroup + iMaxTags * iMaxRate, 'out of', len(lPlayersTags))
        lPlayerGroup = [lPlayersTags[x:(x + iMaxTags)] for x in
                        range(iPlayerGroup, min(len(lPlayersTags), iPlayerGroup + iMaxTags * iMaxRate), iMaxTags)]
        while True:
            try:
                lAllPlayers = await get_players(officialClient, lPlayerGroup)
                await asyncio.sleep(2)
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
            except clashroyale.errors.NotFoundError:
                print('Not Found Error')
                await asyncio.sleep(10)
                break
            # loop through battles and add to array
            for lPlayers in lAllPlayers:
                cursor.execute("""UPDATE players
                                SET max_trophies=%s
                                WHERE player_tag=%s""" % (
                    lPlayers['bestTrophies'], '"' + lPlayers['tag'] + '"'))  # .replace('#', '')
            try:
                conn.commit()
            except:
                pass
            break
    await asyncio.sleep(10)
    conn.commit()
    cursor.close()
    conn.close()
    await officialClient.close()


# asyncio.run(get_players_max_trophies(0))
asyncio.run(get_players_max_trophies(500000))
