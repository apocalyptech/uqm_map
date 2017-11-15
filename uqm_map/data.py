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
import string
import os.path

class MinData(object):
    """
    A class to hold mineral data.  Each planet has one of these, and each
    system uses a few of these for aggregate data as well.
    """

    def __init__(self, common=0, corrosive=0, base=0, noble=0, rare=0, precious=0, radioactive=0, exotic=0):
        self.common = common
        self.corrosive = corrosive
        self.base = base
        self.noble = noble
        self.rare = rare
        self.precious = precious
        self.radioactive = radioactive
        self.exotic = exotic

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
        self.quasi = False
        self.idnum = idnum
        self.name = name
        self.x = x
        self.y = y
        self.draw_x = int(x/10)
        self.draw_y = 1000-int(y/10)
        self.position = position
        self.stype = stype
        self.extra = extra
        self.highlight = True
        self.planets = []
        self.min_agg = None
        self.min_agg_full = None
        self.bio_agg = None
        self.bio_agg_full = None
        self.bio_danger_agg = None
        self.bio_danger_agg_full = None
        if (self.position and self.position != ''):
            self.fullname = '{} {}'.format(self.position, self.name)
        else:
            self.fullname = self.name
        self.quasispace = False

    def addplanet(self, planet):
        """
        Adds a planet to the system; only used when initially importing the data
        """
        self.planets.append(planet)

    def distance_to(self, system):
        """
        Returns the distance between this system and the specified one
        """
        if system:
            return (math.sqrt((self.x-system.x)**2+(self.y-system.y)**2)/10)

    def set_aggregate(self, dispfilter, aggfilter):
        """
        Sets the aggregate mineral/bio value of the planet, using the given
        filters.  Will set the "highlight" property appropriately.
        """
        self.highlight = dispfilter.approve(self)
        self.min_agg = MinData()
        self.min_agg_full = MinData()
        self.bio_agg = 0
        self.bio_agg_full = 0
        self.bio_danger_agg = 0
        self.bio_danger_agg_full = 0
        for planet in self.planets:
            self.bio_agg_full += planet.bio
            self.bio_danger_agg_full += planet.bio_danger
            for mineral in min_vals:
                self.min_agg_full.__dict__[mineral] += planet.mineral.__dict__[mineral]
            if (aggfilter.approve(planet)):
                self.bio_agg += planet.bio
                self.bio_danger_agg += planet.bio_danger
                for mineral in min_vals:
                    self.min_agg.__dict__[mineral] += planet.mineral.__dict__[mineral]
        return (self.min_agg.value(), self.bio_agg)

    # Aggregate reporting follows;  I suppose this isn't very Pythonic, but
    # it means slightly less typing later on.  Go figure.
    def agg_value(self):
        return self.min_agg.value()
    def agg_weight(self):
        return self.min_agg.weight()
    def agg_worth(self):
        return self.min_agg.worth()
    def full_agg_value(self):
        return self.min_agg_full.value()
    def full_agg_weight(self):
        return self.min_agg_full.weight()
    def full_agg_worth(self):
        return self.min_agg_full.worth()
    def bio_agg_value(self):
        return self.bio_agg
    def full_bio_agg_value(self):
        return self.bio_agg_full
    def bio_danger_agg_value(self):
        return self.bio_danger_agg
    def full_bio_danger_agg_value(self):
        return self.bio_danger_agg_full

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
        self.coords = []
        self.agg_min_value = 9999
        self.agg_max_value = 0
        self.agg_spread = 0
        self.bio_agg_min_value = 9999
        self.bio_agg_max_value = 0
        self.bio_spread = 0
        self.connections = []
        self.quasispace = []
        for x in range(1001):
            self.coords.append([])
            for y in range(1001):
                self.coords[x].append(None)

    def add(self, idnum, name, position, x, y, stype, extra):
        """
        Add a new system, only used during the initial import.
        """
        self.systems[idnum] = System(idnum, name, position, x, y, stype, extra)
        self.coords[self.systems[idnum].draw_x][self.systems[idnum].draw_y] = self.systems[idnum]

    def add_quasi(self, x, y, qs_x, qs_y, label):
        """
        Adds a new quasispace exit, only used during the initial import.
        """
        self.systems[label] = Quasispace(x, y, qs_x, qs_y, label)
        self.coords[self.systems[label].draw_x][self.systems[label].draw_y] = self.systems[label]
        self.quasispace.append(self.systems[label])

    def get(self, idnum):
        """
        Returns a system given its ID.
        """
        try:
            return self.systems[idnum]
        except KeyError:
            return None

    def lookup(self, x, y):
        """
        Looks up a system given an (x,y) coord from the map
        """
        return self.coords[int(x)][int(y)]

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
        self.bio_spread = 0
        for system in self.getall():
            if (system.quasi):
                continue
            (mineral, bio) = system.set_aggregate(self.dispfilter, self.aggfilter)
            if (system.highlight):
                if (mineral < self.agg_min_value):
                    self.agg_min_value = mineral
                if (mineral > self.agg_max_value):
                    self.agg_max_value = mineral
                if (bio < self.bio_agg_min_value):
                    self.bio_agg_min_value = bio
                if (bio > self.bio_agg_max_value):
                    self.bio_agg_max_value = bio
        self.agg_spread = float(self.agg_max_value - self.agg_min_value)
        self.bio_spread = float(self.bio_agg_max_value - self.bio_agg_min_value)

    def ret_intensity(self, system):
        """
        Returns the mineral intensity of a given system, based on the calculated aggregates.
        """
        if (self.agg_spread == 0):
            return 100
        else:
            return (system.agg_value()-self.agg_min_value)/self.agg_spread

    def ret_bio_intensity(self, system):
        """
        Returns the biological intensity of a given system, based on the calculated aggregates.
        """
        if (self.bio_spread == 0):
            return 100
        else:
            return (system.bio_agg_value()-self.bio_agg_min_value)/self.bio_spread

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
        self.draw_x = int(x/10)
        self.draw_y = 1000-int(y/10)
        self.qs_x = qs_x
        self.qs_y = qs_y
        self.draw_quasi_x = qs_x-Quasispace.quasi_offset
        self.draw_quasi_y = (1000-qs_y)-Quasispace.quasi_offset
        self.id = label
        self.quasi = True
        self.fullname = 'Quasispace Exit {}'.format(label)

    def distance_to(self, system):
        """
        Returns the distance between this system and the specified one
        """
        if system:
            return (math.sqrt((self.x-system.x)**2+(self.y-system.y)**2)/10)

def get_systems(filename):
    """
    Returns our main `Systems` object containing all the data for the game,
    given `filename` which should be a gzipped JSON file.
    """

    data = None
    with gzip.GzipFile(filename, 'r') as df:
        data = json.loads(df.read().decode('utf-8'))
    if data is None:
        raise Exception('Data not found in {}'.format(filename))

    planet_types = {}
    const_names = {}

    # Create our systems
    systems = Systems()
    for system in data['systems']:
        systems.add(system['sid'], system['name'], system['position'], system['x'], system['y'], system['stype'], system['extra'])
        const_names[system['name']] = True

    # Make sure we store our list of quasispace exits, too
    for quasi in data['quasispace']:
        systems.add_quasi(quasi['x'], quasi['y'], quasi['qs_x'], quasi['qs_y'], quasi['label'])

    # ... and now a list of planets
    for planet in data['planets']:
        systems.get(planet['sid']).addplanet(Planet(
                planet['pid'], planet['pname'], planet['ptype'], planet['tectonics'], planet['weather'], planet['temp'], planet['gravity'],
                planet['bio'], planet['bio_danger'],
                MinData(planet['min_common'], planet['min_corrosive'], planet['min_base'], planet['min_noble'],
                    planet['min_rare'], planet['min_precious'], planet['min_radio'], planet['min_exotic'])
                )
            )
        if (planet['ptype'][-6:] == ' World'):
            planet_types[planet['ptype'][:-6]] = True
        else:
            planet_types[planet['ptype']] = True

    # Let's process our constellation connection information too.
    for (sid, lids) in data['constellations'].items():
        ssystem = systems.systems[sid]
        ssys_x = ssystem.draw_x
        ssys_y = ssystem.draw_y
        for lid in lids:
            lsystem = systems.systems[lid]
            systems.connections.append(((ssys_x, ssys_y), (lsystem.draw_x, lsystem.draw_y)))

    # ... this should happen automatically, but regardless:
    data = None

    # Run through aggregates and calc min/max
    systems.process_aggregates()

    # ... and return the systems object
    return systems
