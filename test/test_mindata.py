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

from uqm_map.data import MinData

class MinDataTests(unittest.TestCase):
    """
    Tests for our `MinData` class.
    """

    def test_init(self):
        """
        Tests our basic initialization routine
        """
        md = MinData(common=1, corrosive=2, base=3, noble=4, rare=5,
            precious=6, radioactive=7, exotic=8)
        self.assertEqual(md.common, 1)
        self.assertEqual(md.corrosive, 2)
        self.assertEqual(md.base, 3)
        self.assertEqual(md.noble, 4)
        self.assertEqual(md.rare, 5)
        self.assertEqual(md.precious, 6)
        self.assertEqual(md.radioactive, 7)
        self.assertEqual(md.exotic, 8)

    def test_value_empty(self):
        """
        Tests the value for empty
        """
        md = MinData()
        self.assertEqual(md.value(), 0)

    def test_value_common(self):
        """
        Tests the value for common
        """
        md = MinData(common=3)
        self.assertEqual(md.value(), 3)

    def test_value_corrosive(self):
        """
        Tests the value for corrosive
        """
        md = MinData(corrosive=3)
        self.assertEqual(md.value(), 6)

    def test_value_base(self):
        """
        Tests the value for base
        """
        md = MinData(base=3)
        self.assertEqual(md.value(), 9)

    def test_value_noble(self):
        """
        Tests the value for noble
        """
        md = MinData(noble=3)
        self.assertEqual(md.value(), 12)

    def test_value_rare(self):
        """
        Tests the value for rare
        """
        md = MinData(rare=3)
        self.assertEqual(md.value(), 15)

    def test_value_precious(self):
        """
        Tests the value for precious
        """
        md = MinData(precious=3)
        self.assertEqual(md.value(), 18)

    def test_value_radioactive(self):
        """
        Tests the value for radioactive
        """
        md = MinData(radioactive=3)
        self.assertEqual(md.value(), 24)

    def test_value_exotic(self):
        """
        Tests the value for exotic
        """
        md = MinData(exotic=3)
        self.assertEqual(md.value(), 75)
    
    def test_value_combined(self):
        """
        Tests combined value
        """
        md = MinData(common=1, corrosive=2, base=3, noble=4, rare=5,
            precious=6, radioactive=7, exotic=8)
        self.assertEqual(md.value(), 347)

    def test_weight_empty(self):
        """
        Tests the weight for empty
        """
        md = MinData()
        self.assertEqual(md.weight(), 0)

    def test_weight_common(self):
        """
        Tests the weight for common
        """
        md = MinData(common=3)
        self.assertEqual(md.weight(), 3)

    def test_weight_corrosive(self):
        """
        Tests the weight for corrosive
        """
        md = MinData(corrosive=3)
        self.assertEqual(md.weight(), 3)

    def test_weight_base(self):
        """
        Tests the weight for base
        """
        md = MinData(base=3)
        self.assertEqual(md.weight(), 3)

    def test_weight_noble(self):
        """
        Tests the weight for noble
        """
        md = MinData(noble=3)
        self.assertEqual(md.weight(), 3)

    def test_weight_rare(self):
        """
        Tests the weight for rare
        """
        md = MinData(rare=3)
        self.assertEqual(md.weight(), 3)

    def test_weight_precious(self):
        """
        Tests the weight for precious
        """
        md = MinData(precious=3)
        self.assertEqual(md.weight(), 3)

    def test_weight_radioactive(self):
        """
        Tests the weight for radioactive
        """
        md = MinData(radioactive=3)
        self.assertEqual(md.weight(), 3)

    def test_weight_exotic(self):
        """
        Tests the weight for exotic
        """
        md = MinData(exotic=3)
        self.assertEqual(md.weight(), 3)
    
    def test_weight_combined(self):
        """
        Tests combined weight
        """
        md = MinData(common=1, corrosive=2, base=3, noble=4, rare=5,
            precious=6, radioactive=7, exotic=8)
        self.assertEqual(md.weight(), 36)

    def test_worth_empty(self):
        """
        Tests the worth for empty
        """
        md = MinData()
        self.assertAlmostEqual(md.worth(), 0.0)

    def test_worth_common(self):
        """
        Tests the worth for common
        """
        md = MinData(common=3)
        self.assertAlmostEqual(md.worth(), 1.0)

    def test_worth_corrosive(self):
        """
        Tests the worth for corrosive
        """
        md = MinData(corrosive=3)
        self.assertAlmostEqual(md.worth(), 2.0)

    def test_worth_base(self):
        """
        Tests the worth for base
        """
        md = MinData(base=3)
        self.assertAlmostEqual(md.worth(), 3.0)

    def test_worth_noble(self):
        """
        Tests the worth for noble
        """
        md = MinData(noble=3)
        self.assertAlmostEqual(md.worth(), 4.0)

    def test_worth_rare(self):
        """
        Tests the worth for rare
        """
        md = MinData(rare=3)
        self.assertAlmostEqual(md.worth(), 5.0)

    def test_worth_precious(self):
        """
        Tests the worth for precious
        """
        md = MinData(precious=3)
        self.assertAlmostEqual(md.worth(), 6.0)

    def test_worth_radioactive(self):
        """
        Tests the worth for radioactive
        """
        md = MinData(radioactive=3)
        self.assertAlmostEqual(md.worth(), 8.0)

    def test_worth_exotic(self):
        """
        Tests the worth for exotic
        """
        md = MinData(exotic=3)
        self.assertAlmostEqual(md.worth(), 25.0)
    
    def test_worth_combined(self):
        """
        Tests combined worth
        """
        md = MinData(common=1, corrosive=2, base=3, noble=4, rare=5,
            precious=6, radioactive=7, exotic=8)
        self.assertAlmostEqual(md.worth(), 9.639, 3)

    def test_add_common(self):
        """
        Tests adding common
        """
        md = MinData()
        md2 = MinData(common=1)
        md.add(md2)
        self.assertEqual(md.common, 1)

    def test_add_corrosive(self):
        """
        Tests adding corrosive
        """
        md = MinData()
        md2 = MinData(corrosive=1)
        md.add(md2)
        self.assertEqual(md.corrosive, 1)

    def test_add_base(self):
        """
        Tests adding base
        """
        md = MinData()
        md2 = MinData(base=1)
        md.add(md2)
        self.assertEqual(md.base, 1)

    def test_add_noble(self):
        """
        Tests adding noble
        """
        md = MinData()
        md2 = MinData(noble=1)
        md.add(md2)
        self.assertEqual(md.noble, 1)

    def test_add_rare(self):
        """
        Tests adding rare
        """
        md = MinData()
        md2 = MinData(rare=1)
        md.add(md2)
        self.assertEqual(md.rare, 1)

    def test_add_precious(self):
        """
        Tests adding precious
        """
        md = MinData()
        md2 = MinData(precious=1)
        md.add(md2)
        self.assertEqual(md.precious, 1)

    def test_add_radioactive(self):
        """
        Tests adding radioactive
        """
        md = MinData()
        md2 = MinData(radioactive=1)
        md.add(md2)
        self.assertEqual(md.radioactive, 1)

    def test_add_exotic(self):
        """
        Tests adding exotic
        """
        md = MinData()
        md2 = MinData(exotic=1)
        md.add(md2)
        self.assertEqual(md.exotic, 1)

    def test_add_all(self):
        """
        Tests adding all values
        """
        md = MinData(common=1, corrosive=2, base=3, noble=4, rare=5,
            precious=6, radioactive=7, exotic=8)
        md2 = MinData(common=8, corrosive=7, base=6, noble=5, rare=4,
            precious=3, radioactive=2, exotic=1)
        md.add(md2)
        self.assertEqual(md.common, 9)
        self.assertEqual(md.corrosive, 9)
        self.assertEqual(md.base, 9)
        self.assertEqual(md.noble, 9)
        self.assertEqual(md.rare, 9)
        self.assertEqual(md.precious, 9)
        self.assertEqual(md.radioactive, 9)
        self.assertEqual(md.exotic, 9)
