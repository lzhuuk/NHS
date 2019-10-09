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
    worksheet.write(0, 0, 'Term')

    rowCount = 1
    for name in nameListIMO:
        if re.search('left', name, re.I):
            if re.sub('left', 'right', name) in nameListIMO:
                pass
            else:
                print(name)
                worksheet.write(rowCount, 0, name)
                rowCount += 1
        elif re.search('right', name, re.I):
            if re.sub('right', 'left', name) in nameListIMO:
                pass
            else:
                print(name)
                worksheet.write(rowCount, 0, name)
                rowCount += 1

    workbook.save('results/Excel_test.xls')

if __name__ == '__main__':
    print('********** Scripts start. **********')
    main()
    print('********** Scripts end. **********')
