class Country:
    def __init__(self, id=None, name=None, lat=None, lon=None, continent=None, population=None, area=None):
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.continent = continent
        self.population = population
        self.area = area

    def load_from_json(self, json_object):
        # TODO: country = json_object is stupid
        meta = json_object['elements'][0]
        self.id = meta['id']
        self.lat = meta['lat']
        self.lon = meta['lon']
        self.name = meta['tags']['name:en']
        self.continent = meta['tags']['is_in:continent']
        self.population = meta['tags']['population']
        self.area = meta['tags']['sqkm']

