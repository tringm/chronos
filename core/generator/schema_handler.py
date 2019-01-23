from config import in_path
from pprint import pprint
from lib.loader import json_loader

pprint(json_loader(in_path() / 'schema' / 'schema1.json'))


