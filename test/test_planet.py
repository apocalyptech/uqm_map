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

from uqm_map.data import Planet, MinData

class PlanetTests(unittest.TestCase):
    """
    Tests for our `Planet` class.  Very little to do in here.
    """

    def test_init(self):
        """
        Tests our basic initialization routine
        """
        p = Planet(idnum=1,
            name='Planet',
            ptype='Type',
            tectonics=4,
            weather=6,
            temp=200,
            gravity=2,
            bio=100,
            bio_danger=50,
            mineral=MinData())
        self.assertEqual(p.idnum, 1)
        self.assertEqual(p.name, 'Planet')
        self.assertEqual(p.ptype, 'Type')
        self.assertEqual(p.tectonics, 4)
        self.assertEqual(p.weather, 6)
        self.assertEqual(p.temp, 200)
        self.assertEqual(p.gravity, 2)
        self.assertEqual(p.bio, 100)
        self.assertEqual(p.bio_danger, 50)
        self.assertNotEqual(p.mineral, None)
