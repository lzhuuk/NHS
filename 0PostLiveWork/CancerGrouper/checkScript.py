'''
This is a script for checking the laterality in the resulted file.
It outputs terms which may not have corresponding left/right term.
'''

import xlrd, xlwt
import os, sys
import re

def main():

    current_path = os.path.abspath(__file__)
    os.chdir(os.path.dirname(current_path))

    print('Preparing table...')
    #loading data table
    excel1 = xlrd.open_workbook(\
    'results/Leileis cancer super grouper - v1.0 - keepOnly.xlsx')
    table1 = excel1.sheet_by_name(u'data')
    nameListIMO = table1.col_values(2)[1:]

    print('Saving results...')
    workbook = xlwt.Workbook(encoding = 'utf-8')
    worksheet = workbook.add_sheet('output_file')
    worksheet.write(0, 0, 'Flag')

    for i, name in enumerate(nameListIMO):
        # logic of laterality checking
        thisPass = True
        if re.search('left', name, re.I):
            if re.sub('left', 'right', name) in nameListIMO:
                pass
            else:
                thisPass = False
        if re.search('right', name, re.I):
            if re.sub('right', 'left', name) in nameListIMO:
                pass
            else:
                thisPass = False

        flag = ''
        if thisPass == False:
             flag = 'check'
             print(name)
        worksheet.write(i+1, 0, flag)

    workbook.save('results/Excel_test.xls')

if __name__ == '__main__':
    print('********** Scripts start. **********')
    main()
    print('********** Scripts end. **********')
