import pandas as pd
import os, sys
import re
import TemplateTools as TT

def main():

    current_path = os.path.abspath(__file__)
    os.chdir(os.path.dirname(current_path))

    df_SER_raw_whole = pd.read_excel('sources/SER20190809.xlsx', sheet_name='SER export', header=[4])
    df_ESR_raw_whole = pd.read_excel('sources/Data Source 1- Main.xlsx', sheet_name='Data', header=[0])

    df_SER_providerType_selected = pd.read_excel(\
    'sources/Provider Type SER - selected.xlsx', sheet_name='Sheet1', header=[0])
    list_SER_providerType_selected = \
    df_SER_providerType_selected["Selected Provider Type"].tolist()

    df_SER_raw = df_SER_raw_whole[df_SER_raw_whole['Provider type'].isin(list_SER_providerType_selected)]
    df_ESR_raw = df_ESR_raw_whole[df_ESR_raw_whole['Staff Group'].isin(['Medical and Dental', 'Students'])]

    columnNames_SER = ['ID', 'Provider name', 'External Name', 'Sex', \
    'Rpt Grp One', 'Provider type', 'Provider specialty', \
    'Rpt Grp Six', 'MPI ID-Type', 'MPI ID']
    columnNames_ESR = ['SER File Name', 'SER External Name', 'Gender', \
    'Employee Number', 'Assignment No.', 'Position Title', 'Role', 'Area Of Work', \
    'Org L2', 'Org L3', 'Org L4', 'Org L5', \
    'Professional Registration Num']

    df_SER = df_SER_raw[columnNames_SER]
    df_ESR = df_ESR_raw[columnNames_ESR]

    df_SER['Rpt Grp One'] = df_SER['Rpt Grp One'].apply(cleanID)
    df_ESR['Employee Number'] = df_ESR['Employee Number'].apply(cleanID)

    df_SER_providerName_toCheckEmNum = df_SER.loc[pd.isna(df_SER['Rpt Grp One']), 'Provider name']
    list_SER_providerName_toCheckEmNum = df_SER_providerName_toCheckEmNum.drop_duplicates().tolist()
    df_SER_toCheckEmNum = df_SER[df_SER['Provider name'].isin(list_SER_providerName_toCheckEmNum)]
    df_SER_remain = df_SER[~df_SER['Provider name'].isin(list_SER_providerName_toCheckEmNum)]
    df_SER_toCheckEmNum = df_SER_toCheckEmNum.sort_values(by='Provider name')

    dupIndicated = df_SER_remain.duplicated('Rpt Grp One', keep=False)
    df_SER_dup = df_SER_remain[dupIndicated]
    df_SER_remain = df_SER_remain[~dupIndicated]

    dupIndicated = df_ESR.duplicated('Employee Number', keep=False)
    df_ESR_dup = df_ESR[dupIndicated]
    df_ESR_remain = df_ESR[~dupIndicated]

    df_SER_remain['Key'] = df_SER_remain.apply(lambda row: \
    (row['Provider name'], row['External Name'], row['Rpt Grp One']), axis=1)

    df_ESR_remain['Key'] = df_ESR_remain.apply(lambda row: \
    (row['SER File Name'], row['SER External Name'], row['Employee Number']), axis=1)

    res = pd.merge(df_SER_remain, df_ESR_remain, \
    # left_on=['Rpt Grp One'], right_on=['Employee Number'], \
    on='Key',
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
    # , str(row['Org L5'])
    ), axis=1)

    res_both['IsSameTemplate'] = res_both.apply(lambda row: \
    str(row['TemplateGene']) == str(row['Rpt Grp Six']), axis=1)

    res_both_HasSameTemplate = res_both[res_both['IsSameTemplate'].isin([True])]

    res_both = res_both[[
    'ID', 'Provider name', 'External Name', 'Sex', \
    'Provider type', 'Provider specialty', \
    'Rpt Grp One', 'MPI ID-Type', 'MPI ID', \
    'Rpt Grp Six', 'TemplateGene', 'IsSameTemplate', \
    'Key', \
    'SER File Name', 'SER External Name', 'Gender', \
    'Position Title', 'Role', 'Area Of Work', \
    'Org L2', 'Org L3', 'Org L4', 'Org L5', \
    'Assignment No.', 'Employee Number', 'Professional Registration Num', \
    'IfHasThisRegNumInSER' \
    ]]

    summary = pd.Series([ \
    'Input source files: ' + 'SER ({} rows), ESR ({} rows).'.format(len(df_SER_raw_whole), len(df_ESR_raw_whole)),
    'Choose the subset of SER ({} rows): '.format(len(df_SER)) + 'from the selected provider types.',
    'Choose the subset of ESR ({} rows): '.format(len(df_ESR)) + '"Medical and Dental", "Students" in "Staff Group".',

    'Remove SER rows (those provider names with empty "Rpt Grp One" ' \
    + '(i.e. Employee Number)) as shown in the tab SER_ToCheck ' \
    + '({} rows) ;remaining {} SER rows.'\
    .format(len(df_SER_toCheckEmNum), len(df_SER_remain)),

    'Process "Employee Number" in ESR ("Rpt Grp One" in SER) by deleting digits after "-".',

    'Remove duplicated rows (i.e. multiple rows with same Employee Number) as shown in two tabs: ' \
    + 'SER_DUP ({} rows), ESR_DUP ({} rows).'.format(len(df_SER_dup), len(df_ESR_dup)),

    'Match on the Key: SER ("Provider name", "External Name", "Rpt Grp One") '
    + ', ESR ("SER File Name", "SER External Name", "Employee Number").',

    'Join non-duplicated rows which results in three tabs: ' \
    + 'IN_BOTH ({} rows), SER_ONLY ({} rows), ESR_ONLY ({} rows).'.format(len(res_both), len(res_SER),
     len(res_ESR)),

    'Add "IfHasThisRegNumInSER" Column (to the tab IN_BOTH): ' \
    + 'True ({}/{}={}% rows) if "Professional Registration Num" (ESR) in "MPI ID" (SER).'\
    .format(len(res_both_HasRegNum), len(res_both), round(100*len(res_both_HasRegNum)/len(res_both),2) ),

    'Add "TemplateGene" Column (to the tab IN_BOTH): ' \
    + 'generated template (by the logic version 1.0) from the ESR info ("Position Title", "Role", "Area Of Work").',

    'Add "IsSameTemplate" Column (to the tab IN_BOTH): ' \
    + 'True ({}/{}={}% rows) if "TemplateGene" (ESR) is same with "Rpt Grp Six" (SER).'\
    .format(len(res_both_HasSameTemplate), len(res_both), round(100*len(res_both_HasSameTemplate)/len(res_both),2) ),
    ])

    summary.name = 'Analysis Process'

    with pd.ExcelWriter('results/output.xlsx') as writer:
        res_both.to_excel(writer, sheet_name='IN_BOTH')
        res_SER.to_excel(writer, sheet_name='SER_ONLY')
        res_ESR.to_excel(writer, sheet_name='ESR_ONLY')
        df_SER_dup.to_excel(writer, sheet_name='SER_DUP')
        df_ESR_dup.to_excel(writer, sheet_name='ESR_DUP')
        df_SER_toCheckEmNum.to_excel(writer, sheet_name='SER_ToCheck')
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
