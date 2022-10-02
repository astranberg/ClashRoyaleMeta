import time

import clashroyale
import logging
import speech_recognition as sr
import requests
import globals
import PySimpleGUI as sg
import pandas as pd
import csv

globals.init()
logging.basicConfig(level=logging.INFO)

# initialize the recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

use_mic = True
self_tag = "%23C899VP2"
officialClient = clashroyale.official_api.Client(globals.officialAPIToken)

cs = pd.read_csv("card_stats.csv", index_col=0).transpose().to_dict(orient='series')

print(cs['Fireball']['TowerDamage' + '14'])


# cs = pd.read_csv(r"card_stats.csv").to_dict()
# print(cardstats["fireball"])
# print(cs.values["Archers"])

def find_card_spoken(words, list_of_cards):
    words = [x.lower().replace("-", "").replace("the", "").strip() for x in words]
    list_of_cards = [x.lower().replace("-", "").replace("the", "").strip() for x in list_of_cards]
    for word in words:
        if word in list_of_cards:
            print(word)
            return word
    return ""


def get_top_players(sClan, sMember):
    # Get Client Objects

    lClans = officialClient.search_clans(name=sClan)
    lClans = [x for x in lClans if x.name.lower() == sClan.lower()]
    # print([x.name for x in lClans])

    memberTag = ""
    print("%s clans found" % len(lClans))
    for clan in lClans:
        lMembers = officialClient.get_clan_members(clan.tag)
        # print("="*100)
        print([x.name for x in lMembers])
        try:
            memberTag = [x for x in lMembers if x.name.lower() == sMember.lower()][0].tag
            # print("")
            # print(memberTag)
        except:
            memberTag = ""
        if memberTag != "":
            print("Found member ""%s"" (%s) in clan ""%s"" (%s)" % (sMember, memberTag, sClan, clan.tag))
            lBattles = officialClient.get_player_battles(memberTag)
            lDeck = getLastDeck(lBattles)
            # for battle in lBattles:
            #    if battle.deckSelection == "collection":
            #        #print(battle)
            #        lDeck = battle.team[0].cards
            #        print(lDeck)
            lCards = [x.name + " (" + str(14 + x.level - x.maxLevel) + ")" for x in lDeck]
            print("")
            print(lCards)
            return [x.icon_urls.medium for x in lDeck], [x.name.lower() for x in lDeck]
            exit()


def getLastDeck(lBattles):
    for battle in lBattles:
        if battle.deckSelection == "collection":
            # print(battle)
            lDeck = battle.team[0].cards
            print(lDeck)
            return lDeck
            exit()


def imageFromUrl(url):
    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    return response.raw.read()


def createGUI():
    while True:
        # Create an input dialogue for inputting opponent name and opponent clan name
        layout = [
            [sg.Text("Userame"), sg.InputText("good knight", key='member')],
            [sg.Text("Clan"), sg.InputText("bad boyz club", key='clan')],
            [sg.Button("Search"), sg.Button("Close")]]
        input_window = sg.Window(title="Opponent Finder", layout=layout, margins=(100, 50), finalize=True)
        input_window["clan"].bind("<Return>", "_Enter")
        while True:
            event, values = input_window.read()
            if event == "Close" or event == sg.WINDOW_CLOSED:
                exit()
            elif event == "Search":
                break
            elif event == "clan" + "_Enter":
                break
        input_window.close()
        member_name = values['member']
        clan_name = values['clan']
        # Check that user actually submitted something, otherwise exit program
        if member_name == "" or clan_name == "" or event == "Close":
            exit()
        else:
            urls, opponents_deck = get_top_players(clan_name, member_name)
            print(urls)
            print(opponents_deck)
            lOppDeck = [imageFromUrl(urls[0]), imageFromUrl(urls[1]), imageFromUrl(urls[2]), imageFromUrl(urls[3]),
                        imageFromUrl(urls[4]), imageFromUrl(urls[5]), imageFromUrl(urls[6]), imageFromUrl(urls[7])]
            layout = [
                [sg.Text("Opponent: %s" % member_name)],
                [sg.Text("Clan: %s" % clan_name)],
                [sg.Image(data=lOppDeck[0], subsample=2, key=0), sg.Image(data=lOppDeck[1], subsample=2, key=1),
                 sg.Image(data=lOppDeck[2], subsample=2, key=2), sg.Image(data=lOppDeck[3], subsample=2, key=3)],
                [sg.Image(data=lOppDeck[4], subsample=3, key=4, pad=28),
                 sg.Image(data=lOppDeck[5], subsample=3, key=5, pad=27),
                 sg.Image(data=lOppDeck[6], subsample=3, key=6, pad=27),
                 sg.Image(data=lOppDeck[7], subsample=3, key=7, pad=28)],
                [sg.Button("Next Game")],
                [sg.Button("Quit")]]
            opponent_window = sg.Window(title="Opponents Deck", layout=layout, margins=(100, 50), finalize=True)
            opponent_window.refresh()
            time.sleep(1)
            # move card to end
            card = "archers"
            urls.append(urls.pop(opponents_deck.index(card)))  # doesn't do anything just staying consistent
            lOppDeck.append(lOppDeck.pop(opponents_deck.index(card)))
            opponents_deck.append(opponents_deck.pop(opponents_deck.index(card)))
            print(urls)
            print(opponents_deck)
            updateCardOrder(opponent_window, lOppDeck)
            opponent_window.refresh()
            time.sleep(1)
            opponent_window.refresh()
            if not use_mic:
                # Wait for button clicks
                while True:
                    try:
                        event, values = opponent_window.read()
                    except:
                        break
                    if event == "Next Game" or event == "Next Game" + "_Enter":
                        break
                    if event == "Quit" or event == sg.WINDOW_CLOSED:
                        exit()
                # breaks the outer loop too
                if event == "Quit":
                    exit()
            else:
                # Start speech recognition!
                with mic as source:
                    # mic stuff
                    r.adjust_for_ambient_noise(source)
                    while True:
                        # read the audio data from the default microphone
                        print('speak!')
                        audio_data = r.listen(source, timeout=0)
                        # convert speech to text, then try to find the card spoken
                        try:
                            text = r.recognize_google(audio_data, show_all=True)
                            words = [x['transcript'].lower() for x in text['alternative']]
                            # print(text)
                            print(words)
                            card_spoken = find_card_spoken(words, opponents_deck)
                        except:
                            words = []
                            card_spoken = ""
                        if card_spoken == "" and "quit" in words:
                            quit()
                        elif card_spoken == "" and "next game" in words:
                            break

                        # gui stuff, prevent it from freezing
                        opponent_window.refresh()

            opponent_window.close()


def updateCardOrder(window, deck):
    for i in range(4):
        window[i].update(data=deck[i], subsample=2)
    for i in range(4, 8):
        window[i].update(data=deck[i], subsample=3)


lDeck = getLastDeck(officialClient.get_player_battles(self_tag))
lCards = [x.name + " (" + str(14 + x.level - x.maxLevel) + ")" for x in lDeck]
lCardLevels = [(14 - x.maxLevel + x.level) for x in lDeck]
print(cs['Archers']['Type'])
lDeck2 = [x for x in cs if cs[x]['Type'] == "spell"]

print(lDeck2)
# print(lCards)

# print([x.name for x in officialClient.get_all_cards()])

# createGUI()

# get_top_players("knights radiant", "Josh")

# ideas - utilize spells in MY deck to show what combination of spells kills opponent cards
