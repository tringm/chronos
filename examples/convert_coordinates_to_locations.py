from config import root_path
import pandas as pd
from core.epsg.lib.query import transform_coordinates
from core.osm.lib.query import get_area_by_coordinates

path = root_path() / 'examples' / 'io' / 'kiva_keskusta_kavelijoille_syksy2014.csv'
data = pd.read_csv(path, delimiter=';')

long_standard = []
lat_standard = []
locations = []

# TODO: add check timoeut for query

for index, row in data.iterrows():
    print(index)
    long = str(row['longitudeETRSGK25']).replace(',', '.')
    lat = row['latitudeETRSGK25'].replace(',', '.')
    long_converted, lat_converted = transform_coordinates(long, lat, '3879', '4326')
    long_standard.append(long_converted)
    lat_standard.append(lat_converted)
    loc = get_area_by_coordinates(lat=lat_converted, lon=long_converted, level_criteria='10')["elements"][0]['tags']['name']
    locations.append(loc)

data['longitudeWGS84'] = pd.Series(long_standard)
data['latitudeWGS84'] = pd.Series(lat_standard)
data['location'] = pd.Series(locations)
data.to_csv((root_path() / 'examples' / 'io' / 'kiva_keskusta_location.csv'), index=False)
