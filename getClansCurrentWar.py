import asyncio
import random

import clashroyale
import sqlite3
import logging
import requests
from datetime import date
import globals

globals.init()

logging.basicConfig(level=logging.INFO)

# Define Tokens

officialAPIToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjYyNTgwNTVkLTAyMDMtNDFhOS05NTRjLWUwNjNmYzk1ZDQ0ZCIsImlhdCI6MTY1NTE1NDEwMSwic3ViIjoiZGV2ZWxvcGVyLzZlYmYzNzdmLWVkNjQtMmFlZC02MjRhLWE3Nzg5YmM4OGZiNCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3My43Ny41OC42MyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.4wG7WwYjTQQIkd5_czrhLtmh2str4V1OmPLdTSG2RIrMufqJfk_BYmmf_Xz98kASYUfCJxtygn3UuMFHR7y4SA"
api_key = {"Authorization": f"Bearer {officialAPIToken}"}


def getClanScore(json, clantag):
    for clan in json['clans']:
        if clan['tag'] == clantag:
            return clan['clanScore']


def getClanFame(json, clantag):
    for clan in json['clans']:
        if clan['tag'] == clantag:
            return clan['fame']


def getClanProgress(json, clantag):
    for clan in json['items']:
        if clan['clan']['tag'] == clantag:
            return clan['progressEndOfDay']


def getLastPeriodProgress(json, clantag):
    return getClanProgress(json, clantag)


def getClanRanked(json, rank):
    latestPeriod = json['periodLogs'][-1]
    for clan in latestPeriod['items']:
        clanrank = clan['endOfDayRank']
        if clanrank == rank:
            return clan['clan']['tag']


def getNumParticipants(json):
    count = 0
    for player in json['participants']:
        if player['fame'] > 0:
            count += 1
    return count


def sortByFame(e):
    return e['fame']


def sortByPoints(e):
    return e['periodPoints']


def sortByLastProgress(e):
    return e['progress']


def get_clan_players():
    # Add clan tags to database
    conn = sqlite3.connect(globals.databasename)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS players(
        player_tag TEXT,
        update_date TEXT,
        max_trophies TEXT,
        UNIQUE(player_tag));''')
    conn.commit()

    # Define Variables
    lClanPlayersTags = []
    iMaxTags = 1
    cr = clashroyale.official_api.Client(officialAPIToken, is_async=True, timeout=30)

    # loop through clans, iMaxTags at a time
    lClans = [i[0] for i in cursor.execute('''SELECT * FROM clans''')]
    lClans = [x for x in lClans if len(x) > 5]  # remove tags if 5 of less characters, as these will error
    random.shuffle(lClans)
    print('There are', len(lClans), 'clans in the database.')
    print("clantag|clanrank|clanprogress|periodindex|requiredtrophies|members")
    my_trophies = requests.get("https://api.clashroyale.com/v1/players/%23C899VP2", api_key).json()['trophies']
    for clan in lClans:
        # clan = "29Y82L0P"
        baseUrl = "https://api.clashroyale.com/v1/clans/"
        currentriverraceurl = "/currentriverrace"
        result = requests.get(baseUrl + "%23" + clan + currentriverraceurl, api_key)
        resultjson = result.json()
        if result.status_code == 200:
            state = resultjson['state']
            latestPeriod = resultjson['periodLogs'][-1]
            lastPeriodindex = latestPeriod['periodIndex']
            currPeriodindex = resultjson['periodIndex']
            bConsiderLastPeriod = (currPeriodindex == lastPeriodindex + 1)
            # print(bConsiderLastPeriod)

            lClans = []
            for clanjson in resultjson['clans']:
                lClans.append({'tag': clanjson['tag'], 'fame': int(clanjson['fame']),
                               'progress': int(getLastPeriodProgress(latestPeriod, clanjson['tag'])),
                               'score': int(clanjson['clanScore']),
                               'participants': int(getNumParticipants(clanjson))})
            lClans.sort(key=sortByFame, reverse=True)

            if lClans[0]['score'] > 3000:
                clandetailsresult = requests.get(baseUrl + "%23" + lClans[0]['tag'].replace("#", ""), api_key)
                clandetailsjson = clandetailsresult.json()
                members = clandetailsjson['members']
                requiredtrophies = clandetailsjson['requiredTrophies']
                admittype = clandetailsjson['type']
                if bConsiderLastPeriod:  # this skips last Progress Points sorting on Colliseum days.
                    lClans.sort(key=sortByLastProgress, reverse=True)
                fameDistance = lClans[0]['fame'] - lClans[1]['fame']
                progressDistance = lClans[0]['progress'] - lClans[1]['progress']
                # print(lClans)
                if members < 50 and requiredtrophies < my_trophies and admittype != 'closed':
                    if bConsiderLastPeriod:
                        print(lClans[0]['tag'], progressDistance, admittype, lClans[0]['participants'],
                              lClans[0]['progress'])
                    else:
                        print(lClans[0]['tag'], fameDistance, admittype, lClans[0]['participants'])

    conn.commit()
    cursor.close()
    conn.close()
    cr.close()


get_clan_players()
