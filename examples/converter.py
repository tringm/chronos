import json

import pandas as pd

from config import root_path

path = root_path() / 'examples' / 'io' / 'kiva_keskusta_location.csv'
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', -1)
data = pd.read_csv(path, delimiter=',')
data.to_csv((root_path() / 'examples' / 'io' / 'kiva_keskusta_with_location.csv'), sep=";", index=False)
data.to_json((root_path() / 'examples' / 'io' / 'kiva_keskusta_with_location.json'), orient='records', force_ascii=False)