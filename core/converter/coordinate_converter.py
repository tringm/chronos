import requests
from abc import ABC, abstractmethod
from typing import Tuple, List
import json


class CoordinateConverter(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def convert_coordinate(self, coordinate: Tuple, base_system_code, target_system_code):
        pass

    @abstractmethod
    def convert_multiple_coordinates(self, coordinates: List[Tuple], base_system_code, target_system_code):
        pass


class EpsgCoordinateConverter(CoordinateConverter):
    def __init__(self):
        super().__init__()
        self.base_url = 'http://epsg.io/trans?'

    def convert_coordinate(self, coordinate: Tuple, base_system_code: str, target_system_code: str):
        """

        :param coordinate: tuple of 2 or 3 coordinate
        :param base_system_code: source system code in epsg in string format (ESPG:3879 -> 3879)
        :param target_system_code: target system code
        :return: Converted coordinates
        """
        if len(coordinate) < 2 or len(coordinate) > 3:
            raise ValueError('Coordinate must be a tuple contains (x, y) or (x, y, z) coordinates')
        if len(coordinate) == 2:
            query = f"x={coordinate[0]}&y={coordinate[1]}"
        else:
            query = f"x={coordinate[0]}&y={coordinate[1]}&z={coordinate[2]}"
        query += f"&s_srs={base_system_code}&t_srs={target_system_code}"
        r = requests.get(self.base_url + query)
        r.raise_for_status()
        result_as_json = json.loads(r.content.decode('latin1'))
        return result_as_json['x'], result_as_json['y']

    def convert_multiple_coordinates(self, coordinates: List[Tuple], base_system_code, target_system_code):
        """

        :param coordinates: list of tuple of 2 or 3 coordinate
        :param base_system_code: source system code in epsg in string format (ESPG:3879 -> 3879)
        :param target_system_code: target system code
        :return: List of converted coordinates
        """
        if len(coordinates[0]) < 2 or len(coordinates[0]) > 3:
            raise ValueError('Coordinates must be a list of tuple contains (x, y) or (x, y, z) coordinates')
        query = 'data='
        for idx, coor in enumerate(coordinates):
            query += ','.join([str(c) for c in coor])
            if idx != len(coor) - 1:
                query += ';'
        query += f"&s_srs={base_system_code}&t_srs={target_system_code}"
        r = requests.get(self.base_url + query)
        r.raise_for_status()
        result_as_json = json.loads(r.content.decode('latin1'))
        if len(coordinates[0]) == 2:
            results = [(t['x'], t['y']) for t in result_as_json]
        else:
            results = [(t['x'], t['y'], t['z']) for t in result_as_json]

        return results
