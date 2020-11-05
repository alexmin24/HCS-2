import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
from plotnine import *
from plotnine.data import mpg
### all the files we want to read in
from collections import Counter, OrderedDict
from itertools import repeat, chain

import re

from textblob import TextBlob

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

# Python code to find frequency of each word
def freq(str):
    # break the string into list of words
    str_list = str.split()
    sorted_list = []

    # gives set of unique words
    words = sorted(str_list, key=str_list.count, reverse=True)

    return list(OrderedDict.fromkeys(words))

def get_freq(lst, string):
    lst_str = ' '.join(map(str, lst))
    text = TextBlob(lst_str)
    return text.words.count(string,case_sensitive=True)

def get_sentiment(lst):
    lst_str = ' '.join(map(str, lst))
    text = TextBlob(lst_str)
    return text.sentiment

def freq_body(series):
    str_list = []
    for body in series:
        str_list.extend(remove_tags(body).split())
    unique_words = set(str_list)

    # gives set of unique words
    words = sorted(str_list, key=str_list.count, reverse=True)

    return list(OrderedDict.fromkeys(words))

dont_include=['the', 'of', 'to', 'and', 'in', 'a', 'that', 'for', 'is', 'as', 'The', 'his', 'he', 'on', 'with', 'be', 'has', 'not', 'was', 'will', 'by', 'at', 'are', 'from', 'it', 'have', 'which', 'this', 'an', 'would',
              'but', 'more', 'had','In', 'been', 'who', 'only', 'its', 'He', 'were', 'their', 'last', 'one', 'new', 'than', 'or', 'said', 'when', 'can', 'two', 'I', 'no','out', 'most', 'all', 'they', 'should', 'these', 'if', 'however,', 'our',
              'there', 'may', 'also','any', 'about','both', 'some', 'other', 'now', 'such', 'could', 'much', 'must', 'even', 'after', 'we', 'up', 'since', 'many', 'into',  'while', 'do', 'so', 'over', 'still', 'make', 'made', 'before', 'through', 'It',]

years = [i * 4 for i in range(489, 505)]
years_text = list(map(lambda x : str(x) + ".jsonlines", years))

article_nums_winners = []
article_nums_losers = []

total_freq_winners=[]
total_freq_losers=[]

filters=[
    ['Trump', 'Biden'],
    ['Trump', 'Clinton'],
    ['Obama', 'Romney'],
    ['Obama', 'McCain'],
    ['Bush', 'Kerry'],
    ['Bush', 'Gore'],
    ['Clinton', 'Dole'],
    ['Clinton', 'Bush'],
    ['Bush', 'Dukakis'],
    ['Reagan', 'Mondale'],
    ['Reagan', 'Carter'],
    ['Carter', 'Ford'],
    ['Nixon', 'McGovern'],
    ['Nixon', 'Humphrey'],
    ['Johnson', 'Goldwater'],
    ['Kennedy', 'Nixon'],
    ['Eisenhower', 'Stevenson']
]

filters = filters[::-1]

winner_polarity=[]
winner_subjectivity=[]
loser_polarity=[]
loser_subjectivity=[]

dfs = list(map(lambda x: pd.read_json(x, lines=True), years_text))
for i in range(len(dfs)):
    bodies  = dfs[i]['body']
    for j in range(2):
        lst = list(filter(lambda x: filters[i][j] in x, bodies))

        frequencies = freq_body([" ".join([w for w in t.split() if not w in dont_include]) for t in lst])
        df = pd.DataFrame({'body': frequencies})
        df.to_csv(str(years[i]) + filters[i][j] + ".csv" ,index=False)

        if j == 0:
            article_nums_winners.append(len(lst))
            total_freq_winners.append(get_freq(bodies, filters[i][j]))

            winner_polarity.append(get_sentiment(lst).polarity)
            winner_subjectivity.append(get_sentiment(lst).subjectivity)
        else:
            article_nums_losers.append(len(lst))
            total_freq_losers.append(get_freq(bodies, filters[i][j]))

            loser_polarity.append(get_sentiment(lst).polarity)
            loser_subjectivity.append(get_sentiment(lst).subjectivity)


win_percentage = []
lost_percentage = []
for x in range(len(years)):
   win_percentage.append(article_nums_winners[x] / (article_nums_winners[x] + article_nums_losers[x]))
   lost_percentage.append(article_nums_losers[x] / (article_nums_winners[x] + article_nums_losers[x]))


total_win_percentage=[]
total_lost_percentage=[]
for x in range(len(years)):
   total_win_percentage.append(total_freq_winners[x] / (total_freq_winners[x] + total_freq_losers[x]))
   total_lost_percentage.append(total_freq_losers[x] / (total_freq_winners[x] + total_freq_losers[x]))

'''df = pd.DataFrame({'year': years, 'winners': article_nums_winners, 'losers': article_nums_losers})
df.to_csv("numbers.csv", index=False)

df2 = pd.DataFrame({'year': years, 'winners': win_percentage, 'losers': lost_percentage})
df2.to_csv("percentages.csv", index=False)

df3 = pd.DataFrame({'year': years, 'winners': total_freq_winners, 'losers': total_freq_losers})
df3.to_csv("totals.csv", index=False)

df3 = pd.DataFrame({'year': years, 'winners': total_win_percentage, 'losers': total_lost_percentage})
df3.to_csv("total_percentages.csv", index=False)

df4 = pd.DataFrame({'year': years, 'winners_polarity': winner_polarity,
                   'winners_subjectivity': winner_subjectivity, 'losers_polarity': loser_polarity,
                    'losers_subjectivity': loser_subjectivity})
df4.to_csv('sentiments.csv', index=False)'''

for i in range(len(years)):
    win_polarity = winner_polarity[i]
    loss_polarity = loser_polarity[i]

    if (win_polarity > 0):
        print(filters[i][0] + "was written about positively")
    else:
        print(filters[i][0] + "was written about negatively")

    if (loss_polarity > 0):
        print(filters[i][1] + "was written about positively")
    else:
        print(filters[i][1] + "was written about negatively")
