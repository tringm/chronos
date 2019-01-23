from core.osm.lib.query import *
import json
from config import in_path


def cache_meta_data():
    countries_meta = get_countries()
    countries_meta_path = in_path() / 'osm' / 'country' / 'countries_meta.json'
    with countries_meta_path.open(mode='w') as f:
        json.dump(countries_meta, f)

### cities in finland


def cache_country_meta(country_name):
    country = get_country_by_name(country_name)
    path = in_path() / 'osm' / 'country' / (country_name + '.json')
    with path.open(mode='w') as f:
        json.dump(country, f)


def cache_cities_by_countries(country_name):
    cities = get_cities_by_countries(country_name)
    path = in_path() / 'osm' / 'city' / (country_name + '_cities.json')
    with path.open(mode='w') as f:
        json.dump(cities, f)


def cache_streets_by_city(city_name, way_type=None):
    streets = get_streets_by_city(city_name, way_type)
    path = in_path() / 'osm' / 'city' / (city_name + '_streets.json')
    with path.open(mode='w') as f:
        json.dump(streets, f)


# cache_country_meta('Finland')
# cache_cities_by_countries('Finland')
cache_streets_by_city('Helsinki', 'residential')




