import xlrd, xlwt
import os, sys
import SaveResults as SR

def main():

    current_path = os.path.abspath(__file__)
    os.chdir(os.path.dirname(current_path))

    # read master file
    excel1 = xlrd.open_workbook(\
    'sources/Prefcard fuzzy match - AddingIDsWithDuplicationsV0-16092019-update.xlsx')
    table1 = excel1.sheet_by_name('WholeTable')
    cardIdListEpic = table1.col_values(0)[1:]
    procedureIdListAll = table1.col_values(10)[1:]
    procedureIdListDup = table1.col_values(13)[1:]

    # preprocessing
    cardIdListEpic = [id.replace('M-','') for id in cardIdListEpic]
    procedureIdListAll = [idEntryProc(item) for item in procedureIdListAll]
    procedureIdListDup = [idEntryProc(item) for item in procedureIdListDup]

    # build mapping from index to cardId
    dict_cardId_index = {}
    for i, cardId in enumerate(cardIdListEpic):
        if dict_cardId_index.get(cardId) != None:
            sys.exit('KEY CONFLICT @ cardIdListEpic')
        dict_cardId_index[cardId] = i


    # exclude all the duplications
    procedureIdListPure = []
    for item1, item2 in zip(procedureIdListAll, procedureIdListDup):
        thisItem = []
        for id in item1:
            if id not in item2:
                thisItem.append(id)
        procedureIdListPure.append(thisItem)
    # print(procedureIdListPure)

    # add auto-review1 results
    table2 = excel1.sheet_by_name('DuplicationsPart2')
    for i in range(1, table2.nrows):
        thisRow = table2.row_values(i)
        thisCardId = thisRow[0].replace('M-','')
        thisProcId = thisRow[10]
        thisFlag = thisRow[12]
        if thisFlag == 'Keep':
            thisIndex = dict_cardId_index[thisCardId]
            procedureIdListPure[thisIndex].append(thisProcId)

    # add auto-review2 results
    excel2 = xlrd.open_workbook(\
    'sources/Prefcard fuzzy match - AddingIDsWithDuplicationsV0-19092019-rawSplit.xlsx')
    table3 = excel2.sheet_by_name('toKeep')
    for i in range(1, table3.nrows):
        thisRow = table3.row_values(i)
        thisCardId = thisRow[0].replace('M-','')
        thisProcId = thisRow[10]
        if True:
            thisIndex = dict_cardId_index[thisCardId]
            procedureIdListPure[thisIndex].append(thisProcId)

    # add manual review results
    excel3 = xlrd.open_workbook(\
    'sources/review-LeileiAlexa-03102019 - noFillOnly - doublecheck-Leilei 08102019 - edited.xlsx')
    table4 = excel3.sheet_by_name('Final')
    for i in range(1, table4.nrows):
        thisRow = table4.row_values(i)
        thisCardId = thisRow[0].replace('M-','')
        thisProcId = thisRow[10]
        if True:
            thisIndex = dict_cardId_index[thisCardId]
            procedureIdListPure[thisIndex].append(thisProcId)

    # print(procedureIdListPure)

    SR.saveResults(procedureIdListPure, True)


def idEntryProc(item):
    tempList = []
    try:
        theseId = item.split('\n')
    except:
        if type(item) == float:
            tempList.append(str(item).replace('.0','').strip())
        else:
            sys.exit('ERROR: ' + str(item))
    else:
        for id in theseId:
            if id.strip() != '':
                tempList.append(id.strip())
    return tempList


if __name__ == '__main__':
    print('********** Scripts start. **********')
    main()
    print('********** Scripts end. **********')
