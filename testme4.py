from collections import Counter
import asyncio
import logging
import csv
import clashroyale
from collections import OrderedDict
from BattleInterpreter import archetype
from interpretbattles import battleDeckPrinter
import numpy

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
officialClient = clashroyale.official_api.Client(officialAPIToken, is_async=False)
unofficialClient = clashroyale.royaleapi.Client(unofficialAPIToken, is_async=False)

# Get the top x clans
lTopClans = officialClient.get_top_clans(57000249, limit=200)
print('Number of Clans:', len(lTopClans))

# Define Variables
lClanPlayersTags = []
iMaxTags = 25

# loop through clans, iMaxTags at a time
for iClanGroup in range(0, len(lTopClans), iMaxTags):
    lClanGroup = [i.tag.replace('#', '') for i in
                  lTopClans[iClanGroup:min(iClanGroup + iMaxTags, len(lTopClans))]]  # get next 25 (or max) clans
    lClanGroup = list(OrderedDict.fromkeys(lClanGroup))  # remove duplicate tags
    lClanGroup = [x for x in lClanGroup if len(x) > 5]  # remove tags if 5 of less characters, as these will error
    lClanGroupTags = officialClient.get_clan(*lClanGroup)  # get data from all clans,* iterates the list into args
    print(' Clan group', iClanGroup, 'has', len(lClanGroupTags), 'clans.')
    for clan in lClanGroupTags:  # loop through each clan in the response
        for members in clan['members']:  # loop through each member in a clan
            lClanPlayersTags.append(members['tag'].replace('#', ''))  # add each member's tag to a list

# Print the data
lClanPlayersTags = list(OrderedDict.fromkeys(lClanPlayersTags))  # removes duplicate tags
lClanPlayersTags = [x for x in lClanPlayersTags if
                    len(x) > 5]  # remove tags if 5 or less characters, as these will error
print('Unique Player Tags Found', len(lClanPlayersTags))
print('List', lClanPlayersTags)

# Define more variables
lBattles = []

lDeck = [['3M No Pump'], ['Balloon Cycle'], ['Balloon Freeze'], ['Bridge Spam'], ['Classic 3M Pump'], ['Classic bait'],
         ['Doulbe Prince'], ['EG Healer'], ['EG Sparky'], ['EGNW'], ['Giant 3M'], ['Giant Cycle'], ['Giant Dbl Prince'],
         ['Giant GY'], ['Giant Loon'], ['Giant Miner'], ['Giant Prince'], ['Giant Skele Clone'], ['Giant Sparky'],
         ['Goblin giant sparky'], ['Golem'], ['Golem Balloon'], ['Golem Lightning'], ['GY Control'], ['Hog 2.6'],
         ['Hog Bait'], ['Hog Cycle'], ['Hog EQ'], ['Hog mortar'], ['Hog mortar bait'], ['HogXNado'], ['Icebow'],
         ['LavaClone'], ['Lavaloon'], ['Lavaminer'], ['LJ Balloon'], ['Miner Bait'], ['Miner Balloon'], ['Miner cycle'],
         ['Miner Cycle'], ['Miner Hog'], ['Miner Poison'], ['Miner Rocket'], ['Miner WB'], ['MK bait'],
         ['MK Miner Control'], ['MK miner hog'], ['Mortar Miner Bait'], ['Noob Rage'], ['Pekka Miner'],
         ['Ram rider 3M Miner'], ['Ram Rider Spam'], ['RG'], ['Royal hogs'], ['Xbow 2.9'], ['Xbow Misc']]


def makeunique(l):
    res = []
    for i in l:
        if i in res:
            pass
        else:
            res.append(i)
    return res


def makeunique2(l):
    temp = Counter([tuple(sorted(x)) for x in l])
    z2 = [list(k) for k, v in temp.items() if v == 1]
    return z2


async def get_battles(cr, clan_groups):
    return await asyncio.gather(*[
        cr.get_player_battles(*group)
        for group in clan_groups
    ])


async def main():
    lResults = []
    unofficialClient = clashroyale.royaleapi.Client(unofficialAPIToken, is_async=True, timeout=100)
    # Loop through the players, iMaxTags at a time
    iMaxTags = 25
    iMaxRate = 8
    # for iPlayerGroup in range(0, len(lClanPlayersTags), iMaxTags):
    for iPlayerGroup in range(0, len(lClanPlayersTags), iMaxTags * iMaxRate):
        lPlayerGroup = [lClanPlayersTags[x:(x + iMaxTags)] for x in
                        range(iPlayerGroup, min(len(lClanPlayersTags), iPlayerGroup + iMaxTags * iMaxRate), iMaxTags)]
        # print('lPlayerGroup',lPlayerGroup)
        # get data from all players,* iterates the list into args
        # print(lClanPlayersTags[iPlayerGroup:min(iPlayerGroup + 25, len(lClanPlayersTags))])
        lAllPlayerBattles = await get_battles(unofficialClient, lPlayerGroup)
        await asyncio.sleep(5)
        print(' Player group', str(iPlayerGroup) + '/' + str(len(lClanPlayersTags)), 'has',
              sum([len(_) for _ in lAllPlayerBattles]), 'battles.')
        # lPlayerBattles = lPlayerBattles[0]
        # loop through battles and add to array
        for lPlayerBattles in lAllPlayerBattles:
            for i in range(0, len(lPlayerBattles)):
                # if any(lPlayerBattles[i]['utcTime'] in _ for _ in lResults if lPlayerBattles[i]['team'][0]['tag'] in _):
                #    print('Duplicate!',lPlayerBattles[i]['utcTime'] + lPlayerBattles[i]['team'][0]['tag'])
                # else:
                lPlyrDeck = archetype(lPlayerBattles[i]['team'][0]['deck'])
                lOppDeck = archetype(lPlayerBattles[i]['opponent'][0]['deck'])
                # print(lPlyrDeck)
                # print(lOppDeck)
                if lPlayerBattles[i]['winner'] > 0:
                    lResults.append([lPlayerBattles[i]['utcTime'], lPlayerBattles[i]['mode']['name'],
                                     lPlayerBattles[i]['team'][0]['tag'], lPlayerBattles[i]['team'][0]['startTrophies'],
                                     lPlayerBattles[i]['teamCrowns'], lPlyrDeck[0], lPlyrDeck[1],
                                     [z['name'].lower() for z in lPlayerBattles[i]['team'][0]['deck']],
                                     lPlayerBattles[i]['opponent'][0]['tag'],
                                     lPlayerBattles[i]['opponent'][0]['startTrophies'],
                                     lPlayerBattles[i]['opponentCrowns'], lOppDeck[0], lOppDeck[1],
                                     [z['name'].lower() for z in lPlayerBattles[i]['opponent'][0]['deck']]])
                    # lResults[lPlyrDeck[2]][lOppDeck[2]] = 1 + lResults[lPlyrDeck[2]][lOppDeck[2]]
                elif lPlayerBattles[i]['winner'] == 0:
                    pass
                    # print('draw:', lOppDeck[1], lPlayerBattles[i]['opponentCrowns'], lPlyrDeck[1],
                    # lPlayerBattles[i]['teamCrowns'])
                else:
                    # print('winner:', lOppDeck[1], lPlayerBattles[i]['opponentCrowns'], 'loser:', lPlyrDeck[1],
                    # lPlayerBattles[i]['teamCrowns'])
                    lResults.append([lPlayerBattles[i]['utcTime'], lPlayerBattles[i]['mode']['name'],
                                     lPlayerBattles[i]['opponent'][0]['tag'],
                                     lPlayerBattles[i]['opponent'][0]['startTrophies'],
                                     lPlayerBattles[i]['opponentCrowns'], lOppDeck[0], lOppDeck[1],
                                     [z['name'].lower() for z in lPlayerBattles[i]['opponent'][0]['deck']],
                                     lPlayerBattles[i]['team'][0]['tag'], lPlayerBattles[i]['team'][0]['startTrophies'],
                                     lPlayerBattles[i]['teamCrowns'], lPlyrDeck[0], lPlyrDeck[1],
                                     [z['name'].lower() for z in lPlayerBattles[i]['team'][0]['deck']]])
                    # lResults[lOppDeck[2]][lPlyrDeck[2]] = 1 + lResults[lOppDeck[2]][lPlyrDeck[2]]
    print('Removing duplicate battles.')
    battles_before = len(lResults)
    lResults = makeunique(lResults)
    battles_after = len(lResults)
    print('Removed', battles_before - battles_after, 'duplicate values!')
    print(str(battles_after) + '/' + str(battles_before) + ' battles remain!')
    print(lResults)
    return lResults


lResults = asyncio.run(main())
print('Done!')
with open('new_file.csv', 'w+', newline='') as my_csv:
    csvWriter = csv.writer(my_csv, delimiter=',')
    csvWriter.writerows(lResults)
battleDeckPrinter(lResults, 'ladder', 5500, 5800, 300, 3)
battleDeckPrinter(lResults, 'ladder', 4600, 8200, 600, 3)
battleDeckPrinter(lResults, 'ladder', 4600, 8200, 300, 3)
battleDeckPrinter(lResults, 'ladder', 4600, 8200, 3000, 3)
battleDeckPrinter(lResults, 'challenge', 4600, 8200, 3000, 3)


async def waitplz():
    await asyncio.sleep(30)


asyncio.run(waitplz())
