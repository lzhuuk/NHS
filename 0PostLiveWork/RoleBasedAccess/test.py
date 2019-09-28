import pandas as pd
import os, sys

def main():

    current_path = os.path.abspath(__file__)
    os.chdir(os.path.dirname(current_path))

    df_ESR_providerType_selected = pd.read_excel(\
    'sources/Provider Type SER - selected.xlsx', sheet_name='Sheet1', header=[0])

    print(df_ESR_providerType_selected.head())
    print(df_ESR_providerType_selected.tail())

    print(df_ESR_providerType_selected["Selected Provider Type"].tolist())

if __name__ == '__main__':
    print('********** Scripts start. **********')
    main()
    print('********** Scripts end. **********')
