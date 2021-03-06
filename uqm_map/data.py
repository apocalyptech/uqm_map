#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:
#
# UQM Starmap Viewer
# Copyright (C) 2009-2017 CJ Kucera
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import sys
import math
import gzip
import json
import string
import os.path

class MinData(object):
    """
    A class to hold mineral data.  Each planet has one of these, and each
    system uses a few of these for aggregate data as well.
    """

    min_vals = [ 'common', 'corrosive', 'base', 'noble', 'rare', 'precious', 'radioactive', 'exotic' ]

    def __init__(self, common=0, corrosive=0, base=0, noble=0, rare=0, precious=0, radioactive=0, exotic=0):
        self.common = common
        self.corrosive = corrosive
        self.base = base
        self.noble = noble
        self.rare = rare
        self.precious = precious
        self.radioactive = radioactive
        self.exotic = exotic

    def add(self, other):
        """
        Adds another MinData structure to ourselves.
        """
        self.common += other.common
        self.corrosive += other.corrosive
        self.base += other.base
        self.noble += other.noble
        self.rare += other.rare
        self.precious += other.precious
        self.radioactive += other.radioactive
        self.exotic += other.exotic

    def value(self):
        """
        Returns the RU value for the given set of minerals
        """
        return self.common+(2*self.corrosive)+(3*self.base)+(4*self.noble)+ \
            (5*self.rare)+(6*self.precious)+(8*self.radioactive)+(25*self.exotic)

    def weight(self):
        """
        Returns the weight of all the minerals (that is, how much room they'll
        consume in your cargo holds)
        """
        return self.common+self.corrosive+self.base+self.noble+self.rare+self.precious+self.radioactive+self.exotic

    def worth(self):
        """
        This is labeled "MVpU" or "Mineral Value per Unit" in the GUI typically -
        it's just a measure of how much bang for the buck you get.  A planet with
        7k RU in Exotic Minerals has more "worth" than one with 7k RU in Base Metals
        because it'll take far less room in your cargo holds.
        """
        if (self.weight() != 0):
            return self.value()/float(self.weight())
        else:
            return 0

class Planet(object):
    """
    Just some basic data about a planet.  Nothing terribly exciting.
    """

    def __init__(self, idnum, name, ptype, tectonics, weather, temp, gravity, bio, bio_danger, mineral):
        self.idnum = idnum
        self.name = name
        self.ptype = ptype
        self.tectonics = tectonics
        self.weather = weather
        self.temp = temp
        self.gravity = gravity
        self.bio = bio
        self.bio_danger = bio_danger
        self.mineral = mineral

class Filter(object):
    """
    A class to hold filters that we'll use to limit systems/planets.
    """

    def __init__(self):
        """
        Initial filter doesn't actually contain anything.
        """
        self.reset()

    def reset(self):
        """
        Resets the individual filters to None
        """
        self.filters = []

    def add(self, new_filter):
        """
        Adds a new filter to the filter chain.
        """
        self.filters.append(new_filter)

    def filtering(self):
        """
        Returns whether or not we have an active filter.
        """
        return (len(self.filters) > 0)

    def approve(self, obj):
        """
        Returns true if the given object is approved, false if denied.
        """
        for fil in self.filters:
            if (not fil.approve(obj)):
                return False
        return True

class ProxDispFilter(object):
    """
    A class to hold filter information related to system proximity.
    """

    def __init__(self, from_system, radius):
        self.from_system = from_system
        self.radius = radius

    def approve(self, system):
        return (self.from_system and system.distance_to(self.from_system) <= self.radius)

class TypeDispFilter(object):
    """
    A class to hold filter information about what kinds of planets we'll accept.
    Note that we'll be getting passed a system to approve(), so we must loop through
    the planets ourselves.
    """

    def __init__(self, ptype):
        self.ptype = ptype
        self.typelen = len(self.ptype)

    def approve(self, system):
        """
        Returns true if the system contains a planet of the given type,
        or false if not.
        """
        for planet in system.planets:
            if (planet.ptype[:self.typelen] == self.ptype):
                return True
        return False

class NameDispFilter(object):
    """
    A class to hold filter information which matches system names.  Note that it'll
    also search in the 'extra' field if the 'special info' box is checked.
    """

    def __init__(self, name, specialchecked):
        self.name = name.lower()
        self.specialchecked = specialchecked

    def approve(self, system):
        """
        Returns true if the system matches the given name, false if not.
        """
        return (system.fullname.lower().find(self.name) > -1 or
                (self.specialchecked and system.extra.lower().find(self.name) > -1))

class ConstDispFilter(object):
    """
    A class to hold filter information which matches constellation names.
    """

    def __init__(self, name):
        self.name = name

    def approve(self, system):
        """
        Returns true if the system matches the given constellation name, false if not.
        """
        return (system.name == self.name)

class SafetyAggFilter(object):
    """
    A class to hold aggregate safety filter information, used to make the processing of
    mineral and bio data aggregates easier.
    """

    def __init__(self):
        """
        Initial filter will end up accepting all planets on the map
        """
        self.set_tectonics(8)
        self.set_weather(8)
        self.set_temp(5200)
        self.set_bio(400)

    def set_tectonics(self, tectonics_val, less_than=True):
        """
        Sets our tectonics match limit to `tectonics_val`.  If `less_than`
        is `True`, we'll use a <= match.  Otherwise, >=.
        """
        self.tectonics_val = tectonics_val
        if less_than:
            self.tectonics = self.tectonics_lte
        else:
            self.tectonics = self.tectonics_gte

    def set_weather(self, weather_val, less_than=True):
        """
        Sets our weather match limit to `weather_val`.  If `less_than`
        is `True`, we'll use a <= match.  Otherwise, >=.
        """
        self.weather_val = weather_val
        if less_than:
            self.weather = self.weather_lte
        else:
            self.weather = self.weather_gte

    def set_temp(self, temp_val, less_than=True):
        """
        Sets our temp match limit to `temp_val`.  If `less_than`
        is `True`, we'll use a <= match.  Otherwise, >=.
        """
        self.temp_val = temp_val
        if less_than:
            self.temp = self.temp_lte
        else:
            self.temp = self.temp_gte

    def set_bio(self, bio_val, less_than=True):
        """
        Sets our bio match limit to `bio_val`.  If `less_than`
        is `True`, we'll use a <= match.  Otherwise, >=.
        """
        self.bio_val = bio_val
        if less_than:
            self.bio = self.bio_lte
        else:
            self.bio = self.bio_gte

    def approve(self, planet):
        """
        Returns true if the given planet is approved, false if denied.
        """
        return (self.tectonics(planet) and self.weather(planet) and self.temp(planet) and self.bio(planet))

    # The various functions for testing follow
    def tectonics_lte(self, planet):
        return (planet.tectonics <= self.tectonics_val)
    def tectonics_gte(self, planet):
        return (planet.tectonics >= self.tectonics_val)
    def weather_lte(self, planet):
        return (planet.weather <= self.weather_val)
    def weather_gte(self, planet):
        return (planet.weather >= self.weather_val)
    def temp_lte(self, planet):
        return (planet.temp <= self.temp_val)
    def temp_gte(self, planet):
        return (planet.temp >= self.temp_val)
    def bio_lte(self, planet):
        return (planet.bio_danger <= self.bio_val)
    def bio_gte(self, planet):
        return (planet.bio_danger >= self.bio_val)

class System(object):
    """
    Class to hold information about a specific system.  Most of the "fun"
    data in here is the aggregate data.  We keep track of two sets of
    aggregates; one which holds the total value of the system, and one
    which holds the value which might be modified by safety filters.
    """

    def __init__(self, idnum, name, position, x, y, stype, extra):
        self.is_quasispace = False
        self.idnum = idnum
        self.name = name
        self.x = x
        self.y = y
        # TODO: These two vars are GUI-specific; move 'em to there.
        self.draw_x = int(x/10)
        self.draw_y = 1000-int(y/10)
        self.position = position
        self.stype = stype
        self.extra = extra
        self.highlight = True
        self.planets = []
        self.mineral_agg = None
        self.mineral_agg_full = None
        self.bio_agg = None
        self.bio_agg_full = None
        self.bio_danger_agg = None
        self.bio_danger_agg_full = None
        if (self.position and self.position != ''):
            self.fullname = '{} {}'.format(self.position, self.name)
        else:
            self.fullname = self.name

    def addplanet(self, planet):
        """
        Adds a planet to the system; only used when initially importing the data.
        Returns the Planet object again, for convenience.
        """
        self.planets.append(planet)
        return planet

    def distance_to(self, system):
        """
        Returns the distance between this system and the specified one
        """
        return (math.sqrt((self.x-system.x)**2+(self.y-system.y)**2)/10)

    def apply_filters(self, dispfilter, aggfilter):
        """
        Applies the given display and aggregate filters to our system.  Sets
        our internal `highlight` variable to indicate whether the system
        should be highlighted (ie: it succeeds in passing the `dispfilter`),
        and sets the internal aggregate variables based on the safety
        parameters defined by `aggfilter`.  Returns a tuple with two elements:
            1) The total mineral value, when `aggfilter` is taken into account
            2) The total bio value, when `aggfilter` is taken into account
        """
        self.highlight = dispfilter.approve(self)
        self.mineral_agg = MinData()
        self.mineral_agg_full = MinData()
        self.bio_agg = 0
        self.bio_agg_full = 0
        self.bio_danger_agg = 0
        self.bio_danger_agg_full = 0
        for planet in self.planets:
            self.bio_agg_full += planet.bio
            self.bio_danger_agg_full += planet.bio_danger
            self.mineral_agg_full.add(planet.mineral)
            if (aggfilter.approve(planet)):
                self.bio_agg += planet.bio
                self.bio_danger_agg += planet.bio_danger
                self.mineral_agg.add(planet.mineral)
        return (self.mineral_agg.value(), self.bio_agg)

class Quasispace(object):
    """
    Just a little class to hold quasispace exit information.  Not much more
    than a glorified dict, but this way we access all the data in the same
    way, and we can pretend to be a system.
    """

    # TODO: This is a GUI thing, should get moved into there
    quasi_offset = 425

    def __init__(self, x, y, qs_x, qs_y, label):
        self.x = x
        self.y = y
        # TODO: these, too, are GUI.  Pull 'em out of here
        self.draw_x = int(x/10)
        self.draw_y = 1000-int(y/10)
        self.qs_x = qs_x
        self.qs_y = qs_y
        # TODO: Guiiiiiiiii....
        self.draw_quasi_x = qs_x-Quasispace.quasi_offset
        self.draw_quasi_y = (1000-qs_y)-Quasispace.quasi_offset
        self.label = label
        self.is_quasispace = True
        self.fullname = 'Quasispace Exit {}'.format(label)
        self.extra = ''

    def distance_to(self, system):
        """
        Returns the distance between this system and the specified one
        """
        return (math.sqrt((self.x-system.x)**2+(self.y-system.y)**2)/10)

class Systems(object):
    """
    Aggregate class to hold all of our systems.

    Note that we set up two global filters - one to filter aggregate data based
    on planets (ie: the saftey filter), and the other to filter highlighting of
    systems (ie: proximity, etc).  By default these will be empty, and approve
    all systems/planets.
    """

    def __init__(self):
        self.dispfilter = Filter()
        self.aggfilter = Filter()
        self.systems = {}
        self.agg_min_value = 9999
        self.agg_max_value = 0
        self.agg_spread = 0
        self.bio_agg_min_value = 9999
        self.bio_agg_max_value = 0
        self.bio_agg_spread = 0
        self.connections = []
        self.quasispace = []

        self.constellation_names = set()
        self.planet_types = set()

    def add_system(self, idnum, name, position, x, y, stype, extra):
        """
        Add a new system, only used during the initial import.  Returns
        the new System object.
        """
        self.systems[idnum] = System(idnum, name, position, x, y, stype, extra)
        self.constellation_names.add(name)
        return self.systems[idnum]

    def add_quasi(self, x, y, qs_x, qs_y, label):
        """
        Adds a new quasispace exit, only used during the initial import.
        """
        self.systems[label] = Quasispace(x, y, qs_x, qs_y, label)
        self.quasispace.append(self.systems[label])
        return self.systems[label]

    def add_planet_type(self, planet):
        """
        Adds a new planet type to our main set of planet types.  Used mostly just
        for the GUI to draw a selection dropdown.  This is only really ever called
        from `load_from_json`.
        """
        if planet.ptype[-6:] == ' World':
            self.planet_types.add(planet.ptype[:-6])
        else:
            self.planet_types.add(planet.ptype)

    def get(self, idnum):
        """
        Returns a system given its ID.
        """
        try:
            return self.systems[idnum]
        except KeyError:
            return None

    def getall(self):
        """
        Returns a list of all of the systems we know about
        """
        return self.systems.values()

    def process_aggregates(self):
        """
        Loop through all of our systems and calculate its aggregate values, using the
        given filters.  Will also set the "highlight" var for each system
        accordingly.  Will only calculate min/max values for planets which
        are set to be highlighted (so that the color spread will be accurate)
        """
        self.agg_min_value = 9999
        self.agg_max_value = 0
        self.agg_spread = 0
        self.bio_agg_min_value = 9999
        self.bio_agg_max_value = 0
        self.bio_agg_spread = 0
        for system in self.getall():
            if (system.is_quasispace):
                continue
            (mineral, bio) = system.apply_filters(self.dispfilter, self.aggfilter)
            if system.highlight:
                if (mineral < self.agg_min_value):
                    self.agg_min_value = mineral
                if (mineral > self.agg_max_value):
                    self.agg_max_value = mineral
                if (bio < self.bio_agg_min_value):
                    self.bio_agg_min_value = bio
                if (bio > self.bio_agg_max_value):
                    self.bio_agg_max_value = bio

        # The checks in here would only occur if no systems have been loaded,
        # or if no systems match the given filters
        if self.agg_min_value == 9999 and self.agg_max_value == 0:
            self.agg_min_value = 0
        else:
            self.agg_spread = float(self.agg_max_value - self.agg_min_value)
        if self.bio_agg_min_value == 9999 and self.bio_agg_max_value == 0:
            self.bio_agg_min_value = 0
        else:
            self.bio_agg_spread = float(self.bio_agg_max_value - self.bio_agg_min_value)

    def mineral_intensity(self, system):
        """
        Returns the mineral intensity of a given system, based on the calculated aggregates.
        This will be a value from 0 to 1.
        """
        if (self.agg_spread == 0):
            return 1
        else:
            return (system.mineral_agg.value()-self.agg_min_value)/self.agg_spread

    def bio_intensity(self, system):
        """
        Returns the biological intensity of a given system, based on the calculated aggregates.
        This will be a value from 0 to 1.
        """
        if (self.bio_agg_spread == 0):
            return 1
        else:
            return (system.bio_agg-self.bio_agg_min_value)/self.bio_agg_spread

    @staticmethod
    def load_from_json(json_string):
        """
        Returns a new `Systems` objects based on a JSON string passed in.  The
        JSON string should have a top-level dict, laid out in pseudostructure
        like so:

        {
            'systems': [
                {
                    'sid': <System ID Number>,
                    'name': <System Name>,
                    'position': <System Position (Alpha, Beta, ...)>,
                    'x': <x coordinate>,
                    'y': <y coordinate>,
                    'stype': <system type (green dwarf, orange giant, ...)>,
                    'extra': <extra info (homeworlds, melnorme trading posts, ...)>,
                },
                ...
            ],
            'planets': [
                {
                    'pid': <Planet ID Number>,
                    'sid': <System ID Number (foreign key to 'systems', basically),
                    'pname': <Planet Name ("Planet I", etc)>,
                    'ptype': <Planet Type (Acid World, ...)>,
                    'tectonics': <Tectonics Level>,
                    'weather': <Weather Level>,
                    'temp': <Temperature>,
                    'gravity': <Gravity Level>,
                    'bio': <Total Bio Value>,
                    'bio_danger': <Total "Dangerous" Bio Value>,
                    'mineral': <Total Mineral Count (weight)>,
                    'min_common': <Total Common Mineral Count (weight)>,
                    'min_corrosive': <Total Corrosive Mineral Count (weight)>,
                    'min_base': <Total Base Mineral Count (weight)>,
                    'min_noble': <Total Noble Mineral Count (weight)>,
                    'min_rare': <Total Rare Mineral Count (weight)>,
                    'min_precious': <Total Precious Mineral Count (weight)>,
                    'min_radio': <Total Radioactive Mineral Count (weight)>,
                    'min_exotic': <Total Exotic Mineral Count (weight)>,
                },
                ...
            ],
            'quasispace': [
                {
                    'label': <label>,
                    'x': <x coordinate in hyperspace>,
                    'y': <y coordinate in hyperspace>,
                    'qs_x': <x coordinate in quasispace>,
                    'qs_y': <y coordinate in quasispace>,
                },
                ...
            ],
            'constellations': {
                "<system ID Number>": [
                    <system ID Number>,
                    ...
                ],
                ...
            },
        }

        The `constellations` dict basically just defines what lines should be
        drawn.  For instance, the Vulpeculae system (where the Orz can be
        found) has a central star with a bunch of spokes coming out of it,
        so the most efficient way to define that in the `constellations` dict
        is:

            "2250": [2245, 2247, 2251, 2258, 2255, 2248],

        ... where 2250 is the ID of the central system, and the rest are the
        spokes.  (JSON dict keys can't be ints, hence the string there.)
        Most constellations can't be specified quite so compactly, of course.
        Sextantis, for instance, is a line of six systems, so its most compact
        form looks like:

            "2171": [2167, 2159],
            "2157": [2159, 2164],
            "2170": [2164],

        And of course there's no need to be as compact as possible; the
        Vulpeculae system from above could just as easily be written as:

            "2250": [2245],
            "2250": [2247],
            "2250": [2251],
            "2250": [2258],
            "2250": [2255],
            "2250": [2248],

        ... and the order of each of those pairs could be reversed, as well.

        """

        # Process the JSON string
        data = json.loads(json_string)

        # Create our systems
        systems = Systems()
        for system in data['systems']:
            systems.add_system(system['sid'], system['name'], system['position'], system['x'], system['y'], system['stype'], system['extra'])

        # Make sure we store our list of quasispace exits, too
        for quasi in data['quasispace']:
            systems.add_quasi(quasi['x'], quasi['y'], quasi['qs_x'], quasi['qs_y'], quasi['label'])

        # ... and now a list of planets
        for planet in data['planets']:
            p = systems.get(planet['sid']).addplanet(Planet(
                    planet['pid'], planet['pname'], planet['ptype'], planet['tectonics'], planet['weather'], planet['temp'], planet['gravity'],
                    planet['bio'], planet['bio_danger'],
                    MinData(planet['min_common'], planet['min_corrosive'], planet['min_base'], planet['min_noble'],
                        planet['min_rare'], planet['min_precious'], planet['min_radio'], planet['min_exotic'])
                    )
                )
            systems.add_planet_type(p)

        # Let's process our constellation connection information too.
        for (system_id, link_ids) in data['constellations'].items():
            # JSON dict keys cannot be ints, so we've gotta cast here.
            system_id = int(system_id)
            system = systems.systems[system_id]
            for link_id in link_ids:
                link_system = systems.systems[link_id]
                systems.connections.append((system, link_system))

        # ... this should happen automatically, but regardless:
        data = None

        # Run through aggregates and calc min/max
        systems.process_aggregates()

        # ... and return the systems object
        return systems

    @staticmethod
    def load_from_file(filename=None):
        """
        Returns a new `Systems` object based on data from the specified `filename`.
        If `filename` is not passed in, we will attempt to find our main data
        file.

        The file should be gzipped JSON, encoded with utf-8, in the format
        described by `load_from_json`.
        """

        # TODO: This bit should be modified to work if we ever get around to
        # packaging this properly with a setup.py, so it can find that data
        # dir.
        if not filename:
            filename = os.path.join(
                os.path.dirname(__file__),
                '..',
                'data',
                'uqm.json.gz',
                )

        with gzip.GzipFile(filename, 'r') as df:
            return Systems.load_from_json(df.read().decode('utf-8'))
