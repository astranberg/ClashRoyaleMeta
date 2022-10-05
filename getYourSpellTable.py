import json
import logging

import PySimpleGUI as sg
import clashroyale
import pandas as pd
import requests
import speech_recognition as sr

import globals

globals.init()
logging.basicConfig(level=logging.INFO)

# initialize the recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

# Read the card stats CSV into a dicitonary
cs = json.loads(requests.get(r"https://royaleapi.github.io/cr-api-data/json/cards_stats.json").text)
pd.json_normalize(cs)
print(cs["projectile"])


def findSpellDamage(spell, level, building=True):
    spell += "Spell"
    for card in cs['projectile']:
        print(card)
        if spell in card['name']:
            print(card['name'])
            if building:
                dmg = (int(card['damage_per_level'][level]) * 0.3 + 0.49999).__round__(0)
            else:
                dmg = card['damage_per_level'][level]
            return dmg
            break


print(findSpellDamage("Arrows", 10))
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


# Get your deck!
self_tag = "%23C899VP2"
officialClient = clashroyale.official_api.Client(globals.officialAPIToken)
lDeck = getLastDeck(officialClient.get_player_battles(self_tag))
lCards = [x.name + " (" + str(14 + x.level - x.maxLevel) + ")" for x in lDeck]
lCardLevels = [(14 - x.maxLevel + x.level) for x in lDeck]

# Get info about your spells and their tower damage
spell_names = [x for x in cs if cs[x]['Type'] == "spell" and x in [y.name for y in lDeck]]
spell_level = [(14 - x.maxLevel + x.level) for x in lDeck if x.name in spell_names]
spell_towerdamage = [cs[spell_names[i]]['TowerDamage' + str(spell_level[i])] for i in range(len(spell_names))]
all_cards = officialClient.get_all_cards()
spell_icons = [imageFromUrl(x.icon_urls.medium) for x in all_cards if x.name in spell_names]

print(spell_names)
print(spell_level)
print(spell_towerdamage)
# print(spell_icons)

# Make spell tower damage info into a useful table
spell_table = []
layout = []
for x in range(len(spell_names)):
    spell_table.append([spell_names[x], spell_towerdamage[x]])
    layout.append([sg.Image(data=spell_icons[x], subsample=4), sg.Text(spell_towerdamage[x])])
    for y in range(len(spell_names)):
        spell_table.append([spell_names[x] + " + " + spell_names[y], spell_towerdamage[x] + spell_towerdamage[y]])
        layout.append([sg.Image(data=spell_icons[x], subsample=4), sg.Image(data=spell_icons[y], subsample=4),
                       sg.Text(spell_towerdamage[x] + spell_towerdamage[y])])

layout = []
header = []
for i in range(len(spell_names)):
    header.append(sg.Image(data=spell_icons[i], subsample=4))
layout.append([header])
for j in range(len(spell_names)):
    for i in range(len(spell_names)):
        dmg = spell_towerdamage[i] + spell_towerdamage[j]
    layout.append([sg.Image(data=spell_icons[j], subsample=4), sg.Text(dmg)])

print(spell_table)

layout.append([sg.Button("Quit")])
spell_window = sg.Window(title="Spell Combos", layout=layout, margins=(100, 50), finalize=True).read()
