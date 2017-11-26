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
        p = Planet(1, 'Planet I', 'Moonbase', 1, 1, 100, 1, 10, 5, MinData())
        self.s.add_planet_type(p)
        self.assertEqual(len(self.s.planet_types), 1)
        self.assertIn('Moonbase', self.s.planet_types)

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
