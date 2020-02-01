import operator
import functools
import xlsxwriter
from datetime import datetime


def sumproduct(*lists):
    return sum(functools.reduce(operator.mul, data) for data in zip(*lists))


lArch = [['Dual Lane', '3M'], ['Balloon', 'Cycle'], ['Balloon', 'Freeze'], ['Bridge Spam'],
         ['Beatdown', 'Dual Lane', '3M'], ['Bait'], ['Controll'], ['Beatdown'], ['Beatdown', 'Elixir Golem'],
         ['Beatdown', 'Elixir Golem'], ['Beatdown', 'Giant', 'Dual Lane'], ['Giant', 'Cycle'], ['Beatdown', 'Giant'],
         ['Beatdown', 'Graveyard', 'Giant'], ['Giant', 'Balloon'], ['Beatdown', 'Giant', 'Miner', 'Cycle'],
         ['Giant', 'Control'], ['Clone'], ['Beatdown', 'Giant'], ['Beatdown', 'Goblin Giant'], ['Beatdown', 'Golem'],
         ['Beatdown', 'Balloon', 'Golem'], ['Beatdown', 'Golem'], ['Graveyard', 'Control'], ['Hog', 'Cycle'],
         ['Hog', 'Bait', 'Cycle'], ['Hog', 'Cycle'], ['Hog', 'Cycle'], ['Hog', 'Siege'],
         ['Hog', 'Siege', 'Bait', 'Cycle'], ['Hog', 'Control'], ['Siege'], ['Beatdown', 'Lavahound'],
         ['Beatdown', 'Balloon'], ['Beatdown', 'Miner'], ['Balloon', 'Cycle'], ['Miner', 'Bait'],
         ['Miner', 'Cycle', 'Balloon'], ['Miner', 'Control'], ['Miner', 'Cycle'], ['Hog', 'Miner'],
         ['Miner', 'Control', 'Cycle'], ['Miner', 'Cycle'], ['Miner', 'Cycle'], ['Bait', 'Control'],
         ['Miner', 'Control'], ['Hog', 'Miner'], ['Siege', 'Miner', 'Bait'], ['Rage'], ['Miner', 'Control'],
         ['Bridge Spam', 'Beatdown', 'Dual Lane'], ['Bridge Spam'], ['Royale giant'], ['Dual Lane'], ['Siege'],
         ['Siege']]
lDeck = [['3M No Pump'], ['Balloon Cycle'], ['Balloon Freeze'], ['Bridge Spam'], ['Classic 3M Pump'], ['Classic bait'],
         ['Doulbe Prince'], ['EG Healer'], ['EG Sparky'], ['EGNW'], ['Giant 3M'], ['Giant Cycle'], ['Giant Dbl Prince'],
         ['Giant GY'], ['Giant Loon'], ['Giant Miner'], ['Giant Prince'], ['Giant Skele Clone'], ['Giant Sparky'],
         ['Goblin giant sparky'], ['Golem'], ['Golem Balloon'], ['Golem Lightning'], ['GY Control'], ['Hog 2.6'],
         ['Hog Bait'], ['Hog Cycle'], ['Hog EQ'], ['Hog mortar'], ['Hog mortar bait'], ['HogXNado'], ['Icebow'],
         ['LavaClone'], ['Lavaloon'], ['Lavaminer'], ['LJ Balloon'], ['Miner Bait'], ['Miner Balloon'], ['Miner cycle'],
         ['Miner Cycle'], ['Miner Hog'], ['Miner Poison'], ['Miner Rocket'], ['Miner WB'], ['MK bait'],
         ['MK Miner Control'], ['MK miner hog'], ['Mortar Miner Bait'], ['Noob Rage'], ['Pekka Miner'],
         ['Ram rider 3M Miner'], ['Ram Rider Spam'], ['RG'], ['Royal hogs'], ['Xbow 2.9'], ['Xbow Misc']]
lInclude = [['three musketeers'], ['balloon'], ['balloon', 'freeze'], ['battle ram', 'p.e.k.k.a'],
            ['three musketeers', 'elixir collector'], ['goblin barrel'], ['prince', 'dark prince'],
            ['elixir golem', 'healer'], ['elixir golem', 'sparky'], ['elixir golem', 'night witch'],
            ['giant', 'three musketeers'], ['giant'], ['giant', 'dark prince', 'prince'], ['giant', 'graveyard'],
            ['giant', 'balloon'], ['giant', 'miner'], ['giant', 'prince'], ['giant skeleton', 'clone'],
            ['giant', 'sparky'], ['goblin giant', 'sparky'], ['golem'], ['golem', 'balloon'], ['golem', 'lightning'],
            ['graveyard'], ['hog rider', 'musketeer', 'ice spirit', 'skeletons', 'fireball'],
            ['hog rider', 'goblin barrel'], ['hog rider'], ['hog rider', 'earthquake'], ['hog rider', 'mortar'],
            ['hog rider', 'mortar', 'goblin barrel'], ['hog rider', 'executioner', 'tornado'], ['x-bow', 'ice wizard'],
            ['lava hound', 'clone'], ['lava hound', 'balloon'], ['lava hound', 'miner'], ['balloon', 'lumberjack'],
            ['miner', 'goblin barrel'], ['miner', 'balloon'], ['miner', 'valkyrie'], ['miner', 'skeletons'],
            ['miner', 'hog rider'], ['miner', 'poison'], ['miner', 'rocket'], ['miner', 'wall breakers'],
            ['mega knight', 'goblin barrel'], ['miner', 'mega knight'], ['mega knight', 'miner', 'hog rider'],
            ['mortar', 'miner', 'goblin gang'], ['rage', ' elite barbarians'], ['p.e.k.k.a', 'miner'],
            ['ram rider', 'three musketeers', 'miner'], ['ram rider'], ['royal giant'], ['royal hogs'],
            ['x-bow', 'archers'], ['x-bow']]
lExclude = [['elixir collector'], ['lavahound', 'miner'], [''], [''], [''],
            ['giant', 'hog rider', 'lavahound', 'mortar'], ['giant', 'hog rider', 'lavahound', 'balloon'], [''], [''],
            ['sparky'], [''], ['miner', 'balloon', 'prince'], [''], [''], [''], [''], ['dark prince'], [''], [''], [''],
            ['lightning', 'balloon'], [''], [''], ['giant', 'golem'], [''], [''],
            ['goblin barrel', 'mortar', 'executioner'], [''], ['goblin barrel'], [''], [''], [''], [''], ['miner'],
            [''], [''], ['mortar', 'hog rider'], ['lava hound'], ['wall breakers'],
            ['giant', 'hog rider', 'lavahound', 'balloon'], ['mega knight'], ['wall breakers'], [''], ['mega knight'],
            [''], [''], [''], [''], ['balloon'], [''], [''], [''], [''], [''], [''], ['ice wizard', 'archers']]


def battleDeckPrinter(lOriginalBattles, type, bottomT, topT, trophystep, maxAgeDays):
    workbookname = type + str(bottomT) + "-" + str(topT) + "Q" + str(trophystep) + 'last' + str(maxAgeDays) + "days"
    wb = xlsxwriter.Workbook(workbookname + '.xlsx')
    for minT in range(bottomT, topT, trophystep):
        maxT = minT + trophystep
        # Filter the battles based on parameters given
        lBattles = [i for i in lOriginalBattles if i[3] >= minT and i[3] <= maxT and i[1].lower() == type.lower()]
        # Filter based on how old the battles are
        lBattles = [i for i in lBattles if
                    (datetime.now() - datetime.strptime(i[0], "%Y-%m-%dT%H:%M:%SZ")).days <= maxAgeDays]
        # Get the unique archetypes present in these battles
        lArchetypes = list(set(_[6][0] for _ in lBattles))
        lArchetypes.extend(list(set(_[12][0] for _ in lBattles)))
        lArchetypes = list(set(_ for _ in lArchetypes))
        # Create lists with correct sizes
        lWinTable = [[0.500] * len(lArchetypes) for _ in range(len(lArchetypes))]
        lArchPrevalence = [0] * len(lArchetypes)
        # Create the win table
        for archwinner in lArchetypes:
            try:
                lArchPrevalence[lArchetypes.index(archwinner)] = len(
                    [_ for _ in lBattles if _[6][0] == archwinner]) + len(
                    [_ for _ in lBattles if _[12][0] == archwinner])
            except:
                lArchPrevalence[lArchetypes.index(archwinner)] = 0
            for archloser in lArchetypes:
                try:
                    lWinTable[lArchetypes.index(archwinner)][lArchetypes.index(archloser)] = len(
                        [(i) for i in lBattles if i[6][0] == archwinner and i[12][0] == archloser]) / (len(
                        [(i) for i in lBattles if i[6][0] == archwinner and i[12][0] == archloser]) + len(
                        [(i) for i in lBattles if i[12][0] == archwinner and i[6][0] == archloser]))
                except:
                    lWinTable[lArchetypes.index(archwinner)][lArchetypes.index(archloser)] = 0.500
        # Viability is the sum product of the win percentage and the prevalence of the archetype
        lViability = [sumproduct(lArchPrevalence, lWinTable[i]) for i in range(len(lArchetypes))]
        # Create a new worksheet
        ws = wb.add_worksheet('T' + str(minT) + '-' + str(maxT))
        ws.set_column('A:A', 18)
        # ws.set_row('1',20)
        bold = wb.add_format({'bold': True})
        rowoffset = len(lArchetypes) + 3  # the rowoffset for the next table
        ws.write(rowoffset - 1, 1, 'Prevalence', bold)
        ws.write(rowoffset - 1, 2, 'Meta Score', bold)
        for i in range(len(lArchetypes)):
            # writing headers
            if len(lArchetypes[i]) > 0:
                ws.write(0, i + 1, lArchetypes[i], bold)
                ws.write(i + 1, 0, lArchetypes[i], bold)
                ws.write(rowoffset + i, 0, lArchetypes[i], bold)
            else:
                ws.write(0, i + 1, 'Misc', bold)
                ws.write(i + 1, 0, 'Misc', bold)
                ws.write(rowoffset + i, 0, 'Misc', bold)
            # write the archetypes matchup win percentage table
            for j in range(len(lArchetypes)):
                ws.write(i + 1, j + 1, lWinTable[i][j])
            # write the prevalence of each archetype in a table below it
            ws.write(rowoffset + i, 1, lArchPrevalence[i])
            ws.write(rowoffset + i, 2, lViability[i] / len(lBattles))
        ws.conditional_format(rowoffset, 2, rowoffset + len(lArchetypes), 2, {'type': '3_color_scale',
                                                                              'mid_type': 'num',
                                                                              'mid_value': 1.0,
                                                                              'mid_color': '#FFFFFF'})
        # print(len(lBattles),minT,maxT)
    wb.close()
