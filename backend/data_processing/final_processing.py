import pandas as pd
import numpy as np
DATASET_PATH = 'C:\\Users\\Prithwish Dan\\Documents\\SP23 Classes\\CS4300\\archive\\restaurants'
RESTAURANT_PATH = DATASET_PATH + '\\restaurants.csv'
RESTAURANT_MENUS_PATH = DATASET_PATH + '\\restaurant-menus.csv'

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
  text = text.replace('&amp;', 'and ')
  text = ''.join(filter(lambda x: x.isalnum() or x.isspace(), text))
  return text

def get_state(full_addr):
    if(type(full_addr) != str):
        return 'None'
    terms = [t.strip() for t in full_addr.split(',')]
    for term in terms:
        if len(term) == 2 and term == term.upper() and term.isalpha() and term in abb_to_us_state:
            return abb_to_us_state[term]
    return 'Non-USA'

restaurant_data = pd.read_csv(RESTAURANT_PATH)
menu_data = pd.read_csv(RESTAURANT_MENUS_PATH)

restaurant_data = restaurant_data[~restaurant_data['score'].isna()]
restaurant_data['name'] = restaurant_data['name'].apply(fix_ampersand)
restaurant_data['category'] = restaurant_data['category'].apply(fix_ampersand)
restaurant_data['state'] = restaurant_data['full_address'].apply(get_state)
# restaurant_data['state'] = restaurant_data['state'].apply(lambda x: x.replace('\r', ''))
restaurant_data.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)

ids = restaurant_data['id'].tolist()
menu_data = menu_data.query('restaurant_id in @ids')

menu_data['name'] = menu_data['name'].apply(fix_ampersand)
menu_data['category'] = menu_data['category'].apply(fix_ampersand)
menu_data['description'] = menu_data['description'].apply(fix_ampersand)
menu_data.reset_index(inplace=True)
menu_data['id'] = menu_data.index

print(restaurant_data.head(10))
print(menu_data.head(10))

restaurant_data.to_csv(DATASET_PATH + '\\restaurant_table.csv', index=False)
# menu_data.to_csv(DATASET_PATH + '\\item_table.csv', index=False)


