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
import unittest

from uqm_map.data import Systems, System, Planet, MinData, NameDispFilter, SafetyAggFilter

class SystemsTests(unittest.TestCase):
    """
    Tests for our `Systems` class.  This is the main class which holds information
    about the entire starmap.
    """

    def setUp(self):
        """
        Some vars we might need on (nearly) every test
        """
        self.s = Systems()

    def test_init(self):
        """
        Tests basic initialization
        """
        self.assertEqual(list(self.s.getall()), [])
        self.assertEqual(len(self.s.constellation_names), 0)
        self.assertEqual(len(self.s.planet_types), 0)
        self.assertEqual(self.s.connections, [])

    def test_add_single(self):
        """
        Tests adding a system (this and the next few tests also happen to
        test `get()` and `getall()`.
        """
        sys = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        self.assertEqual(list(self.s.getall()), [sys])
        self.assertEqual(self.s.get(1), sys)
        self.assertEqual(len(self.s.constellation_names), 1)
        self.assertIn('System', self.s.constellation_names)

    def test_add_two_systems(self):
        """
        Tests adding two systems
        """
        sys1 = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys2 = self.s.add_system(2, 'System', 'Beta', 5500, 5500, 'blue dwarf', '')
        systems = list(self.s.getall())
        self.assertIn(sys1, systems)
        self.assertIn(sys2, systems)
        self.assertEqual(self.s.get(1), sys1)
        self.assertEqual(self.s.get(2), sys2)
        self.assertEqual(len(self.s.constellation_names), 1)
        self.assertIn('System', self.s.constellation_names)

    def test_add_two_different_systems(self):
        """
        Tests adding two systems with different constellation names
        """
        sys1 = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys2 = self.s.add_system(2, 'SystemTwo', 'Alpha', 5500, 5500, 'blue dwarf', '')
        systems = list(self.s.getall())
        self.assertIn(sys1, systems)
        self.assertIn(sys2, systems)
        self.assertEqual(self.s.get(1), sys1)
        self.assertEqual(self.s.get(2), sys2)
        self.assertEqual(len(self.s.constellation_names), 2)
        self.assertIn('System', self.s.constellation_names)
        self.assertIn('SystemTwo', self.s.constellation_names)

    def test_add_quasispace(self):
        """
        Tests adding a Quasispace system
        """
        q = self.s.add_quasi(4900, 4900, 3000, 3000, 'C')
        self.assertEqual(list(self.s.getall()), [q])
        self.assertEqual(self.s.get('C'), q)
        self.assertEqual(len(self.s.constellation_names), 0)

    def test_add_two_quasispace(self):
        """
        Tests adding two Quasispace systems
        """
        q1 = self.s.add_quasi(4900, 4900, 3000, 3000, 'C')
        q2 = self.s.add_quasi(5000, 5000, 2000, 2000, 'A')
        systems = list(self.s.getall())
        self.assertIn(q1, systems)
        self.assertIn(q2, systems)
        self.assertEqual(self.s.get('C'), q1)
        self.assertEqual(self.s.get('A'), q2)
        self.assertEqual(len(self.s.constellation_names), 0)

    def test_add_planet_type_single(self):
        """
        Tests `add_planet_type` by adding a single planet
        """
        p = Planet(1, 'Planet I', 'Acid World', 1, 1, 100, 1, 10, 5, MinData())
        self.s.add_planet_type(p)
        self.assertEqual(len(self.s.planet_types), 1)
        self.assertIn('Acid', self.s.planet_types)

    def test_add_planet_type_double(self):
        """
        Tests `add_planet_type` by adding a two planets with the same type
        """
        p = Planet(1, 'Planet I', 'Acid World', 1, 1, 100, 1, 10, 5, MinData())
        p2 = Planet(2, 'Planet II', 'Acid World', 1, 1, 100, 1, 10, 5, MinData())
        self.s.add_planet_type(p)
        self.s.add_planet_type(p2)
        self.assertEqual(len(self.s.planet_types), 1)
        self.assertIn('Acid', self.s.planet_types)

    def test_add_planet_type_no_world(self):
        """
        Tests `add_planet_type` by adding a single planet whose type does not
        include "World".  (Are there any planets actually like this?)
        """
        p = Planet(1, 'Planet I', 'StarBase', 1, 1, 100, 1, 10, 5, MinData())
        self.s.add_planet_type(p)
        self.assertEqual(len(self.s.planet_types), 1)
        self.assertIn('StarBase', self.s.planet_types)

    def test_add_planet_type_two_types(self):
        """
        Tests `add_planet_type` by adding a two planets with different types
        """
        p = Planet(1, 'Planet I', 'Acid World', 1, 1, 100, 1, 10, 5, MinData())
        p2 = Planet(2, 'Planet II', 'Treasure World', 1, 1, 100, 1, 10, 5, MinData())
        self.s.add_planet_type(p)
        self.s.add_planet_type(p2)
        self.assertEqual(len(self.s.planet_types), 2)
        self.assertIn('Acid', self.s.planet_types)
        self.assertIn('Treasure', self.s.planet_types)

    def test_get_no_systems(self):
        """
        Tests calling `get()` when there are no systems (other `get()`
        calls are pretty well tested by all the above tests).  Likewise
        for `getall()`.
        """
        self.assertEqual(self.s.get(1), None)

    def test_process_aggregates_no_systems(self):
        """
        Process aggregates when there are no systems (and no filters, for that
        matter).  Not very realistic, but whatever.
        """
        self.s.process_aggregates()
        self.assertEqual(self.s.agg_min_value, 0)
        self.assertEqual(self.s.agg_max_value, 0)
        self.assertEqual(self.s.agg_spread, 0)
        self.assertEqual(self.s.bio_agg_min_value, 0)
        self.assertEqual(self.s.bio_agg_max_value, 0)
        self.assertEqual(self.s.bio_agg_spread, 0)

    def test_process_aggregates_one_quasispace(self):
        """
        Process aggregates when there is one quasispace system in there (should
        be ignored)
        """
        self.s.add_quasi(4900, 4900, 3000, 3000, 'C')
        self.s.process_aggregates()
        self.assertEqual(self.s.agg_min_value, 0)
        self.assertEqual(self.s.agg_max_value, 0)
        self.assertEqual(self.s.agg_spread, 0)
        self.assertEqual(self.s.bio_agg_min_value, 0)
        self.assertEqual(self.s.bio_agg_max_value, 0)
        self.assertEqual(self.s.bio_agg_spread, 0)

    def test_process_aggregates_one_system(self):
        """
        Process aggregates when there is one system
        """
        sys = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys.addplanet(Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 10, 5, MinData(
            base=3,
            )))
        self.s.process_aggregates()
        self.assertEqual(self.s.agg_min_value, 9)
        self.assertEqual(self.s.agg_max_value, 9)
        self.assertEqual(self.s.agg_spread, 0)
        self.assertEqual(self.s.bio_agg_min_value, 10)
        self.assertEqual(self.s.bio_agg_max_value, 10)
        self.assertEqual(self.s.bio_agg_spread, 0)

    def test_process_aggregates_one_system_passes_display_filter(self):
        """
        Process aggregates when there is one system which passes the display
        filters
        """
        self.s.dispfilter.add(NameDispFilter('System', False))
        sys = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys.addplanet(Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 10, 5, MinData(
            base=3,
            )))
        self.s.process_aggregates()
        self.assertEqual(self.s.agg_min_value, 9)
        self.assertEqual(self.s.agg_max_value, 9)
        self.assertEqual(self.s.agg_spread, 0)
        self.assertEqual(self.s.bio_agg_min_value, 10)
        self.assertEqual(self.s.bio_agg_max_value, 10)
        self.assertEqual(self.s.bio_agg_spread, 0)

    def test_process_aggregates_one_system_fails_display_filter(self):
        """
        Process aggregates when there is one system which fails the display
        filters
        """
        self.s.dispfilter.add(NameDispFilter('Yehat', False))
        sys = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys.addplanet(Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 10, 5, MinData(
            base=3,
            )))
        self.s.process_aggregates()
        self.assertEqual(self.s.agg_min_value, 0)
        self.assertEqual(self.s.agg_max_value, 0)
        self.assertEqual(self.s.agg_spread, 0)
        self.assertEqual(self.s.bio_agg_min_value, 0)
        self.assertEqual(self.s.bio_agg_max_value, 0)
        self.assertEqual(self.s.bio_agg_spread, 0)

    def test_process_aggregates_two_planets_both_pass_agg_filter(self):
        """
        Process aggregates when there is one system whose planets all
        pass the aggregate filters
        """
        f = SafetyAggFilter()
        self.s.aggfilter.add(f)
        sys = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys.addplanet(Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 10, 5, MinData(
            base=3,
            )))
        sys.addplanet(Planet(2, 'Acid', 'Acid World', 3, 3, 100, 1, 5, 0, MinData(
            radioactive=3,
            )))
        self.s.process_aggregates()
        self.assertEqual(self.s.agg_min_value, 33)
        self.assertEqual(self.s.agg_max_value, 33)
        self.assertEqual(self.s.agg_spread, 0)
        self.assertEqual(self.s.bio_agg_min_value, 15)
        self.assertEqual(self.s.bio_agg_max_value, 15)
        self.assertEqual(self.s.bio_agg_spread, 0)

    def test_process_aggregates_two_planets_one_passes_agg_filter(self):
        """
        Process aggregates when there is one system in which only one planet passes
        the aggregate filters
        """
        f = SafetyAggFilter()
        f.set_weather(2)
        self.s.aggfilter.add(f)
        sys = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys.addplanet(Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 10, 5, MinData(
            base=3,
            )))
        sys.addplanet(Planet(2, 'Acid', 'Acid World', 3, 3, 100, 1, 5, 0, MinData(
            radioactive=3,
            )))
        self.s.process_aggregates()
        self.assertEqual(self.s.agg_min_value, 9)
        self.assertEqual(self.s.agg_max_value, 9)
        self.assertEqual(self.s.agg_spread, 0)
        self.assertEqual(self.s.bio_agg_min_value, 10)
        self.assertEqual(self.s.bio_agg_max_value, 10)
        self.assertEqual(self.s.bio_agg_spread, 0)

    def test_process_aggregates_two_planets_none_pass_agg_filter(self):
        """
        Process aggregates when there is one system in which none of its
        planets pass the aggregate filters
        """
        f = SafetyAggFilter()
        f.set_weather(2)
        self.s.aggfilter.add(f)
        sys = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys.addplanet(Planet(1, 'Acid', 'Acid World', 3, 3, 100, 1, 10, 5, MinData(
            base=3,
            )))
        sys.addplanet(Planet(2, 'Acid', 'Acid World', 3, 3, 100, 1, 5, 0, MinData(
            radioactive=3,
            )))
        self.s.process_aggregates()
        self.assertEqual(self.s.agg_min_value, 0)
        self.assertEqual(self.s.agg_max_value, 0)
        self.assertEqual(self.s.agg_spread, 0)
        self.assertEqual(self.s.bio_agg_min_value, 0)
        self.assertEqual(self.s.bio_agg_max_value, 0)
        self.assertEqual(self.s.bio_agg_spread, 0)

    def test_process_aggregates_two_systems(self):
        """
        Process aggregates when there are two systems
        """
        sys1 = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys1.addplanet(Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 10, 5, MinData(
            base=3,
            )))
        sys2 = self.s.add_system(2, 'System', 'Beta', 5500, 5500, 'blue dwarf', '')
        sys2.addplanet(Planet(2, 'Acid', 'Acid World', 1, 1, 100, 1, 5, 0, MinData(
            radioactive=3,
            )))
        self.s.process_aggregates()
        self.assertEqual(self.s.agg_min_value, 9)
        self.assertEqual(self.s.agg_max_value, 24)
        self.assertEqual(self.s.agg_spread, 15)
        self.assertEqual(self.s.bio_agg_min_value, 5)
        self.assertEqual(self.s.bio_agg_max_value, 10)
        self.assertEqual(self.s.bio_agg_spread, 5)

    def test_process_aggregates_three_systems(self):
        """
        Process aggregates when there are three systems
        """
        sys1 = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys1.addplanet(Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 10, 5, MinData(
            base=3,
            )))
        sys2 = self.s.add_system(2, 'System', 'Beta', 5500, 5500, 'blue dwarf', '')
        sys2.addplanet(Planet(2, 'Acid', 'Acid World', 1, 1, 100, 1, 5, 0, MinData(
            radioactive=3,
            )))
        sys3 = self.s.add_system(3, 'System', 'Gamma', 6000, 6000, 'blue dwarf', '')
        sys3.addplanet(Planet(3, 'Acid', 'Acid World', 1, 1, 100, 1, 0, 0, MinData(
            exotic=3,
            )))
        self.s.process_aggregates()
        self.assertEqual(self.s.agg_min_value, 9)
        self.assertEqual(self.s.agg_max_value, 75)
        self.assertEqual(self.s.agg_spread, 66)
        self.assertEqual(self.s.bio_agg_min_value, 0)
        self.assertEqual(self.s.bio_agg_max_value, 10)
        self.assertEqual(self.s.bio_agg_spread, 10)

    def test_process_aggregates_three_systems_two_disp_one_agg(self):
        """
        Process aggregates when there are three systems - two match the display
        filter and one is cut out by the aggregate.
        """
        f = SafetyAggFilter()
        f.set_weather(2)
        self.s.aggfilter.add(f)
        self.s.dispfilter.add(NameDispFilter('System', False))
        sys1 = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys1.addplanet(Planet(1, 'Acid', 'Acid World', 3, 3, 100, 1, 10, 5, MinData(
            base=3,
            )))
        sys2 = self.s.add_system(2, 'System', 'Beta', 5500, 5500, 'blue dwarf', '')
        sys2.addplanet(Planet(2, 'Acid', 'Acid World', 1, 1, 100, 1, 5, 0, MinData(
            radioactive=3,
            )))
        sys3 = self.s.add_system(3, 'Serpentis', 'Gamma', 6000, 6000, 'blue dwarf', '')
        sys3.addplanet(Planet(3, 'Acid', 'Acid World', 1, 1, 100, 1, 0, 0, MinData(
            exotic=3,
            )))
        self.s.process_aggregates()
        self.assertEqual(self.s.agg_min_value, 0)
        self.assertEqual(self.s.agg_max_value, 24)
        self.assertEqual(self.s.agg_spread, 24)
        self.assertEqual(self.s.bio_agg_min_value, 0)
        self.assertEqual(self.s.bio_agg_max_value, 5)
        self.assertEqual(self.s.bio_agg_spread, 5)

    def test_mineral_intensity_single(self):
        """
        Tests mineral intensity for a single system
        """
        sys1 = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys1.addplanet(Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 10, 5, MinData(
            base=3,
            )))
        self.s.process_aggregates()
        self.assertAlmostEqual(self.s.mineral_intensity(sys1), 1)

    def test_mineral_intensity_multiple(self):
        """
        Tests mineral intensity for multiple systems
        """
        sys1 = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys1.addplanet(Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 10, 5, MinData(
            base=3,
            )))
        sys2 = self.s.add_system(2, 'System', 'Beta', 5500, 5500, 'blue dwarf', '')
        sys2.addplanet(Planet(2, 'Acid', 'Acid World', 1, 1, 100, 1, 5, 0, MinData(
            radioactive=3,
            )))
        sys3 = self.s.add_system(3, 'System', 'Gamma', 6000, 6000, 'blue dwarf', '')
        sys3.addplanet(Planet(3, 'Acid', 'Acid World', 1, 1, 100, 1, 0, 0, MinData(
            exotic=3,
            )))
        self.s.process_aggregates()
        self.assertAlmostEqual(self.s.mineral_intensity(sys1), 0)
        self.assertAlmostEqual(self.s.mineral_intensity(sys2), .227, 3)
        self.assertAlmostEqual(self.s.mineral_intensity(sys3), 1)

    def test_bio_intensity_single(self):
        """
        Tests bio intensity for a single system
        """
        sys1 = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys1.addplanet(Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 10, 5, MinData(
            base=3,
            )))
        self.s.process_aggregates()
        self.assertAlmostEqual(self.s.bio_intensity(sys1), 1)

    def test_bio_intensity_multiple(self):
        """
        Tests bio intensity for multiple systems
        """
        sys1 = self.s.add_system(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        sys1.addplanet(Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 10, 5, MinData(
            base=3,
            )))
        sys2 = self.s.add_system(2, 'System', 'Beta', 5500, 5500, 'blue dwarf', '')
        sys2.addplanet(Planet(2, 'Acid', 'Acid World', 1, 1, 100, 1, 5, 0, MinData(
            radioactive=3,
            )))
        sys3 = self.s.add_system(3, 'System', 'Gamma', 6000, 6000, 'blue dwarf', '')
        sys3.addplanet(Planet(3, 'Acid', 'Acid World', 1, 1, 100, 1, 0, 0, MinData(
            exotic=3,
            )))
        self.s.process_aggregates()
        self.assertAlmostEqual(self.s.bio_intensity(sys3), 0)
        self.assertAlmostEqual(self.s.bio_intensity(sys2), .5)
        self.assertAlmostEqual(self.s.bio_intensity(sys1), 1)

    def test_load_from_json_no_data(self):
        """
        Tests loading from JSON when not actually passed any JSON data.
        """
        with self.assertRaises(Exception) as cm:
            Systems.load_from_json(None)

    def test_load_from_json_empty_string(self):
        """
        Tests loading from JSON when passed an empty string
        """
        with self.assertRaises(Exception) as cm:
            Systems.load_from_json('')

    def test_load_from_json_empty_hash(self):
        """
        Tests loading from JSON when passed an empty hash
        """
        with self.assertRaises(KeyError) as cm:
            Systems.load_from_json('{}')

    def test_load_from_json_empty_data(self):
        """
        Tests loading from JSON with technically valid but empty data
        """
        json_str = '{"systems": [], "quasispace": [], "planets": [], "constellations": {}}'
        s = Systems.load_from_json(json_str)
        self.assertEqual(list(self.s.getall()), [])
        self.assertEqual(len(self.s.constellation_names), 0)
        self.assertEqual(len(self.s.planet_types), 0)
        self.assertEqual(self.s.connections, [])

    def test_load_from_json_single_system_no_planets(self):
        """
        Tests loading from JSON with a single system (and no planets)
        """
        json_str = '{"systems": [{"sid": 1, "name": "System", "position": "Alpha",' \
            '"x": 5000, "y": 6000, "stype": "green dwarf", "extra": "homeworld"' \
            '}], "quasispace": [], "planets": [], "constellations": {}}'
        s = Systems.load_from_json(json_str)
        self.assertEqual(len(s.systems), 1)
        sys = s.get(1)
        self.assertEqual(sys.idnum, 1)
        self.assertEqual(sys.name, 'System')
        self.assertEqual(sys.position, 'Alpha')
        self.assertEqual(sys.x, 5000)
        self.assertEqual(sys.y, 6000)
        self.assertEqual(sys.stype, 'green dwarf')
        self.assertEqual(sys.extra, 'homeworld')
        self.assertEqual(sys.planets, [])
        self.assertEqual(len(s.constellation_names), 1)
        self.assertIn('System', s.constellation_names)

    def test_load_from_json_single_system_one_planet(self):
        """
        Tests loading from JSON with a single system and one planet
        """
        json_str = '{"systems": [{"sid": 1, "name": "System", "position": "Alpha",' \
            '"x": 5000, "y": 6000, "stype": "green dwarf", "extra": "homeworld"' \
            '}], "quasispace": [], "planets": [{"pid": 2, "sid": 1,' \
            '"pname": "Planet I", "ptype": "Acid World", "tectonics": 2, ' \
            '"weather": 3, "temp": 400, "gravity": 1, "bio": 100, "bio_danger": 50, ' \
            '"mineral": 123, ' \
            '"min_common": 1, ' \
            '"min_corrosive": 2, ' \
            '"min_base": 3, ' \
            '"min_noble": 4, ' \
            '"min_rare": 5, ' \
            '"min_precious": 6, ' \
            '"min_radio": 7, ' \
            '"min_exotic": 8 ' \
            '}], "constellations": {}}'
        s = Systems.load_from_json(json_str)
        self.assertEqual(len(s.systems), 1)
        sys = s.get(1)
        self.assertEqual(sys.idnum, 1)
        self.assertEqual(sys.name, 'System')
        self.assertEqual(sys.position, 'Alpha')
        self.assertEqual(sys.x, 5000)
        self.assertEqual(sys.y, 6000)
        self.assertEqual(sys.stype, 'green dwarf')
        self.assertEqual(sys.extra, 'homeworld')
        self.assertEqual(len(s.constellation_names), 1)
        self.assertIn('System', s.constellation_names)
        self.assertEqual(len(sys.planets), 1)
        p = sys.planets[0]
        self.assertEqual(p.idnum, 2)
        self.assertEqual(p.name, 'Planet I')
        self.assertEqual(p.ptype, 'Acid World')
        self.assertEqual(p.tectonics, 2)
        self.assertEqual(p.weather, 3)
        self.assertEqual(p.temp, 400)
        self.assertEqual(p.gravity, 1)
        self.assertEqual(p.bio, 100)
        self.assertEqual(p.bio_danger, 50)
        self.assertEqual(p.mineral.common, 1)
        self.assertEqual(p.mineral.corrosive, 2)
        self.assertEqual(p.mineral.base, 3)
        self.assertEqual(p.mineral.noble, 4)
        self.assertEqual(p.mineral.rare, 5)
        self.assertEqual(p.mineral.precious, 6)
        self.assertEqual(p.mineral.radioactive, 7)
        self.assertEqual(p.mineral.exotic, 8)
        self.assertEqual(len(s.planet_types), 1)
        self.assertIn('Acid', s.planet_types)

    def test_load_from_json_one_quasispace(self):
        """
        Tests loading from JSON with a single Quasispace exit
        """
        json_str = '{"systems": [], "quasispace": [' \
                '{"label": "A", "x": 5000, "y": 6000, ' \
                '"qs_x": 4000, "qs_y": 4500} ' \
                '], "planets": [], "constellations": {}}'
        s = Systems.load_from_json(json_str)
        self.assertEqual(len(s.quasispace), 1)
        q = s.quasispace[0]
        self.assertEqual(s.get('A'), q)
        self.assertEqual(q.label, 'A')
        self.assertEqual(q.x, 5000)
        self.assertEqual(q.y, 6000)
        self.assertEqual(q.qs_x, 4000)
        self.assertEqual(q.qs_y, 4500)

    def test_load_from_json_single_constellation(self):
        """
        Tests loading from JSON with two systems joined in a constellation
        """
        json_str = '{"systems": [' \
            '{"sid": 1, "name": "System", "position": "Alpha",' \
            '"x": 5000, "y": 6000, "stype": "green dwarf", "extra": "homeworld"' \
            '}, ' \
            '{"sid": 2, "name": "System", "position": "Beta",' \
            '"x": 6000, "y": 7000, "stype": "green dwarf", "extra": ""' \
            '} ' \
            '], "quasispace": [], "planets": [], "constellations": {' \
            '"1": [2]' \
            '}}'
        s = Systems.load_from_json(json_str)
        self.assertEqual(len(s.systems), 2)
        sys1 = s.get(1)
        sys2 = s.get(2)
        self.assertEqual(len(s.connections), 1)
        conn = s.connections[0]
        self.assertEqual(conn[0], sys1)
        self.assertEqual(conn[1], sys2)

    def test_load_from_file_default(self):
        """
        Test loading our main default datafile
        """
        s = Systems.load_from_file()
        self.assertEqual(len(s.systems), 518)
        self.assertEqual(len(s.quasispace), 16)
        self.assertEqual(len(s.connections), 424)
        self.assertEqual(len(s.planet_types), 53)
        self.assertEqual(len(s.constellation_names), 132)

    def test_load_from_file_invalid_file(self):
        """
        Tests loading from an invalid filename (ie: this test file)
        """
        with self.assertRaises(OSError) as cm:
            Systems.load_from_file(os.path.realpath(__file__))
        self.assertIn('Not a gzipped file', str(cm.exception))
