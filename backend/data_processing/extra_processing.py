import re
import pandas as pd
DATASET_PATH = 'C:\\Users\\Prithwish Dan\\Documents\\SP23 Classes\\CS4300\\archive'
RESTAURANT_PATH = DATASET_PATH + '\\restaurant_table.csv'
RESTAURANT_MENUS_PATH = DATASET_PATH + '\\item_table.csv'

orig = pd.read_csv(DATASET_PATH + '\\restaurants.csv')
# data = pd.read_csv(RESTAURANT_PATH)
# df = pd.read_csv(RESTAURANT_MENUS_PATH)
# pattern = re.compile('[^A-z0-9 ]+')
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

def get_state(full_addr):
    if(type(full_addr) != str):
        return 'None'
    terms = [t.strip() for t in full_addr.split(',')]
    for term in terms:
        if len(term) == 2 and term == term.upper() and term.isalpha():
            return abb_to_us_state[term]
    return 'n/a'
# def clean_text(string):
#   if type(string) != str:
#     return string
#   return pattern.search(string)
def fix_ampersand(text):
  if(type(text) != str):
      return 'None'
  text = text.replace('&amp;', 'and ')
  text = ''.join(filter(lambda x: x.isalnum() or x.isspace(), text))
  return text
# data['name'] = data['name'].apply(clean_text)
# df.apply_map(clean_text)
# ids = data['id'].tolist()
# orig = orig.query('id in @ids')
# orig = orig.sort_values(by=['id'])
# print(ids)
# print(orig['id'])
orig['name'] = orig['name'].apply(fix_ampersand)
orig['category'] = orig['category'].apply(fix_ampersand)
orig['state'] = orig['full_address'].apply(get_state)

# df['name'] = df['name'].apply(fix_ampersand)
# df['description'] = df['description'].apply(fix_ampersand)
# df['category'] = df['category'].apply(fix_ampersand)
# print(df.loc[75075, :])
# print(data['name'])

orig.to_csv(DATASET_PATH + '\\restaurant_table2.csv')
# df.to_csv(DATASET_PATH + '\\item_table2.csv')