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

from uqm_map.data import ProxDispFilter, System, Quasispace

class ProxDispFilterTests(unittest.TestCase):
    """
    Tests for our `ProxDispFilter` class.  This filters systems/quasispace
    by distance from a given other system/quasispace.
    """

    def setUp(self):
        """
        Some objects which we're likely to want in various tests
        """
        self.system_center = System(1, 'Center', 'Alpha', 5000, 5000, 'white dwarf', '')
        self.pdf = ProxDispFilter(self.system_center, 100)
        self.quasi_center = Quasispace(5000, 5000, 5000, 5000, 'X')
        self.qpdf = ProxDispFilter(self.quasi_center, 100)

    def test_init(self):
        """
        Tests our basic initialization routine
        """
        self.assertEqual(self.pdf.from_system, self.system_center)
        self.assertEqual(self.pdf.radius, 100)

    def test_match_self(self):
        """
        Test matching ourselves
        """
        pdf = ProxDispFilter(self.system_center, 0)
        self.assertEqual(pdf.approve(self.system_center), True)

    def test_match_close(self):
        """
        Test matching a close system
        """
        system_close = System(2, 'Close', 'Alpha', 5100, 5100, 'red dwarf', '')
        self.assertEqual(self.pdf.approve(system_close), True)

    def test_not_match_far(self):
        """
        Test not matching a far system
        """
        system_far = System(3, 'Far', 'Alpha', 9000, 9000, 'blue dwarf', '')
        self.assertEqual(self.pdf.approve(system_far), False)

    def test_match_quasispace(self):
        """
        Test matching a quasispace system
        """
        quasi_close = Quasispace(4900, 4900, 3000, 3000, 'C')
        self.assertEqual(self.pdf.approve(quasi_close), True)

    def test_not_match_quasispace(self):
        """
        Test not matching a far quasispace
        """
        quasi_far = Quasispace(1000, 1000, 4000, 4000, 'F')
        self.assertEqual(self.pdf.approve(quasi_far), False)

    def test_quasi_match_close(self):
        """
        Test matching a close system, with quasispace origin
        """
        system_close = System(2, 'Close', 'Alpha', 5100, 5100, 'red dwarf', '')
        self.assertEqual(self.qpdf.approve(system_close), True)

    def test_quasi_not_match_far(self):
        """
        Test not matching a far system, with quasispace origin
        """
        system_far = System(3, 'Far', 'Alpha', 9000, 9000, 'blue dwarf', '')
        self.assertEqual(self.qpdf.approve(system_far), False)

    def test_quasi_match_quasispace(self):
        """
        Test matching a quasispace system, with quasispace origin
        """
        quasi_close = Quasispace(4900, 4900, 3000, 3000, 'C')
        self.assertEqual(self.qpdf.approve(quasi_close), True)

    def test_quasi_not_match_quasispace(self):
        """
        Test not matching a far quasispace, with quasispace origin
        """
        quasi_far = Quasispace(1000, 1000, 4000, 4000, 'F')
        self.assertEqual(self.qpdf.approve(quasi_far), False)
