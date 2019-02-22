import json

import requests


def transform_coordinates(x, y, source_system, target_system, base_url='http://epsg.io/trans?'):
    """

    :param x: lat in string format
    :param y: lon in string format
    :param source_system: source system number in epsg in string format (ESPG:3879 -> 3879)
    :param target_system: simliar to source system
    :param base_url:
    :return:
    """
    url = base_url + 'x='
    url += x
    url += '&y='
    url += y
    url += '&s_srs='
    url += source_system
    url += '&t_srs='
    url += target_system

    request = requests.get(url)
    result_as_json = json.loads(request.content.decode('latin1'))
    return (result_as_json['x'], result_as_json['y'])


def transform_multiple_coordinates(xs, ys, source_system, target_system, base_url='http://epsg.io/trans?'):
    """
    :param xs: list of lon in string format
    :param ys: list of lat in string format
    :param source_system: source system number in epsg in string format (ESPG:3879 -> 3879)
    :param target_system: simliar to source system
    :param base_url:
    :return:
    """
    url = base_url + 'data='
    for idx, x in enumerate(xs):
        url += x
        url += ',' + ys[idx]
        if idx != len(xs) - 1:
            url += ';'
    url += '&s_srs='
    url += source_system
    url += '&t_srs='
    url += target_system

    request = requests.get(url)
    result_as_json = json.loads(request.content.decode('latin1'))
    results = [(t['x'], t['y']) for t in result_as_json]
    return results


# print(transform_coordinates('25497346.000153500', '6673006.000000000', '3879', '4326'))


# print(transform_multiple_coordinates(['25497346.000153500', '25496148.499851000'],
#                                      ['6673006.000000000', '6673960.500000000'], '3879', '4326'))