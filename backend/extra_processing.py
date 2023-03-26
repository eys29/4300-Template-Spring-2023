import re
import pandas as pd
DATASET_PATH = 'C:\\Users\\Prithwish Dan\\Documents\\SP23 Classes\\CS4300\\archive'
RESTAURANT_PATH = DATASET_PATH + '\\restaurant_table.csv'
RESTAURANT_MENUS_PATH = DATASET_PATH + '\\item_table.csv'

# orig = pd.read_csv(DATASET_PATH + '\\restaurants.csv')
# data = pd.read_csv(RESTAURANT_PATH)
df = pd.read_csv(RESTAURANT_MENUS_PATH)
pattern = re.compile('[^A-z0-9 ]+')

def clean_text(string):
  if type(string) != str:
    return string
  return pattern.search(string)
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
# data['name'] = orig['name'].apply(fix_ampersand)
# data['category'] = data['category'].apply(fix_ampersand)

df['name'] = df['name'].apply(fix_ampersand)
df['description'] = df['description'].apply(fix_ampersand)
df['category'] = df['category'].apply(fix_ampersand)
print(df.loc[75075, :])
# print(data['name'])

# data.to_csv(DATASET_PATH + '\\restaurant_table.csv')
df.to_csv(DATASET_PATH + '\\item_table.csv')