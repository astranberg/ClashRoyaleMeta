import globals

globals.init()


def deckprint(oDeck):
    for i in range(0, 8):
        print(oDeck[i]['name'])


def archetype(oDeck):
    lCards = [i['name'].lower() for i in oDeck]
    # print(lCards)
    for i in range(0, len(globals.l_arch)):
        if set(globals.l_include[i]).issubset(set(lCards)):  # if all include cards are found in deck
            # print('Match',lDeck[i],lCards)
            if len(set(globals.l_exclude[i]).intersection(lCards)) == 0:  # if no exclude cards are found in deck
                # FOUND A MATCH
                # print('Match',lDeck[i],lCards)
                return ([globals.l_arch[i], globals.l_deck[i], i])
    # print('Deck Not Found')
    # print([i['name'] for i in oDeck])
    return ([[''], '', (len(globals.l_deck))])
