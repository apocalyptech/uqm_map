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

from uqm_map.data import SafetyAggFilter, Planet

class SafetyAggFilterTests(unittest.TestCase):
    """
    Tests for our `SafetyAggFilter` class.  This is used to alter the
    reported RU/Bio values of planets in a system modified by the user's
    preference for safety (general presets from the GUI will be tiered
    based on Melnorme upgrades).

    Many of the tests here will set up planets which won't be matched
    by the default SafetyAggFilter parameters -- this won't be possible
    in UQM itself; the default values are set high enough to match all
    planets in UQM/SC2.
    """

    def setUp(self):
        """
        Vars we can use in most of our tests
        """
        self.saf = SafetyAggFilter()
        self.saf_r = SafetyAggFilter()
        self.saf_r.set_tectonics(3, False)
        self.saf_r.set_weather(3, False)
        self.saf_r.set_temp(50, False)
        self.saf_r.set_bio(50, False)

    def test_init(self):
        """
        Tests our basic initialization routine
        """
        self.assertEqual(self.saf.tectonics_val, 8)
        self.assertEqual(self.saf.weather_val, 8)
        self.assertEqual(self.saf.temp_val, 5200)
        self.assertEqual(self.saf.bio_val, 400)

    def test_match(self):
        """
        Tests matching on a planet.
        """
        p = Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 0, 0, 0)
        self.assertEqual(self.saf.approve(p), True)

    def test_no_match_tectonics(self):
        """
        Tests matching on a planet, which fails due to tectonics
        """
        p = Planet(1, 'Acid', 'Acid World', 9, 1, 100, 1, 0, 0, 0)
        self.assertEqual(self.saf.approve(p), False)

    def test_no_match_weather(self):
        """
        Tests matching on a planet, which fails due to weather
        """
        p = Planet(1, 'Acid', 'Acid World', 1, 9, 100, 1, 0, 0, 0)
        self.assertEqual(self.saf.approve(p), False)

    def test_no_match_temp(self):
        """
        Tests matching on a planet, which fails due to temp
        """
        p = Planet(1, 'Acid', 'Acid World', 1, 1, 10000, 1, 0, 0, 0)
        self.assertEqual(self.saf.approve(p), False)

    def test_no_match_bio(self):
        """
        Tests matching on a planet, which fails due to bio
        """
        p = Planet(1, 'Acid', 'Acid World', 1, 1, 100, 1, 500, 500, 0)
        self.assertEqual(self.saf.approve(p), False)

    def test_match_rev(self):
        """
        Tests matching on a planet, with greater-than matches.
        """
        p = Planet(1, 'Acid', 'Acid World', 4, 4, 100, 1, 100, 100, 0)
        self.assertEqual(self.saf_r.approve(p), True)

    def test_no_match_rev_tectonics(self):
        """
        Tests matching on a planet, with greater-than matches, which fails
        due to tectonics
        """
        p = Planet(1, 'Acid', 'Acid World', 1, 4, 100, 1, 100, 100, 0)
        self.assertEqual(self.saf_r.approve(p), False)

    def test_no_match_rev_weather(self):
        """
        Tests matching on a planet, with greater-than matches, which fails
        due to weather
        """
        p = Planet(1, 'Acid', 'Acid World', 4, 1, 100, 1, 100, 100, 0)
        self.assertEqual(self.saf_r.approve(p), False)

    def test_no_match_rev_temp(self):
        """
        Tests matching on a planet, with greater-than matches, which fails
        due to temp
        """
        p = Planet(1, 'Acid', 'Acid World', 4, 4, 25, 1, 100, 100, 0)
        self.assertEqual(self.saf_r.approve(p), False)

    def test_no_match_rev_bio(self):
        """
        Tests matching on a planet, with greater-than matches, which fails
        due to bio
        """
        p = Planet(1, 'Acid', 'Acid World', 4, 4, 100, 1, 100, 10, 0)
        self.assertEqual(self.saf_r.approve(p), False)
