# chronos

A data generator that pull real data from real world


## Seeders

### Names

Names are crawled from [names.mongabay](https://names.mongabay.com/) (names data in U.S)
* Surname.csv contains surnames by race and statistics (e.g: % of people identify as that race)
* Firstname.csv contains first name ranked by gender

### Geographical data
User location data is based on:
    * Open Street Map(OSM):
        * Country's info (e.g: name, code, population, continent, etc.)
        * Cities's info (e.g: name, code, population, etc.)
        * Street Names
    * Geonames:
        * Postal codes for missing postal codes data in OSM
