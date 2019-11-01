import pandas as pd
import os, sys
import re

current_path = os.path.abspath(__file__)
os.chdir(os.path.dirname(current_path))

# read template crosswalk
df_CW = pd.read_excel('sources/TemplatesCW.xlsx', sheet_name='Sheet1', \
index_col=0, header=0)
df_CW = df_CW[df_CW['Owning Application']=='Orders']
df_CW.drop(['Test', 'Owning Application'], axis=1, inplace=True)
# print(df_CW)

# delete empty columns
# print(df_CW.shape)
for i in df_CW.columns:
    if df_CW[i].count() == 0:
        df_CW.drop(labels=i, axis=1, inplace=True)
# print(df_CW.shape)
print(df_CW)

# delete columns that do not compare
colIndexList = list(df_CW.columns)
# removeIndexs =
# ['5155', '5160', '5150', '5020', '5175', '5170']
# for ind in removeIndexs:
#     colIndexList.remove(ind)
# print(colIndexList)

# read and select SER data
df_SER_raw_whole = pd.read_excel('sources/SER20190809.xlsx', sheet_name='SER export', header=0)
df_SER = df_SER_raw_whole[df_SER_raw_whole['2905'].isin(df_CW.index)]
df_SER = df_SER.reset_index(drop=True)
df_SER = df_SER[colIndexList]
print(df_SER)

# df_SER_test = df_SER.iloc[[0]]
# df_CW_test = df_CW.iloc[[0]]
# res = df_SER_test == df_CW_test

with pd.ExcelWriter('results/test.xlsx') as writer:
    # res.to_excel(writer, sheet_name='test1')
    df_SER.to_excel(writer, sheet_name='test2')
    df_CW.to_excel(writer, sheet_name='test3')
