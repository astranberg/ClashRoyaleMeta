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

# Get the top x clans
lTopClans = officialClient.get_top_clans(57000249, limit=100)
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
    lClanGroupTags = unofficialClient.get_clan(*lClanGroup)  # get data from all clans,* iterates the list into args
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

lDeck = [['Bridge Spam'], ['EGNW'], ['EG Sparky'], ['Giant double prince'], ['Giant GY'], ['Giant Miner NW'],
         ['Giant cycle'], ['Giant sparky'], ['Giant 3M'], ['Goblin giant sparky'], ['Golem balloon'],
         ['Golem Lightning'], ['Golem NW'], ['GY Control'], ['Hog EQ'], ['HogXNado'], ['Hog mortar'],
         ['Hog mortar bait'], ['Hog 2.6'], ['LavaClone'], ['Lavaloon'], ['Lavaminer'], ['Mortar Miner Bait'],
         ['MK miner hog'], ['Miner Hog'], ['Miner Balloon'], ['Miner bait'], ['Miner cycle'], ['Miner WB'],
         ['MK Miner Control'], ['Pekka Miner'], ['Miner Poison'], ['Classic bait'], ['Ram Rider Spam'],
         ['Ram rider 3M Miner'], ['RG Furnace'], ['RG'], ['Royal hogs'], ['Xbow 2.9'], ['Icebow'], ['MK bait'],
         ['Balloon Freeze'], ['Classic 3M Pump'], ['Hog Rocket'], ['Noob Rage'], ['EG Healer'], ['Xbow Misc']]
lResults = []
a = ''

# Loop through the players, iMaxTags at a time
for iPlayerGroup in range(0, len(lClanPlayersTags), iMaxTags):
    # get data from all players,* iterates the list into args
    print(lClanPlayersTags[iPlayerGroup:min(iPlayerGroup + 25, len(lClanPlayersTags))])
    lPlayerBattles = unofficialClient.get_player_battles(*lClanPlayersTags[iPlayerGroup:min(iPlayerGroup + 25,
                                                                                            len(lClanPlayersTags))])
    print(' Player group', iPlayerGroup, 'has', len(lPlayerBattles), 'battles.')
    # loop through battles and add to array
    for i in range(0, len(lPlayerBattles)):
        if any(lPlayerBattles[i]['utcTime'] in _ for _ in lResults if lPlayerBattles[i]['team'][0]['tag'] in _):
            print('Duplicate!', lPlayerBattles[i]['utcTime'] + lPlayerBattles[i]['team'][0]['tag'])
        else:
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
                a = a
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
print('Done!', lResults)
with open('new_file.csv', 'w+', newline='') as my_csv:
    csvWriter = csv.writer(my_csv, delimiter=',')
    csvWriter.writerows(lResults)
battleDeckPrinter(lResults, 'ladder', 4600, 8200, 600, 3, 'LadderQ300')
battleDeckPrinter(lResults, 'ladder', 4600, 8200, 3000, 3, 'LadderALL')
battleDeckPrinter(lResults, 'challenge', 4600, 8200, 3000, 3, 'challenge')
