import operator
import functools
import xlsxwriter
from datetime import datetime
import globals

globals.init()


def sumproduct(*lists):
    return sum(functools.reduce(operator.mul, data) for data in zip(*lists))


lTabColors = ['#E6B8B7', '#CCC0DA', '#92CDDC', '#FABF8F', '#8DB4E2', '#C4BD97']


def battleDeckPrinter(lOriginalBattles, type, bottomT, topT, trophystep, maxAgeDays):
    if trophystep == 0:
        trophystep = topT - bottomT
    # Define XLSX workbook and format variables
    globals.init()
    workbookname = type + str(bottomT) + "-" + str(topT) + "Q" + str(trophystep) + 'last' + str(maxAgeDays) + "days"
    wb = xlsxwriter.Workbook(workbookname + '.xlsx')
    percentformat = wb.add_format()
    percentformat.set_num_format('0.00%')
    headerformat = wb.add_format({'align': 'center', 'bold': True})
    headerformat.set_bottom(6)
    headerformat.set_left(1)
    headerformat.set_right(1)
    percentformatRborder = wb.add_format()
    percentformatRborder.set_num_format('0.00%')
    percentformatRborder.set_right(1)
    lborder = wb.add_format()
    lborder.set_left(1)
    topborder = wb.add_format()
    topborder.set_top(1)
    boldformat = wb.add_format({'bold': True})
    boldformatalignright = wb.add_format({'align': 'right', 'bold': True})
    # Make master worksheet
    masterws = wb.add_worksheet('Summary')
    masterws.set_tab_color('#8DB4E2')
    mastercol = 1
    masterws.write(1, 0, 'Misc', boldformatalignright)
    for i in range(len(globals.l_arch)):
        masterws.write(i + 2, 0, globals.l_deck[i], boldformatalignright)
    l_unique_deck = list(set(globals.l_deck))
    for i in range(len(l_unique_deck)):
        masterws.write(i + 2, 0, l_unique_deck[i], boldformatalignright)
    masterws.set_column(0, 0, 19)
    for minT in range(bottomT, topT, trophystep):
        maxT = minT + trophystep
        # Filter the battles based on parameters given
        lBattles = [i for i in lOriginalBattles if i[3] >= minT and i[3] <= maxT and i[1].lower() == type.lower()]
        # Filter based on how old the battles are
        lBattles = [i for i in lBattles if
                    (datetime.now() - datetime.strptime(i[0], "%Y-%m-%dT%H:%M:%SZ")).days <= maxAgeDays]
        # Get the unique archetypes present in these battles
        lArchetypes = [_[6] for _ in lBattles]
        lArchetypes.extend(_[12] for _ in lBattles)
        lArchetypes = list(set(_ for _ in lArchetypes))
        # Create lists with correct sizes
        lWinTable = [[0.500] * len(lArchetypes) for _ in range(len(lArchetypes))]
        lArchPrevalence = [0] * len(lArchetypes)
        if len(lArchetypes) == 0:
            pass
        else:
            # Create the win table
            for archwinner in lArchetypes:
                try:
                    lArchPrevalence[lArchetypes.index(archwinner)] = len(
                        [_ for _ in lBattles if _[6] == archwinner]) + len(
                        [_ for _ in lBattles if _[12] == archwinner])
                except:
                    lArchPrevalence[lArchetypes.index(archwinner)] = 0
                for archloser in lArchetypes:
                    try:
                        lWinTable[lArchetypes.index(archwinner)][lArchetypes.index(archloser)] = len(
                            [(i) for i in lBattles if i[6] == archwinner and i[12] == archloser]) / (len(
                            [(i) for i in lBattles if i[6] == archwinner and i[12] == archloser]) + len(
                            [(i) for i in lBattles if i[12] == archwinner and i[6] == archloser]))
                    except:
                        lWinTable[lArchetypes.index(archwinner)][lArchetypes.index(archloser)] = 0.500
            # Viability is the sum product of the win percentage and the prevalence of the archetype
            lViability = [sumproduct(lArchPrevalence, lWinTable[i]) for i in range(len(lArchetypes))]
            # Create a new worksheet
            ws = wb.add_worksheet('T' + str(minT) + '-' + str(maxT))
            ws.set_tab_color(lTabColors[int(((minT - bottomT) / trophystep) % (len(lTabColors)))])
            ws.set_column('A:A', 18)
            # ws.set_row('1',20)
            rowoffset = len(lArchetypes) + 3  # the rowoffset for the next table
            ws.write(rowoffset - 1, 1, 'Prevalence', boldformat)
            ws.write(rowoffset - 1, 2, 'Meta Score', boldformat)
            for i in range(len(globals.l_deck) + 1):
                for i in range(len(l_unique_deck) + 1):
                    masterws.write(i + 1, mastercol, '', lborder)
                    masterws.write(i + 1, mastercol + 1, '', percentformatRborder)
            for i in range(len(lArchetypes)):
                # writing headers
                if len(lArchetypes[i]) > 0:
                    ws.write(0, i + 1, lArchetypes[i], boldformat)
                    ws.write(i + 1, 0, lArchetypes[i], boldformat)
                    ws.write(rowoffset + i, 0, lArchetypes[i], boldformat)
                else:
                    ws.write(0, i + 1, 'Misc', boldformat)
                    ws.write(i + 1, 0, 'Misc', boldformat)
                    ws.write(rowoffset + i, 0, 'Misc', boldformat)
                # write the archetypes matchup win percentage table
                for j in range(len(lArchetypes)):
                    ws.write(i + 1, j + 1, lWinTable[i][j])
                # write the prevalence of each archetype in a table below it
                ws.write(rowoffset + i, 1, lArchPrevalence[i])
                ws.write(rowoffset + i, 2, (lViability[i] / len(lBattles)) - 1, percentformat)
                if len(lArchetypes[i]) > 0:
                    masterws.write(globals.l_deck.index(lArchetypes[i]) + 2, mastercol, lArchPrevalence[i], lborder)
                    masterws.write(globals.l_deck.index(lArchetypes[i]) + 2, mastercol + 1,
                                   (lViability[i] / len(lBattles)) - 1,
                                   masterws.write(l_unique_deck.index(lArchetypes[i]) + 2, mastercol,
                                                  lArchPrevalence[i], lborder)
                    masterws.write(l_unique_deck.index(lArchetypes[i]) + 2, mastercol + 1,
                                   (lViability[i] / len(lBattles)) - 1,
                                   percentformatRborder)
                    else:
                    masterws.write(1, mastercol, lArchPrevalence[i], lborder)
                    masterws.write(1, mastercol + 1, (lViability[i] / len(lBattles)) - 1, percentformatRborder)
                    masterws.write(len(globals.l_arch) + 2, mastercol, '', topborder)
                    masterws.write(len(globals.l_arch) + 2, mastercol + 1, '', topborder)
                    masterws.set_column(mastercol, mastercol, 2)
                    masterws.set_column(mastercol, mastercol, 5.5)
                    masterws.merge_range(0, mastercol, 0, mastercol + 1, ws.name, headerformat)
                    mastercol += 2
                    ws.conditional_format(rowoffset, 2, rowoffset + len(lArchetypes), 2, {'type': '3_color_scale',
                                                                                          'mid_type': 'num',
                                                                                          'mid_value': 0,
                                                                                          'mid_color': '#FFFFFF'})
                    for i in range(2, mastercol, 2):
                        masterws.conditional_format(1, i, 1 + len(globals.l_deck), i, {'type': '3_color_scale',
                                                                                       'mid_type': 'num',
                                                                                       'mid_value': 0,
                                                                                       'mid_color': '#FFFFFF'})
                    for i in range(1, mastercol, 2):
                        masterws.conditional_format(1, i, 1 + len(l_unique_deck), i, {'type': '3_color_scale',
                                                                                      'mid_type': 'num',
                                                                                      'mid_value': 200,
                                                                                      'mid_color': '#FFFFFF',
                                                                                      'max_color': '#FFFFFF'})
                    masterws.conditional_format(1, i + 1, 1 + len(l_unique_deck), i + 1, {'type': '3_color_scale',
                                                                                          'mid_type': 'num',
                                                                                          'mid_value': 0,
                                                                                          'mid_color': '#FFFFFF'})

                    wb.close()
                    print('Completed', workbookname)
