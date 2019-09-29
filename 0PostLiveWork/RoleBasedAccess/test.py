import pandas as pd
import os, sys

def main():

    current_path = os.path.abspath(__file__)
    os.chdir(os.path.dirname(current_path))


if __name__ == '__main__':
    print('********** Scripts start. **********')
    main()
    print('********** Scripts end. **********')
