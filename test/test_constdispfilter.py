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

from uqm_map.data import ConstDispFilter, System

class ConstDispFilterTests(unittest.TestCase):
    """
    Tests for our `ConstDispFilter` class.  This is similar to NameDispFilter
    but only matches on exact matches for the constellation name, and is
    case sensitive, and will never match on extra text
    """

    def test_init(self):
        """
        Tests our basic initialization routine
        """
        cdf = ConstDispFilter('Name')
        self.assertEqual(cdf.name, 'Name')

    def test_match(self):
        """
        Tests matching a full system name
        """
        system = System(1, 'System Name', 'Alpha', 5000, 5000, 'blue dwarf', '')
        cdf = ConstDispFilter('System Name')
        self.assertEqual(cdf.approve(system), True)

    def test_no_match(self):
        """
        Tests matching a full system name where it doesn't work
        """
        system = System(1, 'System Name', 'Alpha', 5000, 5000, 'blue dwarf', '')
        cdf = ConstDispFilter('Alpha System Name')
        self.assertEqual(cdf.approve(system), False)

    def test_case_mismatch(self):
        """
        Tests a case mismatch
        """
        system = System(1, 'Constellation', 'Alpha', 5000, 5000, 'blue dwarf', '')
        cdf = ConstDispFilter('constellation')
        self.assertEqual(cdf.approve(system), False)

    def test_no_match_extra(self):
        """
        Tests matching a full system name where it doesn't work, even though
        the extra text might do the trick
        """
        system = System(1, 'System Name', 'Alpha', 5000, 5000, 'blue dwarf', 'Alpha System Name')
        cdf = ConstDispFilter('Alpha System Name')
        self.assertEqual(cdf.approve(system), False)
