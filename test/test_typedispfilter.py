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

from uqm_map.data import TypeDispFilter, System, Planet

class TypeDispFilterTests(unittest.TestCase):
    """
    Tests for our `TypeDispFilter` class.  This filters systems based on the
    types of planets they contain.
    """

    def setUp(self):
        """
        Some objects which we're likely to want in various tests
        """
        self.planet_acid = Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 0, 0, 0)
        self.planet_chlorine = Planet(2, 'Chlorine', 'Chlorine World', 1, 1, 100, 1, 0, 0, 0)
        self.planet_dust = Planet(3, 'Dust', 'Dust World', 1, 1, 100, 1, 0, 0, 0)
        self.planet_emerald = Planet(4, 'Emerald', 'Emerald World', 1, 1, 100, 1, 0, 0, 0)

    def test_init(self):
        """
        Tests our basic initialization routine
        """
        tdf = TypeDispFilter('Green')
        self.assertEqual(tdf.ptype, 'Green')
        self.assertEqual(tdf.typelen, 5)

    def test_match_full(self):
        """
        Tests matching a full type
        """
        tdf = TypeDispFilter('Acid World')
        system = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        system.addplanet(self.planet_acid)
        self.assertEqual(tdf.approve(system), True)

    def test_match_substring(self):
        """
        Tests matching a substring type
        """
        tdf = TypeDispFilter('Acid')
        system = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        system.addplanet(self.planet_acid)
        self.assertEqual(tdf.approve(system), True)

    def test_no_match(self):
        """
        Tests matching a system which doesn't match
        """
        tdf = TypeDispFilter('Acid World')
        system = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        system.addplanet(self.planet_chlorine)
        self.assertEqual(tdf.approve(system), False)

    def test_match_multiple(self):
        """
        Tests matching a system with more than one planet
        """
        tdf = TypeDispFilter('Acid World')
        system = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        system.addplanet(self.planet_dust)
        system.addplanet(self.planet_chlorine)
        system.addplanet(self.planet_acid)
        self.assertEqual(tdf.approve(system), True)

    def test_no_match_multiple(self):
        """
        Tests matching a system with more than one planet which doesn't match
        """
        tdf = TypeDispFilter('Acid World')
        system = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        system.addplanet(self.planet_emerald)
        system.addplanet(self.planet_dust)
        system.addplanet(self.planet_chlorine)
        self.assertEqual(tdf.approve(system), False)

    def test_no_match_empty(self):
        """
        Tests matching an empty system (should fail)
        """
        tdf = TypeDispFilter('Acid World')
        system = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        self.assertEqual(tdf.approve(system), False)
