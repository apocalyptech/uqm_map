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

from uqm_map.data import System, Planet, MinData, Filter, TypeDispFilter, SafetyAggFilter

class SystemTests(unittest.TestCase):
    """
    Tests for our `System` class.  This is the class which describes a
    system and holds a bunch of Planet objects.  
    """

    def setUp(self):
        """
        Some vars we might need on (nearly) every test
        """
        self.s = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', 'hint')

    def test_init(self):
        """
        Tests our basic initialization routine
        """
        self.assertEqual(self.s.idnum, 1)
        self.assertEqual(self.s.name, 'System')
        self.assertEqual(self.s.position, 'Alpha')
        self.assertEqual(self.s.x, 5000)
        self.assertEqual(self.s.y, 5000)
        self.assertEqual(self.s.stype, 'blue dwarf')
        self.assertEqual(self.s.extra, 'hint')
        self.assertEqual(self.s.fullname, 'Alpha System')
        self.assertEqual(self.s.is_quasispace, False)

    def test_init_no_position(self):
        """
        Tests our basic initialization routine without a `position`
        argument (or, more accurately, with an empty string for `position`)
        """
        s = System(1, 'System', '', 5000, 5000, 'blue dwarf', 'hint')
        self.assertEqual(s.fullname, 'System')

    def test_add_one_planet(self):
        """
        Tests adding a single planet
        """
        self.assertEqual(len(self.s.planets), 0)
        p = Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 0, 0, MinData())
        p2 = self.s.addplanet(p)
        self.assertEqual(p, p2)
        self.assertEqual(len(self.s.planets), 1)

    def test_add_two_planets(self):
        """
        Tests adding two planets
        """
        self.assertEqual(len(self.s.planets), 0)
        self.s.addplanet(Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 0, 0, MinData()))
        self.s.addplanet(Planet(2, 'Chlorine', 'Chlorine World', 1, 1, 100, 1, 0, 0, MinData()))
        self.assertEqual(len(self.s.planets), 2)

    def test_distance_to_self(self):
        """
        Tests computing the distance to ourself
        """
        self.assertAlmostEqual(self.s.distance_to(self.s), 0)

    def test_distance_close(self):
        """
        Tests computing the distance to another system close by
        """
        s2 = System(2, 'System', 'Beta', 5500, 5000, 'blue dwarf', '')
        self.assertAlmostEqual(self.s.distance_to(s2), 50)

    def test_distance_diagonal(self):
        """
        Tests computing the distance to another system at a diagonal
        """
        s2 = System(2, 'System', 'Beta', 3000, 7000, 'blue dwarf', '')
        self.assertAlmostEqual(self.s.distance_to(s2), 282.84, 2)

    def test_apply_filters_empty_filters(self):
        """
        Tests applying filters when there are none to apply.  System should
        remain highlighted, and all planetary resources included in the
        aggregate.
        """
        self.s.addplanet(Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 10, 5, MinData(
            base=3,
            )))
        self.s.addplanet(Planet(2, 'Chlorine', 'Chlorine World', 1, 1, 100, 1, 15, 10, MinData(
            base=1,
            radioactive=5,
            )))
        self.s.apply_filters(Filter(), Filter())
        self.assertEqual(self.s.highlight, True)
        self.assertEqual(self.s.mineral_agg.value(), 52)
        self.assertEqual(self.s.mineral_agg_full.value(), 52)
        self.assertEqual(self.s.mineral_agg.base, 4)
        self.assertEqual(self.s.mineral_agg_full.base, 4)
        self.assertEqual(self.s.mineral_agg.radioactive, 5)
        self.assertEqual(self.s.mineral_agg_full.radioactive, 5)
        self.assertEqual(self.s.bio_agg, 25)
        self.assertEqual(self.s.bio_agg_full, 25)
        self.assertEqual(self.s.bio_danger_agg, 15)
        self.assertEqual(self.s.bio_danger_agg_full, 15)

    def test_apply_filters_dont_highlight(self):
        """
        Tests applying filters when one makes the system not highlight
        """
        self.s.addplanet(Planet(2, 'Chlorine', 'Chlorine World', 1, 1, 100, 1, 15, 10, MinData(
            base=1,
            radioactive=5,
            )))
        f = Filter()
        f.add(TypeDispFilter('Syreen'))
        self.s.apply_filters(f, Filter())
        self.assertEqual(self.s.highlight, False)
        self.assertEqual(self.s.mineral_agg.value(), 43)
        self.assertEqual(self.s.mineral_agg_full.value(), 43)
        self.assertEqual(self.s.bio_agg, 15)
        self.assertEqual(self.s.bio_agg_full, 15)
        self.assertEqual(self.s.bio_danger_agg, 10)
        self.assertEqual(self.s.bio_danger_agg_full, 10)

    def test_apply_filters_no_planet_matches(self):
        """
        Tests applying filters when no planets match the aggregate filter
        """
        self.s.addplanet(Planet(2, 'Chlorine', 'Chlorine World', 1, 1, 100, 1, 15, 10, MinData(
            base=1,
            radioactive=5,
            )))
        f = Filter()
        saf = SafetyAggFilter()
        saf.set_tectonics(3, False)
        f.add(saf)
        self.s.apply_filters(Filter(), f)
        self.assertEqual(self.s.highlight, True)
        self.assertEqual(self.s.mineral_agg.value(), 0)
        self.assertEqual(self.s.mineral_agg_full.value(), 43)
        self.assertEqual(self.s.bio_agg, 0)
        self.assertEqual(self.s.bio_agg_full, 15)
        self.assertEqual(self.s.bio_danger_agg, 0)
        self.assertEqual(self.s.bio_danger_agg_full, 10)

    def test_apply_filters_one_planet_matches(self):
        """
        Tests applying filters when one planet matches the aggregate filter.
        """
        self.s.addplanet(Planet(1, 'Acid', 'Acid World', 4, 4, 100, 1, 10, 5, MinData(
            base=3,
            )))
        self.s.addplanet(Planet(2, 'Chlorine', 'Chlorine World', 1, 1, 100, 1, 15, 10, MinData(
            base=1,
            radioactive=5,
            )))
        f = Filter()
        saf = SafetyAggFilter()
        saf.set_tectonics(3, False)
        f.add(saf)
        self.s.apply_filters(Filter(), f)
        self.assertEqual(self.s.highlight, True)
        self.assertEqual(self.s.mineral_agg.value(), 9)
        self.assertEqual(self.s.mineral_agg_full.value(), 52)
        self.assertEqual(self.s.mineral_agg.base, 3)
        self.assertEqual(self.s.mineral_agg_full.base, 4)
        self.assertEqual(self.s.mineral_agg.radioactive, 0)
        self.assertEqual(self.s.mineral_agg_full.radioactive, 5)
        self.assertEqual(self.s.bio_agg, 10)
        self.assertEqual(self.s.bio_agg_full, 25)
        self.assertEqual(self.s.bio_danger_agg, 5)
        self.assertEqual(self.s.bio_danger_agg_full, 15)
