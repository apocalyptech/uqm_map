#!/usr/bin/env python
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

# There's two modules for abstracting XDG, both of which use the base module
# name "xdg".  Obviously inside a virtualenv or whatever it's easy enough to
# make sure there's just a specific one installed, but I'd like to be flexible
# in case someone's just using this with their distro-provided packages.

# This is all pretty improper, but whatever.

try:
    # First try https://pypi.python.org/pypi/pyxdg
    import xdg.BaseDirectory
    base_config_dir = xdg.BaseDirectory.save_config_path('uqm_map')
except (ModuleNotFoundError, ImportError):
    # Now try https://pypi.python.org/pypi/xdg
    import xdg
    base_config_dir = os.path.join(xdg.XDG_CONFIG_HOME, 'uqm_map')

# Ensure our config dir exists.  If using pyxdg, this should actually be
# unnecessary since `save_config_path` would create it.
if not os.path.exists(base_config_dir):
    os.mkdir(base_config_dir)

