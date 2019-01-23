class City:
    def __init__(self, id=None, name=None, lat=None, lon=None, country=None, population=None, area=None):
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.country = country
        self.population = population

    def load_from_json(self, json_object):
        # TODO: country = json_object is stupid
        meta = json_object
        self.id = meta['id']
        self.lat = meta['lat']
        self.lon = meta['lon']
        self.name = meta['tags']['name']
        self.country = meta['tags']['is_in:country']
        self.population = meta['tags']['population']

