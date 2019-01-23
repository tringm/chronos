import requests
from secret import get_geoname_username


base_url = 'http://api.geonames.org/findNearbyPostalCodesJSON?'


def get_postal_codes_by_city(city_name):
    """

    :param city_name: name of city in English
    :return:
    """
    url = base_url + 'placename=' + city_name + '&username=' + get_geoname_username()
    request = requests.get(url)
    postal_codes = [item['postalCode'] for item in request.json()['postalCodes']]
    return postal_codes

