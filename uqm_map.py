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

import os
import sys
import argparse
from uqm_map.gui import Application

# TODO: Figure out a reasonable way to do this so it works both as a
# checked-out git project and something that's been installed properly
# on the system
datafile_default = os.path.join(
        os.path.dirname(__file__),
        'data',
        'uqm.json.gz')

# Argument Definitions
parser = argparse.ArgumentParser(description='UQM/SC2 Starmap Viewer',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-d', '--datafile',
        type=str,
        default=datafile_default,
        help='Datafile to load for starmap')

# Parse arguments
args = parser.parse_args()

# Run the GUI
gui = Application(args.datafile)
sys.exit(gui.exec_())
