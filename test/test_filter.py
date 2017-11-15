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

from uqm_map.data import Filter, ProxDispFilter, NameDispFilter, System

class FilterTests(unittest.TestCase):
    """
    Tests for our `Filter` class.  This is the container which aggregates
    a bunch of filters into one object which can then be used to do filter
    on a number of things at once.
    """

    def setUp(self):
        """
        Vars we can use in most of our tests
        """
        self.f = Filter()

    def test_init(self):
        """
        Tests our basic initialization routine
        """
        self.assertEqual(self.f.filtering(), False)

    def test_add_filter(self):
        """
        Tests adding a new filter to the chain
        """
        self.f.add(NameDispFilter('Hello', False))
        self.assertEqual(self.f.filtering(), True)

    def test_add_two_filters(self):
        """
        Tests adding two new filters to the chain
        """
        s = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        self.f.add(NameDispFilter('Hello', False))
        self.f.add(ProxDispFilter(s, 500))
        self.assertEqual(self.f.filtering(), True)

    def test_reset(self):
        """
        Tests resetting the filter
        """
        s = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        self.f.add(NameDispFilter('Hello', False))
        self.f.add(ProxDispFilter(s, 500))
        self.assertEqual(self.f.filtering(), True)
        self.f.reset()
        self.assertEqual(self.f.filtering(), False)

    def test_approve_empty(self):
        """
        If we have no filters added, any system should be allowed.
        """
        s = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        self.assertEqual(self.f.approve(s), True)

    def test_approve_single_match(self):
        """
        Tests approving a system with a single filter which matches
        """
        s = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        self.f.add(NameDispFilter('alpha system', False))
        self.assertEqual(self.f.approve(s), True)

    def test_approve_two_matches(self):
        """
        Tests approving a system with two filters which both match
        """
        s = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        s2 = System(2, 'System', 'Beta', 5100, 5100, 'red dwarf', '')
        self.f.add(NameDispFilter('alpha system', False))
        self.f.add(ProxDispFilter(s2, 500))
        self.assertEqual(self.f.approve(s), True)

    def test_approve_two_matches_first_fails(self):
        """
        Tests approving a system with two filters in which the first one
        fails.
        """
        s = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        s2 = System(2, 'System', 'Beta', 5100, 5100, 'red dwarf', '')
        self.f.add(NameDispFilter('ur-quan', False))
        self.f.add(ProxDispFilter(s2, 500))
        self.assertEqual(self.f.approve(s), False)

    def test_approve_two_matches_second_fails(self):
        """
        Tests approving a system with two filters in which the second one
        fails.
        """
        s = System(1, 'System', 'Alpha', 5000, 5000, 'blue dwarf', '')
        s2 = System(2, 'System', 'Beta', 9000, 9000, 'red dwarf', '')
        self.f.add(NameDispFilter('alpha system', False))
        self.f.add(ProxDispFilter(s2, 50))
        self.assertEqual(self.f.approve(s), False)
