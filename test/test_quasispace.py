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

from uqm_map.data import Quasispace, System

class QuasispaceTests(unittest.TestCase):
    """
    Tests for our `Quasispace` class.  This essentially just pretends to be
    a System for the purposes of filtering, but is really just holding a couple
    of extra quasispace coordinates.  Doesn't have any mineral data or anything
    like that.
    """

    def setUp(self):
        """
        Some vars we might need on (nearly) every test
        """
        self.q = Quasispace(5000, 5000, 4000, 4000, 'Q')

    def test_init(self):
        """
        Tests our basic initialization routine
        """
        self.assertEqual(self.q.fullname, 'Quasispace Exit Q')
        self.assertEqual(self.q.x, 5000)
        self.assertEqual(self.q.y, 5000)
        self.assertEqual(self.q.qs_x, 4000)
        self.assertEqual(self.q.qs_y, 4000)
        self.assertEqual(self.q.is_quasispace, True)

    def test_distance_to_self(self):
        """
        Tests computing the distance to ourself
        """
        self.assertAlmostEqual(self.q.distance_to(self.q), 0)

    def test_distance_close(self):
        """
        Tests computing the distance to another system close by
        """
        s2 = System(2, 'System', 'Beta', 5500, 5000, 'blue dwarf', '')
        self.assertAlmostEqual(self.q.distance_to(s2), 50)

    def test_distance_diagonal(self):
        """
        Tests computing the distance to another system at a diagonal
        """
        s2 = System(2, 'System', 'Beta', 3000, 7000, 'blue dwarf', '')
        self.assertAlmostEqual(self.q.distance_to(s2), 282.84, 2)
