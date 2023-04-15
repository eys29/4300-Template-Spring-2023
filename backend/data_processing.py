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
RESTAURANT_PATH = DATASET_PATH + '\\restaurant_table.csv'
RESTAURANT_MENUS_PATH = DATASET_PATH + '\\restaurant-menus.csv'

data = pd.read_csv(RESTAURANT_PATH)
df = pd.read_csv(RESTAURANT_MENUS_PATH)
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
abb_to_us_state = {v:k for k,v in us_state_to_abbrev.items()}

def fix_ampersand(text):
    if(type(text) != str):
        return 'None'
    return text.replace('&amp;', 'and ')

def preprocess_text(text):
    if(type(text) != str):
        return 'None'
    text = text.lower()
    text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
    stemmer = PorterStemmer()
    text = " ".join([stemmer.stem(word) for word in text.split() if word not in stop])
    return text

def get_state(full_addr):
    if(type(full_addr) != str):
        return 'None'
    terms = [t.strip() for t in full_addr.split(',')]
    for term in terms:
        if len(term) == 2 and term == term.upper() and term.isalpha():
            return abb_to_us_state[term]
    return 'None'

# data.drop_duplicates(["id"],keep='first',inplace=True)
for i, row in enumerate(data.loc[:, 'name']):
    data.at[i, 'name'] = fix_ampersand(row)

for i, row in enumerate(data.loc[:, 'category']):
    data.at[i, 'category'] = fix_ampersand(row)

for i, row in enumerate(data.loc[:, 'full_address']):
    data.at[i, 'state'] = get_state(row)

# print(data.loc[:, ['name', 'category', 'state']])
print(data.columns)
idxs = data['id'].tolist()
# df.drop_duplicates(["restaurant_id"],keep='first',inplace=True)

# print(df.loc[:, ['category', 'description']])
print(df.shape)
df = df.query('restaurant_id in @idxs')
print(df.shape)
data.to_csv(DATASET_PATH + '\\restaurant_table.csv')
df.to_csv(DATASET_PATH + '\\item_table.csv')

for i, row in enumerate(df.loc[:, 'category']):
    df.at[i, 'category'] = fix_ampersand(row)
    df.at[i, 'id'] = i
    df.at[i, 'description'] = fix_ampersand(df.at[i, 'description'])
    if i % 1000 == 0:
        print(i)

df.to_csv(DATASET_PATH + '\\item_table.csv')

