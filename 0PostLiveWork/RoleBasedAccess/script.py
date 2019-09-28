import pandas as pd
import os, sys
import re
import TemplateTools as TT

def main():

    current_path = os.path.abspath(__file__)
    os.chdir(os.path.dirname(current_path))

    df_SER_raw_whole = pd.read_excel('sources/SER20190809.xlsx', sheet_name='SER export', header=[4])
    df_ESR_raw_whole = pd.read_excel('sources/Data Source 1- Main.xlsx', sheet_name='Data', header=[0])

    df_ESR_raw = df_ESR_raw_whole[df_ESR_raw_whole['Staff Group'].isin(['Medical and Dental', 'Students'])]

    columnNames_SER = ['Provider name', 'External Name', 'Sex', \
    'Rpt Grp One', 'Provider type', 'Provider specialty', \
    'Rpt Grp Six', 'MPI ID-Type', 'MPI ID']
    columnNames_ESR = ['SER File Name', 'SER External Name', 'Gender', \
    'Employee Number', 'Assignment No.', 'Position Title', 'Role', 'Area Of Work', \
    'Org L2', 'Org L3', 'Org L4', 'Org L5', \
    'Professional Registration Num']

    df_SER = df_SER_raw_whole[columnNames_SER]
    df_ESR = df_ESR_raw[columnNames_ESR]

    df_SER['Rpt Grp One'] = df_SER['Rpt Grp One'].apply(cleanID)
    df_ESR['Employee Number'] = df_ESR['Employee Number'].apply(cleanID)

    dupIndicated = df_SER.duplicated('Rpt Grp One', keep=False)
    df_SER_dup = df_SER[dupIndicated]
    df_SER = df_SER[~dupIndicated]

    dupIndicated = df_ESR.duplicated('Employee Number', keep=False)
    df_ESR_dup = df_ESR[dupIndicated]
    df_ESR = df_ESR[~dupIndicated]

    res = pd.merge(df_SER, df_ESR, \
    left_on=['Rpt Grp One'], right_on=['Employee Number'], \
    how='outer', indicator=True, validate='one_to_one')

    res_both = res[res['_merge'].isin(['both'])]
    res_SER = res[res['_merge'].isin(['left_only'])]
    res_ESR = res[res['_merge'].isin(['right_only'])]

    res_SER = res_SER[columnNames_SER]
    res_ESR = res_ESR[columnNames_ESR]

    res_both['IfHasThisRegNumInSER'] = res_both.apply(lambda row: \
    checkID( \
    str(row['MPI ID']), str(row['Professional Registration Num']) \
    ), axis=1)

    res_both_HasRegNum = res_both[res_both['IfHasThisRegNumInSER'].isin([True])]

    res_both['TemplateGene'] = res_both.apply(lambda row: \
    TT.getTemplateIndirect( \
    str(row['Position Title']) + ' ' + \
    str(row['Role']) + ' ' + str(row['Area Of Work']) \
    , str(row['Org L5'])
    ), axis=1)

    res_both['IsSameTemplate'] = res_both.apply(lambda row: \
    str(row['TemplateGene']) == str(row['Rpt Grp Six']), axis=1)

    res_both = res_both[[
    'Provider name', 'External Name', 'Sex', \
    'Provider type', 'Provider specialty', \
    'Rpt Grp One', 'MPI ID-Type', 'MPI ID', \
    'Rpt Grp Six', 'TemplateGene', 'IsSameTemplate', \
    'SER File Name', 'SER External Name', 'Gender',
    'Position Title', 'Role', 'Area Of Work', \
    'Org L2', 'Org L3', 'Org L4', 'Org L5', \
    'Assignment No.', 'Employee Number', 'Professional Registration Num', \
    'IfHasThisRegNumInSER' \
    ]]

    summary = pd.Series([ \
    'Input source files: ' + 'SER ({} entires), ESR ({} entires)'.format(len(df), len(df2)),
    'Choose the subset of ESR ({} entires): '.format(len(df3)) + '"Medical and Dental", "Students" in "Staff Group"',
    'Match on the key "Employee Number" (deleted digits after "-"): ' + '"Rpt Grp One" (in SER), "Employee Number" (in ESR)',
    'Remove duplicated entries (i.e. same key multiple entries) as shown in two tabs: ' \
    + 'SER_DUP ({} entires), ESR_DUP ({} entires)'.format(len(df_SER_dup), len(df_ESR_dup)),
    'Join non-duplicated entries which results in three tabs: ' \
    + 'IN_BOTH ({} entires), SER_ONLY ({} entires), ESR_ONLY ({} entires)'.format(len(res_both), len(res_SER), len(res_ESR)),
    'Add "IfHasThisRegNumInSER" Column (to the tab IN_BOTH): ' \
    + 'True ({}/{}={}% entires) if "Professional Registration Num" (ESR) in "MPI ID" (SER)'\
    .format(len(res_both_HasRegNum), len(res_both), round(100*len(res_both_HasRegNum)/len(res_both),2) ),
    ])

    summary.name = 'Analysis Process'

    with pd.ExcelWriter('results/output.xlsx') as writer:
        res_both.to_excel(writer, sheet_name='IN_BOTH')
        res_SER.to_excel(writer, sheet_name='SER_ONLY')
        res_ESR.to_excel(writer, sheet_name='ESR_ONLY')
        df_SER_dup.to_excel(writer, sheet_name='SER_DUP')
        df_ESR_dup.to_excel(writer, sheet_name='ESR_DUP')
        summary.to_excel(writer, sheet_name='SUMMARY')


def cleanID(thisOneIn):
    thisOne = thisOneIn
    if pd.isna(thisOne):
        return thisOne
    else:
        try:
            thisOne = int(thisOne)
        except:
            pass
        else:
            thisOne = str(thisOne)
        thisIndex = thisOne.find('-')
        if thisIndex != -1:
            return thisOne[:thisIndex]
        else:
            return thisOne

def checkID(stringSER, stringESR):
    if re.search(stringESR, stringSER, re.I):
        return True
    else:
        return False

if __name__ == '__main__':
    print('********** Scripts start. **********')
    main()
    print('********** Scripts end. **********')
