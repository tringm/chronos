from math import floor
import datetime as dt
from random import randint

def divide_by_proportion(proportion_list, n_items):
    result = [floor(prop * n_items) for prop in proportion_list]
    sum_diff = n_items - sum(result)
    if sum_diff > 0:
        if sum_diff > len(proportion_list):
            raise ValueError('Fix me')
        for idx in np.random.choice(len(proportion_list), sum_diff):
            result[idx] += 1
    if sum_diff < 0:
        raise ValueError('Fix me')
    return result


def random_date_time():
    # TODO: parameters for date time (year, month, day, etc.)
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year = randint(2010, 2018)
    month = randint(1, 12)
    day = randint(1, days_in_month[month])
    hour = randint(0, 23)
    minute = randint(0, 59)
    second = randint(0, 59)
    datetime = dt.datetime(year, month, day, hour, minute, second).strftime("%Y-%m-%d %H:%M:%S")
    return datetime
