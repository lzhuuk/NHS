'''
This is a script for selecting processing cancer super grouper file.
The objective is to only keep one IMO term for each SNOMED concept.
As a result, 5111 rows are selected from 48557 rows (the one with "Keep" flag).

Important Note:
The excel spreadsheet MUST be preprocessed before reading into this scripts.
This preprocessing includes:
1. Removing the inactive rows (i.e. EC_INACTIVE_YN is Y);
2. Sorting by CONCEPT_ID (either ascending or descending) with first priority,
and then RECORD_TYPE (must be descending order so that the "TERM" type appears
before the type "BOTH CODE AND TERM") with second priority.
3. Selecting only the rows where CONCEPT_LINE is 1, so that there is no multiple
mapping from a certain IMO term to different SNOMED concepts.
'''

import xlrd, xlwt
import os, sys
import re
import collections

def main():

    current_path = os.path.abspath(__file__)
    os.chdir(os.path.dirname(current_path))

    print('Preparing table...')
    #loading data table
    excel1 = xlrd.open_workbook(\
    'sources/Leileis cancer super grouper - SortedByCID_RTYPE and OnlyNotInactive and OnlyConceptLine1.xlsx')
    table1 = excel1.sheet_by_name(u'data')
    idListSNOMED_RAW = table1.col_values(10)[1:]
    nameListSNOMED = table1.col_values(12)[1:]
    nameListIMO = table1.col_values(2)[1:]


    # build a dictionary called dict
    # key is SNOMED ID, value is SNOMED NAME
    dict = collections.OrderedDict()
    for nameSNOMED, idSNOMED_RAW in zip(nameListSNOMED, idListSNOMED_RAW):
        idSNOMED = idSNOMED_RAW.replace('SNOMED#','').strip()
        if dict.get(idSNOMED) == None:
            dict[idSNOMED] = nameSNOMED
        elif dict[idSNOMED] != nameSNOMED:
            sys.exit(0)

    # build a dictionary called dict2
    # key is SNOMED ID, value is a list of related IMO NAMES
    dict2 = collections.OrderedDict()
    for idSNOMED_RAW, nameIMO in zip(idListSNOMED_RAW, nameListIMO):
        idSNOMED = idSNOMED_RAW.replace('SNOMED#','').strip()
        if dict2.get(idSNOMED) == None:
            dict2[idSNOMED] = []
        dict2[idSNOMED].append(nameIMO)

    # comparing each SNOMED NAME with its related IMO NAMES
    resultsList = []
    for idSNOMED, nameSublistIMO in dict2.items():
        nameSNOMED = dict[idSNOMED]
        thisResults = []
        for nameIMO in nameSublistIMO:
            # logic of calculating likehood ratio
            tempLikehood, tempWord = compute_likehood(nameSNOMED, nameIMO)
            if nameIMO == nameSNOMED:
                tempLikehood = 1.1
            elif tempLikehood < 1.0 and nameIMO == re.sub('\(.*\)', '', nameSNOMED).strip():
                tempLikehood = 0.99
            thisResults.append((tempLikehood,nameIMO))
        resultsList.append(thisResults)

    # generate a list of flag for selecting rows in Excel file
    flagList = []
    ratioList = []
    for thisResults in resultsList:
        # logic of giving a flag
        thisMax = max([elem[0] for elem in thisResults])
        foundOne = False
        for thisTuple in thisResults:
            thisFlag = 'Delete'
            if thisMax == thisTuple[0]:
                if foundOne == False:
                    thisFlag = 'Keep'
                    foundOne = True
                else:
                    thisFlag = 'Check'
            flagList.append(thisFlag)
            ratioList.append(thisTuple[0])


    #opening a new excel to save results
    print('Saving results...')
    workbook = xlwt.Workbook(encoding = 'utf-8')
    worksheet = workbook.add_sheet('output_file')
    worksheet.write(0, 0, 'Flag')
    worksheet.write(0, 1, 'Ratio')

    rowCount = 1
    for thisFlag, thisRatio in zip(flagList,ratioList):
        worksheet.write(rowCount, 0, thisFlag)
        worksheet.write(rowCount, 1, thisRatio)
        rowCount += 1

    workbook.save('results/Excel_test.xls')


def compute_likehood(term1,term2):
    term1=term1.lower()
    term2=term2.lower()

    word1,word2=process_data(term1,term2)

    likehood=0
    insection=check_insection(word1,word2)
    if(len(insection)==0):
        likehood=0
    else:
        word1_len=len(word1)
        word2_len=len(word2)
        insection_len=len(insection)
        if(word1_len>=word2_len):
            likehood=insection_len/word1_len
        else:
            likehood=insection_len/word2_len

    return likehood,word2


def check_insection(word1,word2):
    res=[]
    temp_set=set()
    for i in word1:
        temp_set.add(i)

    for ii in word2:
        if(ii in temp_set):
            #print(ii)
            res.append(ii)

    return res


def process_data(term1,term2):
    # 先去掉特殊符号,不留空
    special_charater1 = ['"', "+", "+/-", "&", "(", ")",","]
    for sc in special_charater1:
        term2 = term2.replace(sc, "")
        term1 = term1.replace(sc, "")
    # 去掉但是要留空的
    special_charater2 = [" - ", " / ","/", "  ", ]
    for sc2 in special_charater2:
        term2 = term2.replace(sc2, " ")
        term1 = term1.replace(sc2, " ")
    word1 = term1.replace('"', '').split(' ')  # 去除"且用空格分离
    word2 = term2.replace('"', '').split(' ')

    # 特殊字符加入一个set
    special_word = ['and', 'or', 'with', 'of', 'surgery', 'operation', 'special acharacters',
                    'space', 'test', 'treatment', 'examination', 'from', 'to', 'using', 'left',
                    'right', 'bilateral', 'yes/no','in','- uclh historical lab','uclh','for','procedure']
    special_word_set = set()
    for i in special_word:
        special_word_set.add(i)

    # 去除特殊字符
    for iii in word1:
        if (iii in special_word_set):
            word1.remove(iii)
        if (len(iii)==0):
            word1.remove(iii)
    for ii in word2:
        if (ii in special_word_set):
            word2.remove(ii)
        if (len(ii)==0):
            word2.remove(ii)

    #word1=list(set(word1))
    #word2=list(set(word2))
    return word1,word2

def preproc(term):
    term = term.replace('due to','')
    term = term.replace('caused by','')
    term = term.replace(':','')
    return term

if __name__ == '__main__':
    print('********** Scripts start. **********')
    main()
    print('********** Scripts end. **********')
