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

from uqm_map.data import NameDispFilter, System, Quasispace

class NameDispFilterTests(unittest.TestCase):
    """
    Tests for our `NameDispFilter` class.  This filters systems based on the
    name of systems, and optionally the extra text.
    """

    def test_init(self):
        """
        Tests our basic initialization routine
        """
        ndf = NameDispFilter('Name', True)
        self.assertEqual(ndf.name, 'name')
        self.assertEqual(ndf.specialchecked, True)

    def test_match_full(self):
        """
        Tests matching a full system name
        """
        system = System(1, 'System Name', 'Alpha', 5000, 5000, 'blue dwarf', '')
        ndf = NameDispFilter('System Name', False)
        self.assertEqual(ndf.approve(system), True)

    def test_match_substring(self):
        """
        Tests matching a substring of a system name
        """
        system = System(1, 'System Name', 'Alpha', 5000, 5000, 'blue dwarf', '')
        ndf = NameDispFilter('Stem', False)
        self.assertEqual(ndf.approve(system), True)

    def test_no_match(self):
        """
        Attempting to match a system which fails
        """
        system = System(1, 'Zoq-Fot-Pik', 'Alpha', 5000, 5000, 'blue dwarf', '')
        ndf = NameDispFilter('Ur-Quan', False)
        self.assertEqual(ndf.approve(system), False)

    def test_match_extra(self):
        """
        Tests matching based on extra text
        """
        system = System(1, 'System Name', 'Alpha', 5000, 5000, 'blue dwarf', 'Zoq-Fot-Pik Homeworld')
        ndf = NameDispFilter('zoq', True)
        self.assertEqual(ndf.approve(system), True)

    def test_match_extra_without_flag(self):
        """
        Tests matching based on extra text, but without the extra text being a valid
        source
        """
        system = System(1, 'System Name', 'Alpha', 5000, 5000, 'blue dwarf', 'Zoq-Fot-Pik Homeworld')
        ndf = NameDispFilter('zoq', False)
        self.assertEqual(ndf.approve(system), False)

    def test_match_full_prefix(self):
        """
        Tests matching a full system name, with the location prefix
        """
        system = System(1, 'System Name', 'Alpha', 5000, 5000, 'blue dwarf', '')
        ndf = NameDispFilter('Alpha System Name', False)
        self.assertEqual(ndf.approve(system), True)

    def test_match_full_wrong_prefix(self):
        """
        Tests matching a full system name, with the location prefix but a wrong one.
        """
        system = System(1, 'System Name', 'Beta', 5000, 5000, 'blue dwarf', '')
        ndf = NameDispFilter('Alpha System Name', False)
        self.assertEqual(ndf.approve(system), False)

    def test_match_uc_lc(self):
        """
        Tests matching an uppercase system name with lowercase search
        """
        system = System(1, 'SYSTEM', 'Alpha', 5000, 5000, 'blue dwarf', '')
        ndf = NameDispFilter('system', False)
        self.assertEqual(ndf.approve(system), True)

    def test_match_lc_uc(self):
        """
        Tests matching a lowercase system name with uppercase search
        """
        system = System(1, 'system', 'Alpha', 5000, 5000, 'blue dwarf', '')
        ndf = NameDispFilter('SYSTEM', False)
        self.assertEqual(ndf.approve(system), True)

    def test_match_extra_uc_lc(self):
        """
        Tests matching extra text with uppercase extra and lowercase search
        """
        system = System(1, 'System Name', 'Alpha', 5000, 5000, 'blue dwarf', 'EXTRA')
        ndf = NameDispFilter('extra', True)
        self.assertEqual(ndf.approve(system), True)

    def test_match_extra_lc_uc(self):
        """
        Tests matching extra text with lowercase extra and uppercase search
        """
        system = System(1, 'System Name', 'Alpha', 5000, 5000, 'blue dwarf', 'extra')
        ndf = NameDispFilter('EXTRA', True)
        self.assertEqual(ndf.approve(system), True)

    def test_match_quasispace(self):
        """
        Test matching a quasispace portal
        """
        q = Quasispace(5000, 5000, 5000, 5000, 'C')
        ndf = NameDispFilter('Quasispace Exit C', False)
        self.assertEqual(ndf.approve(q), True)

    def test_no_match_quasispace(self):
        """
        Test not matching a quasispace portal
        """
        q = Quasispace(5000, 5000, 5000, 5000, 'C')
        ndf = NameDispFilter('Quasispace Exit F', False)
        self.assertEqual(ndf.approve(q), False)

    def test_no_match_quasispace_extra(self):
        """
        Test not matching a quasispace portal, when the filter is allowed
        to search for extra text
        """
        q = Quasispace(5000, 5000, 5000, 5000, 'C')
        ndf = NameDispFilter('Quasispace Exit F', True)
        self.assertEqual(ndf.approve(q), False)
