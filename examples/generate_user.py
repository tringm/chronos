from json import load
from random import choice, shuffle

import numpy as np
import pandas as pd

from config import in_path
from core.generator.seed_maker import generate_people_basic_info
from core.geonames.lib.query import get_postal_codes_by_city
from core.osm.lib.query import get_streets_with_postal_codes_by_city, get_streets_by_city
from core.structure.OSM.City import City
from core.structure.PopulationPyramid import PopulationPyramid

from examples.lib.helper import divide_by_proportion

finland_city_path = in_path() / 'osm' / 'city' / 'Finland_cities.json'

with finland_city_path.open(mode='r') as f:
    cities = []
    for city_meta in load(f)['elements']:
        city = City()
        city.load_from_json(city_meta)
        cities.append(city)

population = 1000
people = generate_people_basic_info(population)

# Assign people to cities based on population proportion
total_population = sum(float(city.population) for city in cities)
cities_population = divide_by_proportion([float(city.population)/total_population for city in cities], population)

people_where = []

for idx, city in enumerate(cities):
    city_population = cities_population[idx]
    streets_raw = get_streets_with_postal_codes_by_city(city.name, 'residential')
    if streets_raw['elements']:
        # convert to tuple of street name and postal code
        streets = [(street['tags']['name'], street['tags']['postal_code']) for street in streets_raw['elements']]
    else:
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

people_data = pd.concat([people, people_where], axis=1)


world_population_pyramid = PopulationPyramid()

brackets_population = divide_by_proportion([(p[0] + p[1])/100 for p in world_population_pyramid.proportion], population)

ages = np.array([])
for idx, bracket_population in enumerate(brackets_population):
    bracket = world_population_pyramid.brackets[idx]
    bracket_ages = np.random.randint(bracket[0], bracket[1], size=bracket_population)
    ages = np.concatenate((ages, bracket_ages))

ages = ages.astype(int)
shuffle(ages)
people_data['age'] = pd.Series(ages)
people_data.to_csv('users.csv', sep=',')





