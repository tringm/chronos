import pandas as pd
from config import mock_data_path
import numpy as np
import datetime
from core.structure.PopulationPyramid import PopulationPyramid


def generate_people_basic_info(population):
    """
    Generate a person's basic info: Name, Gender
    :param population:
    :return:
    """
    surname_data = pd.read_csv(mock_data_path() / 'surname.csv', delimiter=',')
    firstname_data = pd.read_csv(mock_data_path() / 'firstname.csv', delimiter=',')

    surname_samples = surname_data.sample(population, axis=0)
    firstname_samples = firstname_data.sample(population, axis=0)

    is_typical_gender_distribution = np.random.binomial(1, 0.8, population )
    opposite_gender = {'male': 'female', 'female': 'male'}

    people = []

    for idx in range(population):
        info = {}
        info['first_name'] = firstname_samples.iloc[idx]['Name']
        info['last_name'] = surname_samples.iloc[idx]['Surname']
        typical_gender = firstname_samples.iloc[idx]['Gender'].lower()
        if is_typical_gender_distribution[idx]:
            info['gender'] = typical_gender
        else:
            info['gender'] = opposite_gender[typical_gender]
        people.append(info)
    df = pd.DataFrame(people)
    print(df.head(3))
    df = df[['first_name', 'last_name', 'gender']]
    return df



def mail(first_name, last_name):
    ends = ['gmail.com', 'yahoo.com', 'hotmail.com']






