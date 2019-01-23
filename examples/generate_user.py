import json
from config import in_path
from pprint import pprint
from core.structure.OSM.City import City
from core.generator.seed_maker import generate_people_basic_info
from core.osm.lib.query import get_streets_with_postal_codes_by_city, get_streets_by_city
from core.geonames.lib.query import get_postal_codes_by_city
import math
import numpy as np
import pandas as pd
from random import choice

finland_city_path = in_path() / 'osm' / 'city' / 'Finland_cities.json'

with finland_city_path.open(mode='r') as f:
    cities = []
    for city_meta in json.load(f)['elements']:
        city = City()
        city.load_from_json(city_meta)
        cities.append(city)


population = 10
people = generate_people_basic_info(population)

# Assign people to cities based on population proportion
total_population = sum(float(city.population) for city in cities)
cities_population = [math.ceil(float(city.population)/total_population * population) for city in cities]
cities_population[-1] = cities_population[-1] - (sum(cities_population) - population)


people_where = []

for idx, city in enumerate(cities):
    print(city.name)
    city_population = cities_population[idx]
    streets_raw = get_streets_with_postal_codes_by_city(city.name, 'residential')
    if streets_raw['elements']:
        # convert to tuple of street name and postal code
        print('some postal code')
        streets = [(street['tags']['name'], street['tags']['postal_code']) for street in streets_raw['elements']]
    else:
        print('none postal code')
        streets_raw = get_streets_by_city(city.name, 'residential')
        postal_codes = get_postal_codes_by_city(city.name)
        streets = [(street['tags']['name'], choice(postal_codes)) for street in streets_raw['elements']]

    streets_idx = np.random.randint(len(streets), size=city_population)
    for i in range(city_population):
        street = streets[streets_idx[i]]
        # TODO: add character
        address = str(np.random.randint(1000)) + ' ' + street[0]
        postal_code = street[1]
        people_where.append({'address': address, 'postal_code': postal_code})
people_where = pd.DataFrame(people_where)
people_where = people_where[['address', 'postal_code']]

pprint(pd.concat([people, people_where], axis=1))
#
#
# streets_raw = get_streets_with_postal_codes_by_city('Pori')
# streets = [(street['tags']['name'], street['tags']['postal_code']) for street in streets_raw['elements']]
# pprint(streets)
