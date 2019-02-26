from pathlib import Path


def core_path():
    return Path(__file__).parent / 'core'


def mock_data_path():
    return Path(__file__).parent / 'io' / 'in' / 'mock_data'


def in_path():
    return Path(__file__).parent / 'io' / 'in'


def root_path():
    return Path(__file__).parent


