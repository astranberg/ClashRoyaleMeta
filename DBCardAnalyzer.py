import sqlite3
import operator
import functools
import xlsxwriter
import globals
import clashroyale

globals.init()

deck_printer_path = "F:\Dropbox\Games\crmeta\\"


def sumproduct(*lists):
    return sum(functools.reduce(operator.mul, data) for data in zip(*lists))


lTabColors = ['#E6B8B7', '#CCC0DA', '#92CDDC', '#FABF8F', '#8DB4E2', '#C4BD97']


def card_analyzer(battle_type, min_trophies, max_trophies, max_battle_age_hours):
    # Connect to DB and select appropriate battles based on constraints argued
    conn = sqlite3.connect(globals.databasename)
    cursor = conn.cursor()
    # Hard coded if trophy step is 0 then we look at all battles at once
    # Initiate the global variables
    globals.init()
    # Define XLSX workbook
    workbookname = "CardAnalyzer-" + battle_type + str(min_trophies) + "-" + str(max_trophies) + 'last' + str(
        max_battle_age_hours) + "hours"
    wb = xlsxwriter.Workbook(deck_printer_path + workbookname + '.xlsx')
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
    # Get a list of unique cards, since there are multiple definitions for some deck names
    l_cards = getCards()
    # FIXME
    # Write the deck names into the master worksheet
    for i in range(len(l_cards)):
        masterws.write(i + 1, 0, l_cards[i], boldformatalignright)
        masterws.write(0, i + 1, l_cards[i], boldformatalignright)
    masterws.set_column(0, 0, 19)  # width
    #        # Get unique deck lists used in each deck
    #        l_trophyrange_deck_lists = [x[5] for x in lBattles if x[4] == deck_name]
    #        l_trophyrange_deck_lists.extend(x[9] for x in lBattles if x[8] == deck_name)
    #        l_trophyrange_deck_lists = list(set(x for x in l_trophyrange_deck_lists))
    wsCount = 0
    print(list(set(globals.l_deck)))
    for deck_type in list(set(globals.l_deck)):
        print('Archetype: %s' % deck_type)
        # get battles list
        lBattlesWinners = [list(i) for i in cursor.execute(
            '''
            SELECT * FROM battles
            WHERE datetime(battle_time) > datetime('now', '-%s Hour') AND 
            winner_trophies BETWEEN %s AND %s AND 
            loser_trophies BETWEEN %s AND %s AND  
            battle_type like "%s" AND 
            winner_decktype == "%s"
            ''' % (
                max_battle_age_hours, min_trophies, max_trophies, min_trophies, max_trophies, '%' + battle_type + '%',
                deck_type))]
        lBattlesLosers = [list(i) for i in cursor.execute(
            '''
            SELECT * FROM battles
            WHERE datetime(battle_time) > datetime('now', '-%s Hour') AND 
            winner_trophies BETWEEN %s AND %s AND 
            loser_trophies BETWEEN %s AND %s AND  
            battle_type like "%s" AND 
            loser_decktype == "%s"
            ''' % (
                max_battle_age_hours, min_trophies, max_trophies, min_trophies, max_trophies, '%' + battle_type + '%',
                deck_type))]
        if len(lBattlesWinners) + len(lBattlesLosers) == 0:
            continue
        # make worksheet for archetype
        ws = wb.add_worksheet(deck_type)
        ws.set_tab_color(lTabColors[wsCount])
        wsCount += 1
        if wsCount >= len(lTabColors):
            wsCount = 0
        ws.set_column('A:A', 19)
        numBaseWinners = len(lBattlesWinners)
        numBaseLosers = len(lBattlesLosers)
        baseWinpercentage = numBaseWinners / (numBaseWinners + numBaseLosers)
        # conditional format
        ws.conditional_format(1, 1, 1 + len(l_cards), 1, {'type': '3_color_scale',
                                                          'mid_type': 'num',
                                                          'mid_value': (baseWinpercentage),
                                                          'mid_color': '#FFFFFF',
                                                          'max_color': '#50B000'})
        # Make table array
        arrTable = [["" for x in range(len(l_cards) + 2)] for x in range(len(l_cards) + 1)]  # swap +1 +2 ? #debugme
        # Write the deck names into rows/columns
        for i in range(len(l_cards)):
            ws.write(i + 1, 0, l_cards[i], boldformatalignright)
            ws.write(0, i + 1, l_cards[i], boldformatalignright)
            arrTable[0][i + 1] = l_cards[i]
            arrTable[i + 1][0] = l_cards[i]
        # test writing to worksheet
        #        print(arrTable)
        #        for r in range(len(arrTable)):
        #            for c in range(len(arrTable)):
        #                print(r, c, arrTable[r][c])
        #                if r == 1 or c == 1:
        #                    ws.write(r, c, arrTable[r][c], boldformatalignright)
        #                if r == len(arrTable) or c == len(arrTable):
        #                    ws.write(r, c, arrTable[r][c], percentformatRborder)
        #                else:
        #                    ws.write(r, c, arrTable[r][c], percentformat)
        #        wb.close()
        #        quit()
        for i in range(len(l_cards)):  # col
            l_i_BattlesWinners = [x for x in lBattlesWinners if l_cards[i] in x[5].split(",")]
            l_i_BattlesLosers = [x for x in lBattlesLosers if l_cards[i] in x[9].split(",")]
            numBattlesWinners = len(l_i_BattlesWinners)
            numBattlesLosers = len(l_i_BattlesLosers)
            try:
                winpercent = numBattlesWinners / (numBattlesWinners + numBattlesLosers)
            except:
                winpercent = 0
            arrTable[i + 1][-1] = winpercent  # the None row
            bWroteAnyInColumn = False
            for j in range(i, len(l_cards)):  # row
                # Get battles from database
                if i != j:
                    l_ij_BattlesWinners = [x for x in l_i_BattlesWinners if l_cards[j] in x[5].split(",")]
                    l_ij_BattlesLosers = [x for x in l_i_BattlesLosers if l_cards[j] in x[9].split(",")]
                else:
                    l_ij_BattlesWinners = l_i_BattlesWinners
                    l_ij_BattlesLosers = l_i_BattlesLosers
                numBattlesWinners = len(l_ij_BattlesWinners)
                numBattlesLosers = len(l_ij_BattlesLosers)
                print("     %s & %s: %s/%s" % (
                    l_cards[i], l_cards[j], numBattlesWinners, int(numBattlesWinners) + int(numBattlesLosers)))
                if numBattlesWinners + numBattlesLosers == 0:
                    winpercent = 0
                elif (numBattlesWinners + numBattlesLosers) / (numBaseWinners + numBaseLosers) < 0.05:
                    winpercent = 0
                else:
                    winpercent = numBattlesWinners / (numBattlesWinners + numBattlesLosers)
                    arrTable[j + 1][
                        i + 1] = winpercent  # "%s | %s/%s (r%s x c%s)" % (winpercent, numBattlesWinners, int(numBattlesWinners) + int(numBattlesLosers), l_cards[j], l_cards[i])

        # write to worksheet
        print(arrTable)
        columnCorrection = 0
        writeCol = 2
        for r in range(1, len(arrTable)):
            # write col A:A headers
            ws.write(r, 0, arrTable[0][r], boldformatalignright)
            # write col B:B single card win percentage
            ws.write(r, 1, arrTable[r][-1], boldformatalignright)
            # determine if col is worth writing (has data)
            bColumnHasData = False
            for c in range(len(arrTable)):
                if arrTable[r][c] != '' and 1 < c < len(arrTable[r]) and r != c:
                    bColumnHasData = True
                    print("%s has data (%s) [%s, %s]" % (arrTable[r][0], arrTable[r][c], r, c))
                    break
            if bColumnHasData:
                # write col header in row 1
                ws.write(0, writeCol, arrTable[0][r], boldformat)
                # iterate through results
                for c in range(1, len(arrTable[1]) - 1):
                    if arrTable[r][c] != '':
                        ws.write(c, writeCol, arrTable[r][c], percentformat)
                        ws.write_comment(c, writeCol, "r%s/c%s" % (arrTable[0][c], arrTable[0][r]))
                writeCol += 1

        # write conditional formatting
        for r in range(len(arrTable)):
            # ws.write(r, 0, arrTable[0][r], boldformatalignright)
            if r > 0:
                ws.write(r, 1, arrTable[r][-1], percentformat)  # this is only one single
                # print("condformat: %s" % arrTable[r][-1])
                ws.conditional_format(r, 2, r, 1 + len(l_cards), {'type': '3_color_scale',
                                                                  'mid_type': 'num',
                                                                  'mid_value': (arrTable[r][-1]),
                                                                  'mid_color': '#FFFFFF',
                                                                  'max_color': '#50B000'})
        # for i in range(len(arrTable[1]) - columnCorrection, len(arrTable[1])):
        #    ws.write(0, i, '')

        # write last few touches
        ws.write(0, 1, "None", boldformatalignright)
        ws.write(0, 0, baseWinpercentage, percentformat)
        ws.freeze_panes(1, 2)
    ##
    cursor.close()
    conn.close()

    wb.close()
    print('Completed deck analysis!')
    quit()


def getCards():
    # Define Tokens
    officialAPIToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9" \
                       ".eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImYyZjUzYmI2LWIyMDQtNGRkYi1" \
                       "iMGZjLTk0ZTE4ZWU3YzQ2ZSIsImlhdCI6MTU3NDYxNDgzMywic3ViIjoiZGV2ZWxvcGVyLzZlYmYzNzdmLWVkNjQtMmFlZC0" \
                       "2MjRhLWE3Nzg5YmM4OGZiNCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZl" \
                       "ciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI5OC4xOTUuMTU5LjgyIl0sInR5cGUiOiJjbGllbnQifV19.H13g" \
                       "VRs6fkSDyKEAAqPJKscx2AtN9sDbHaWNm2GSpgVZTTAe_sJM_yKkibMTCyOLu8kvOw7xcCOxycIydqqeUw "
    officialClient = clashroyale.official_api.Client(officialAPIToken)
    l_cards = [x.name for x in officialClient.get_all_cards()]
    print(l_cards)
    return l_cards


card_analyzer('ladder', 5600, 7400, 72)
