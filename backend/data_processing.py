import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import random
from wordcloud import WordCloud
import re
import nltk.corpus
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
stop = stopwords.words('english')

DATASET_PATH = 'C:\\Users\\Prithwish Dan\\Documents\\SP23 Classes\\CS4300\\archive'
RESTAURANT_PATH = DATASET_PATH + '\\p3restaurants.csv'
RESTAURANT_MENUS_PATH = DATASET_PATH + '\\p3menu.csv'

data = pd.read_csv(RESTAURANT_PATH)
df = pd.read_csv(RESTAURANT_MENUS_PATH)

def fix_ampersand(text):
    return text.replace('&amp;', 'and ')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
    stemmer = PorterStemmer()
    text = " ".join([stemmer.stem(word) for word in text.split() if word not in stop])
    return text

data.drop_duplicates(["id"],keep='first',inplace=True)
for i, row in enumerate(data.loc[:, 'name']):
    data.at[i, 'name'] = fix_ampersand(row)

for i, row in enumerate(data.loc[:, 'category']):
    data.at[i, 'category'] = fix_ampersand(row)

print(data.loc[:, ['name', 'category']])

df.drop_duplicates(["restaurant_id"],keep='first',inplace=True)
for i, row in enumerate(df.loc[:, 'category']):
    df.at[i, 'category'] = fix_ampersand(row)

for i, row in enumerate(df.loc[:, 'description']):
    df.at[i, 'description'] = fix_ampersand(row) if(type(row) == str) else 'None'

print(df.loc[:, ['category', 'description']])

data.to_csv(RESTAURANT_PATH)
df.to_csv(RESTAURANT_MENUS_PATH)