import logging

import PySimpleGUI as sg
import clashroyale
import requests
import speech_recognition as sr
from ThreadedFileLoader.ThreadedFileLoader import *

import globals

globals.init()
logging.basicConfig(level=logging.INFO)

# initialize the recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()


def process_card_name(card):
    return card.lower().replace("-", "").replace(".", "").replace("the", "").strip()


def get_card_elixir(card):
    return officialClient.get_card_info("Archers")['elixir']


def find_card_spoken(words, list_of_cards):
    words = [process_card_name(x) for x in words]
    list_of_cards = [process_card_name(x) for x in list_of_cards]
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
            member = [x for x in lMembers if x.name.lower() == sMember.lower()][0]
            memberTag = member.tag
            memberTrophies = member.trophies
            # print("")
            print(memberTag, memberTrophies)
        except:
            memberTag = ""
        if memberTag != "" and abs(memberTrophies - myTrophies) < 200:
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
            return memberTag, lBattles, [x.icon_urls.medium for x in lDeck], [x.name.lower() for x in lDeck]
            exit()


def getLastDeck(lBattles):
    for battle in lBattles:
        if battle.deckSelection == "collection":
            # print(battle)
            lDeck = battle.team[0].cards
            print(lDeck)
            return lDeck
            exit()


def getLastMatchingDeck(lBattles, lKnownCards):
    for battle in lBattles:
        if battle.deckSelection == "collection":
            # print(battle)
            lDeck = battle.team[0].cards
            lDeck_names_only = [process_card_name(x.name) for x in lDeck]
            bMatches = True
            for card in lKnownCards:
                if not card in lDeck_names_only:
                    bMatches = False
                    print("Deck doesn't match", lDeck_names_only)
                    break
            if bMatches:
                print("Deck matches!", lDeck_names_only)
                return [x.icon_urls.medium for x in lDeck], lDeck_names_only
                exit()


def imageFromUrl(url):
    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    return response.raw.read()


def getDeckUlrs(lDeck):
    urls = []
    for card in lDeck:
        if card == "unknown":
            urls.append(unknown_card)
        else:
            i = all_cards.index(card)
            urls.append(all_card_urls[i])
    return urls

def createGUI():
    while True:
        # Create an input dialogue for inputting opponent name and opponent clan name
        layout = [
            [sg.Text("Userame"), sg.InputText("", key='member')],
            [sg.Text("Clan"), sg.InputText("", key='clan')],
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
        if event == "Close":
            exit()
        else:
            if member_name == "" or clan_name == "":
                bNoDeckMatch = True
                oppTag = ""
                oppBattles = []
                opponents_deck = []
                for i in range(0, 8):
                    opponents_deck.append("unknown")
                urls = getDeckUlrs(opponents_deck)
                print(opponents_deck)
                print(urls)
                lOppDeck = [imageFromUrl(urls[0]), imageFromUrl(urls[1]), imageFromUrl(urls[2]), imageFromUrl(urls[3]),
                            imageFromUrl(urls[4]), imageFromUrl(urls[5]), imageFromUrl(urls[6]), imageFromUrl(urls[7])]
            else:
                bNoDeckMatch = False
                oppTag, oppBattles, urls, opponents_deck = get_top_players(clan_name, member_name)
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
                    # reset known cards in deck
                    lKnownCards = []
                    # mic stuff
                    r.adjust_for_ambient_noise(source)
                    while True:
                        # read the audio data from the default microphone
                        print('speak!')
                        audio_data = r.listen(source, timeout=0)
                        # convert speech to text, then try to find the card spoken
                        try:
                            text = r.recognize_google(audio_data, show_all=True)
                            words = [process_card_name(x['transcript']) for x in text['alternative']]
                            # print(text)
                            print(words)
                            card_spoken = find_card_spoken(words, opponents_deck)
                        except:
                            words = []
                            card_spoken = ""
                        if card_spoken != "":
                            if card_spoken == "log":
                                card_spoken = "the log"
                            # move card to end
                            urls.append(urls.pop(
                                opponents_deck.index(card_spoken)))  # doesn't do anything just staying consistent
                            lOppDeck.append(lOppDeck.pop(opponents_deck.index(card_spoken)))
                            opponents_deck.append(opponents_deck.pop(opponents_deck.index(card_spoken)))
                            if card_spoken in lKnownCards:
                                lKnownCards.append(lKnownCards.pop(lKnownCards.index(card_spoken)))
                            print(urls)
                            print(opponents_deck)
                            updateCardOrder(opponent_window, lOppDeck)
                            opponent_window.refresh()
                        elif "quit" in words:
                            quit()
                        elif "next game" in words:
                            break
                        else:
                            print('here')
                            card_maybe_spoken = find_card_spoken(words, all_cards)
                            if len(card_maybe_spoken) > 0 and card_maybe_spoken not in lKnownCards:
                                lKnownCards.append(card_maybe_spoken)
                                print("a", lKnownCards)
                                print(opponents_deck)
                                if bNoDeckMatch:
                                    urls = []
                                    opponents_deck = []
                                else:
                                    try:
                                        urls, opponents_deck = getLastMatchingDeck(oppBattles, lKnownCards)
                                    except:
                                        urls = []
                                        opponents_deck = []
                                if len(opponents_deck) > 0:
                                    print("pizza")
                                    print(urls)
                                    print(opponents_deck)
                                    lOppDeck = [imageFromUrl(urls[0]), imageFromUrl(urls[1]), imageFromUrl(urls[2]),
                                                imageFromUrl(urls[3]),
                                                imageFromUrl(urls[4]), imageFromUrl(urls[5]), imageFromUrl(urls[6]),
                                                imageFromUrl(urls[7])]
                                    # move card to end
                                    urls.append(urls.pop(
                                        opponents_deck.index(
                                            card_maybe_spoken)))  # doesn't do anything just staying consistent
                                    lOppDeck.append(lOppDeck.pop(opponents_deck.index(card_maybe_spoken)))
                                    opponents_deck.append(opponents_deck.pop(opponents_deck.index(card_maybe_spoken)))
                                    # update screen
                                    updateCardOrder(opponent_window, lOppDeck)
                                else:
                                    # We now have a custom made deck, with no known match
                                    bNoDeckMatch = True
                                    opponents_deck = lKnownCards[:]
                                    while len(opponents_deck) < 8:
                                        opponents_deck.insert(0, "unknown")
                                    urls = getDeckUlrs(opponents_deck)
                                    print(opponents_deck)
                                    print(urls)
                                    lOppDeck = [imageFromUrl(urls[0]), imageFromUrl(urls[1]), imageFromUrl(urls[2]),
                                                imageFromUrl(urls[3]),
                                                imageFromUrl(urls[4]), imageFromUrl(urls[5]), imageFromUrl(urls[6]),
                                                imageFromUrl(urls[7])]
                                    # move card to end
                                    urls.append(urls.pop(
                                        opponents_deck.index(
                                            card_maybe_spoken)))  # doesn't do anything just staying consistent
                                    lOppDeck.append(lOppDeck.pop(opponents_deck.index(card_maybe_spoken)))
                                    opponents_deck.append(opponents_deck.pop(opponents_deck.index(card_maybe_spoken)))
                                    lKnownCards.append(lKnownCards.pop(lKnownCards.index(card_maybe_spoken)))
                                    # update screen
                                    updateCardOrder(opponent_window, lOppDeck)

                        # gui stuff, prevent it from freezing
                        opponent_window.refresh()

            opponent_window.close()


def updateCardOrder(window, deck):
    for i in range(4):
        window[i].update(data=deck[i], subsample=2)
    for i in range(4, 8):
        window[i].update(data=deck[i], subsample=3)


use_mic = True
self_tag = "%23C899VP2"
officialClient = clashroyale.official_api.Client(globals.officialAPIToken)

mySelf = officialClient.get_player(self_tag)
myTrophies = mySelf.trophies

unknown_card: str = "https://pngimg.com/uploads/question_mark/question_mark_PNG38.png"

print(officialClient.get_all_cards())
all_cards = [process_card_name(x['name']) for x in officialClient.get_all_cards()]
all_card_urls = [x['iconUrls']['medium'] for x in officialClient.get_all_cards()]
# all_card_images = [imageFromUrl(x) for x in all_card_urls]
# all_card_images.append(imageFromUrl(unknown_card))

createGUI()
