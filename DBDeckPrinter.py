import sqlite3
import operator
import functools
import xlsxwriter
import globals

globals.init()


def sumproduct(*lists):
    return sum(functools.reduce(operator.mul, data) for data in zip(*lists))


lTabColors = ['#E6B8B7', '#CCC0DA', '#92CDDC', '#FABF8F', '#8DB4E2', '#C4BD97']


def battleDeckPrinter(battle_type, min_trophies, max_trophies, trophystep, max_battle_age_hours):
    # Connect to DB and select appropriate battles based on constraints argued
    conn = sqlite3.connect('clans.db')
    cursor = conn.cursor()
    lOriginalBattles = [list(i) for i in cursor.execute(
        '''SELECT * FROM battles WHERE datetime(battle_time) > datetime('now', '-%s Hour') AND 
        winner_trophies BETWEEN %s AND %s AND 
        loser_trophies BETWEEN %s AND %s AND 
        battle_type like "%s"''' % (
            max_battle_age_hours, min_trophies, max_trophies, min_trophies, max_trophies, '%' + battle_type + '%'))]
    cursor.close()
    conn.close()
    # Hard coded if trophy step is 0 then we look at all battles at once
    if trophystep == 0:
        trophystep = max_trophies - min_trophies
    # Initiate the global variables
    globals.init()
    # Define XLSX workbook
    workbookname = battle_type + str(min_trophies) + "-" + str(max_trophies) + "Q" + str(trophystep) + 'last' + str(
        max_battle_age_hours) + "hours"
    wb = xlsxwriter.Workbook(workbookname + '.xlsx')
    print('Starting on workbook', workbookname)
    # Declare format variables for XLSX
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
    # Get a list of unique decks, since there are multiple definitions for some deck names
    l_unique_deck = list(set(globals.l_deck))
    # Write the deck names into the master worksheet
    for i in range(len(l_unique_deck)):
        masterws.write(i + 2, 0, l_unique_deck[i], boldformatalignright)
    masterws.set_column(0, 0, 19)
    # Loop through each bracket of trophies
    for minT in range(min_trophies, max_trophies, trophystep):
        maxT = minT + trophystep - (minT + trophystep < max_trophies)  # -1 if not the last trophy range
        # Filter the battles based on parameters given
        lBattles = [i for i in lOriginalBattles if
                    minT <= i[3] <= maxT and minT <= i[6] <= maxT]  # i[3] and i[6] are winner and loser trophies
        # Get the unique archetypes present in these battles
        l_trophyrange_archetypes = [_[4] for _ in lBattles]
        l_trophyrange_archetypes.extend(_[7] for _ in lBattles)
        l_trophyrange_archetypes = list(set(_ for _ in l_trophyrange_archetypes))
        # Create lists for win percentages and the prevalence of each archetype in this trophy range
        lWinTable = [[0.500] * len(l_trophyrange_archetypes) for _ in range(len(l_trophyrange_archetypes))]
        lArchPrevalence = [0] * len(l_trophyrange_archetypes)
        if len(l_trophyrange_archetypes) == 0:
            pass
        else:
            # Create the win table
            for archwinner in l_trophyrange_archetypes:
                try:
                    lArchPrevalence[l_trophyrange_archetypes.index(archwinner)] = len(
                        [_ for _ in lBattles if _[4] == archwinner]) + len(
                        [_ for _ in lBattles if _[7] == archwinner])
                except:
                    lArchPrevalence[l_trophyrange_archetypes.index(archwinner)] = 0
                for archloser in l_trophyrange_archetypes:
                    try:
                        lWinTable[l_trophyrange_archetypes.index(archwinner)][
                            l_trophyrange_archetypes.index(archloser)] = len(
                            [(i) for i in lBattles if i[4] == archwinner and i[7] == archloser]) / (len(
                            [(i) for i in lBattles if i[4] == archwinner and i[7] == archloser]) + len(
                            [(i) for i in lBattles if i[7] == archwinner and i[4] == archloser]))
                    except:
                        lWinTable[l_trophyrange_archetypes.index(archwinner)][
                            l_trophyrange_archetypes.index(archloser)] = 0.500
            # Viability is the sum product of the win percentage and the prevalence of the archetype
            lViability = [sumproduct(lArchPrevalence, lWinTable[i]) for i in range(len(l_trophyrange_archetypes))]
            # Create a new worksheet for trophy range
            ws = wb.add_worksheet('T' + str(minT) + '-' + str(maxT))
            ws.set_tab_color(lTabColors[int(((minT - min_trophies) / trophystep) % (len(lTabColors)))])
            ws.set_column('A:A', 18)
            rowoffset = len(l_trophyrange_archetypes) + 3  # the rowoffset for the summary table, it's row 1
            ws.write(rowoffset - 1, 1, 'Prevalence', boldformat)
            ws.write(rowoffset - 1, 2, 'Meta Score', boldformat)
            # Write headers to master sheet - this matters because in the given trophy range some decks may not be
            # present and the ws would otherwise be missing the |border| formatting
            for i in range(len(l_unique_deck) + 1):
                masterws.write(i + 1, mastercol, '', lborder)
                masterws.write(i + 1, mastercol + 1, '', percentformatRborder)
            # Write to trophy-range specific sheet
            for i in range(len(l_trophyrange_archetypes)):
                # writing headers to trophy specific sheet
                if len(l_trophyrange_archetypes[i]) > 0:
                    ws.write(0, i + 1, l_trophyrange_archetypes[i], boldformat)
                    ws.write(i + 1, 0, l_trophyrange_archetypes[i], boldformat)
                    ws.write(rowoffset + i, 0, l_trophyrange_archetypes[i], boldformat)
                else:
                    ws.write(0, i + 1, 'Misc', boldformat)
                    ws.write(i + 1, 0, 'Misc', boldformat)
                    ws.write(rowoffset + i, 0, 'Misc', boldformat)
                # write the archetypes match-up win percentage table
                for j in range(len(l_trophyrange_archetypes)):
                    ws.write(i + 1, j + 1, lWinTable[i][j])
                # write the prevalence of each archetype in a table below it
                ws.write(rowoffset + i, 1, lArchPrevalence[i])
                ws.write(rowoffset + i, 2, (lViability[i] / len(lBattles)) - 1, percentformat)
                # Write data to master sheet
                if len(l_trophyrange_archetypes[i]) > 0:
                    try:
                        masterws.write(l_unique_deck.index(l_trophyrange_archetypes[i]) + 2, mastercol,
                                       lArchPrevalence[i],
                                       lborder)
                        masterws.write(l_unique_deck.index(l_trophyrange_archetypes[i]) + 2, mastercol + 1,
                                       (lViability[i] / len(lBattles)) - 1,
                                       percentformatRborder)
                    except:
                        pass
                else:
                    masterws.write(1, mastercol, lArchPrevalence[i], lborder)
                    masterws.write(1, mastercol + 1, (lViability[i] / len(lBattles)) - 1, percentformatRborder)
            masterws.write(len(l_unique_deck) + 2, mastercol, '', topborder)  # placing bottom border on the last row
            masterws.write(len(l_unique_deck) + 2, mastercol + 1, '', topborder)
            masterws.set_column(mastercol, mastercol, 6.0)
            masterws.merge_range(0, mastercol, 0, mastercol + 1, ws.name, headerformat)
            mastercol += 2
            ws.conditional_format(rowoffset, 2, rowoffset + len(l_trophyrange_archetypes), 2, {'type': '3_color_scale',
                                                                                               'mid_type': 'num',
                                                                                               'mid_value': 0,
                                                                                               'mid_color': '#FFFFFF'})
    # add conditional formatting to main worksheet
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

    masterws.freeze_panes(1, 1)
    wb.close()
    print('Completed with %s battles analyzed!' % len(lOriginalBattles))


battleDeckPrinter('ladder', 6000, 6900, 300, 72)
# battleDeckPrinter('ladder', 4600, 8200, 600, 72)
# battleDeckPrinter('ladder', 4600, 8200, 0, 24)
# battleDeckPrinter('grand', 5500, 9000, 0, 72)
# battleDeckPrinter('classic', 5500, 9000, 0, 72)
