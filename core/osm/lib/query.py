import requests
import pandas as pd
import io
import json
from pprint import pprint
from config import core_path

overpass_url = 'https://lz4.overpass-api.de/api/interpreter?'

# TODO: Support name in multiple language
# TODO: what if request failes


def get_countries():
    """
    :return: df with 3 column: id, abbreviation, and name in English
    """
    path = core_path() / 'osm' / 'templates' / 'get_countries.txt'
    with path.open(mode='r') as f:
        q = f.read()
    request = requests.post(overpass_url, data=q)
    return request.json()


def get_country_by_name(name):
    """
    Get country info by name in English
    :param name:
    :return: JSON format
    """
    path = core_path() / 'osm' / 'templates' / 'get_country_by_name.txt'
    with path.open(mode='r') as f:
        q = f.read()
    q = q.replace("insert_country_name", name)
    request = requests.post(overpass_url, data=q)
    return request.json()


def get_cities_by_countries(country_name):
    """

    :param country_name: name of the country in english
    :return:
    """
    path = core_path() / 'osm' / 'templates' / 'get_cities_by_country_name.txt'
    with path.open(mode='r') as f:
        q = f.read()
    q = q.replace("insert_country_name", country_name)
    request = requests.post(overpass_url, data=q)
    return request.json()


def get_streets_by_city(city_name, way_type=None):
    """

    :param city_name: name of city in English
    :return:
    """
    query_template_path = core_path() / 'osm' / 'templates' / 'get_streets_by_city_name.txt'
    with query_template_path.open(mode='r') as f:
        q = f.read()
    q = q.replace("insert_city_name", city_name)
    if way_type is not None:
        highway_requirement = 'highway=' + '\"' + way_type + '\"'
        q = q.replace("highway", highway_requirement)
    request = requests.post(overpass_url, data=q)
    return request.json()


def get_streets_with_postal_codes_by_city(city_name, way_type=None):
    """

        :param city_name: name of city in English
        :return:
        """
    query_template_path = core_path() / 'osm' / 'templates' / 'get_streets_with_postal_codes_by_city_name.txt'
    with query_template_path.open(mode='r') as f:
        q = f.read()
    q = q.replace("insert_city_name", city_name)
    if way_type is not None:
        highway_requirement = 'highway=' + '\"' + way_type + '\"'
        q = q.replace("highway", highway_requirement)
    request = requests.post(overpass_url, data=q)
    return request.json()