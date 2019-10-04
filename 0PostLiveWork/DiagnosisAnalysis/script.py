import pandas as pd
import os, sys
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

def main():

    current_path = os.path.abspath(__file__)
    os.chdir(os.path.dirname(current_path))

    df_data = pd.read_excel(\
    'sources/Epic ED Diagnosis Comment Analysis - 04102019.xlsx', \
    sheet_name='comment', header=[0])

    # df_data['Diagnosis(Comments)'] = df_data['Diagnosis(Comments)'].apply(cutOffString)

    # print(df_data['Diagnosis(Comments)'].head())

    temp = df_data['Diagnosis(Comments)'].str.lower().str.cat(sep=' ')
    words = nltk.tokenize.word_tokenize(temp)

    excludeList = [ \
    'left', 'right', 'lt', 'rt', 'r', 'l', \
    'the', 'a', 'and', 'or', 'but', \
    'with', 'by', 'from', 'due', 'non', \
    'to', 'of', 'on', 'in', 'for', 'at', \
    'dx', 'gp', 'likely', 'possible', 'epic', \
    'not', 'no', 'without', 'post', \
    ]
    # 'confirmed', 'probably'
    # 'like', 'any', 'it'

    words = [word for word in words \
    if word.isalpha() and word not in excludeList]

    for i, word in enumerate(words):
        if word == 'pains':
            words[i] = 'pain'
        elif word == 'abdominal':
            words[i] = 'abdo'
        elif word == 'msk':
            words[i] = 'musculoskeletal'

    word_dist = nltk.FreqDist(words)

    # top_N = 100
    rslt = pd.DataFrame(word_dist.most_common(),\
    columns=['Word', 'Frequency'])
    # print(rslt)

    df_excludeList = pd.Series(excludeList)
    df_excludeList.name = 'Excluded Words'

    with pd.ExcelWriter('results/output.xlsx') as writer:
        rslt.to_excel(writer, sheet_name='Sheet1')
        df_excludeList.to_excel(writer, sheet_name='Sheet2')

    # plt.ion()
    word_dist.plot(20,cumulative=False, \
    title="Word Frequency (Top 20) in ED Diagnosis Comments")
    # plt.savefig('results/freqDist.png')
    # plt.ioff()

    # print(' '.join(words))
    # sys.exit(0)

    thisWordCloud = WordCloud(background_color="white", \
    width=1000, height=860, margin=2).generate_from_frequencies(word_dist)
    plt.imshow(thisWordCloud)
    plt.axis("off")
    # plt.show()
    thisWordCloud.to_file('results/wordCloud1.png')

    thisWordCloud = WordCloud(background_color="white", \
    width=1000, height=860, margin=2).generate(' '.join(words))
    plt.imshow(thisWordCloud)
    plt.axis("off")
    # plt.show()
    thisWordCloud.to_file('results/wordCloud2.png')

def cutOffString(stringIn):
    stringIn = str(stringIn)
    stringOut = re.sub(r'not .*|no .*|without .*|post .*', '', stringIn, re.I)
    stringOut = stringOut.strip()
    if re.search('not|no|without|post', stringIn, re.I):
        print('IN:', stringIn)
        print('OUT:', stringOut)
    return stringOut

if __name__ == '__main__':
    print('********** Scripts start. **********')
    main()
    print('********** Scripts end. **********')
