from config import in_path
import csv
import pandas as pd
import numpy as np


def postal_codes_data():
    path = in_path() / 'geonames' / 'countries.csv'
    postal_codes = pd.read_csv(path, sep=',', low_memory=False)
    return postal_codes

data = postal_codes_data()
data[data['name'=='oulu']]
