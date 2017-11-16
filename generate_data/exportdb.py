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

# Figure out where our base `data` path is
base_dir = os.path.dirname(__file__)
constellation_file = os.path.join(base_dir, 'constellations.ini')
data_dir = os.path.join(base_dir, '..', 'data')
json_file = os.path.join(data_dir, 'uqm.json.gz')

# Bit of a notice to anyone running this
print("""
NOTE: This little utility is only useful if you happen to have the
UQM system/planet data stored in a MySQL database and want to use that
to regenerate {json_file}

Unless you're me, this is pretty unlikely to be the case.

Hit <ENTER> to continue, or Ctrl-C to abort.""".format(json_file=json_file))
sys.stdin.readline()

# Munge the system path.  This is lame, but whatever.
sys.path.append(os.path.join(base_dir, '..'))

# Continue with imports
import json
import gzip
import MySQLdb
import configparser
from uqm_map import xdg

# This tiny app doesn't really do anyone any good except for me.  I had
# pulled the map data from UQM into a MySQL database and stored it there
# for awhile - originally the starmap viewer was actually going to do
# all of its filtering and stuff via SQL, though when I started the project
# I never did more than the basic SELECTs you see below, and then did
# all the work via the classes, like the app still does.  Then when I
# thought about the fact that I may want to distribute this somehow, having
# a MySQL dependency was just ludicrous.  So, I ripped out what little
# there was of the DB connectivity and slapped it in here, exporting the
# data to a Pickle object instead, which is how the main app reads it.
#
# ... I know you TOTALLY care about all that.  Anyway, it's here for
# posterity, in case anyone was wondering how the initial pickle had been
# generated.

# Make sure we have a dbinfo.ini file
db_file = os.path.join(xdg.base_config_dir, 'dbinfo.ini')
if not os.path.exists(db_file):
    print('')
    print('A database configuration file must exist at:')
    print("\t{}".format(db_file))
    print('')
    print('The file\'s contents should be formatted like so:')
    print('')
    print('[db]')
    print('host = hostname')
    print('user = dbusername')
    print('pass = dbpassword')
    print('db = dbname')
    print('')
    sys.exit(1)

# Make sure we have a constellations.ini
if not os.path.exists(constellation_file):
    print('{} not found!'.format(constellation_file))
    sys.exit(1)

# Now read in our database info
cp = configparser.ConfigParser()
cp.read(db_file)
db_host = cp.get('db', 'host')
db_user = cp.get('db', 'user')
db_pass = cp.get('db', 'pass')
db_name = cp.get('db', 'db')

# ... and connect to the DB
print('Connecting to database {}@{} as "{}"'.format(db_name, db_host, db_user))
dbconn = MySQLdb.connect(host = db_host,
        user = db_user,
        passwd = db_pass,
        db = db_name)
dbcurs = dbconn.cursor(MySQLdb.cursors.DictCursor)

data = {}

print('Reading system information')
dbcurs.execute('select * from system')
data['systems'] = dbcurs.fetchall()

print('Reading planet information')
dbcurs.execute('select * from planet')
data['planets'] = dbcurs.fetchall()

dbcurs.close()
dbconn.close()

# Hardcode quasispace points
data['quasispace'] = (
        { 'label': 'A', 'x': 438, 'y': 6373, 'qs_x': 500, 'qs_y': 500 },
        { 'label': 'B', 'x': 111, 'y': 9409, 'qs_x': 520, 'qs_y': 514 },
        { 'label': 'C', 'x': 5849, 'y': 6213, 'qs_x': 520, 'qs_y': 540 },
        { 'label': 'D', 'x': 7752, 'y': 8906, 'qs_x': 530, 'qs_y': 528 },
        { 'label': 'E', 'x': 368, 'y': 6332, 'qs_x': 544, 'qs_y': 532 },
        { 'label': 'F', 'x': 3183, 'y': 4906, 'qs_x': 502, 'qs_y': 460 },
        { 'label': 'G', 'x': 1909, 'y': 926, 'qs_x': 506, 'qs_y': 474 },
        { 'label': 'H', 'x': 5673, 'y': 1207, 'qs_x': 516, 'qs_y': 466 },
        { 'label': 'I', 'x': 4090, 'y': 7748, 'qs_x': 476, 'qs_y': 458 },
        { 'label': 'J', 'x': 9210, 'y': 6104, 'qs_x': 468, 'qs_y': 464 },
        { 'label': 'K', 'x': 6116, 'y': 4131, 'qs_x': 476, 'qs_y': 496 },
        { 'label': 'L', 'x': 2302, 'y': 3988, 'qs_x': 466, 'qs_y': 514 },
        { 'label': 'M', 'x': 5657, 'y': 9712, 'qs_x': 448, 'qs_y': 504 },
        { 'label': 'N', 'x': 8607, 'y': 151, 'qs_x': 458, 'qs_y': 492 },
        { 'label': 'O', 'x': 50, 'y': 1647, 'qs_x': 492, 'qs_y': 492 },
        { 'label': 'P', 'x': 9735, 'y': 3153, 'qs_x': 488, 'qs_y': 538 }
    )

# Now let's import our constellation data; note that we're going
# to do some associations here...  We do it here so that the main
# app doesn't have to, and because our IDs may change at some point
# in the future.
print('Processing constellation information')
ids = {}
data['constellations'] = {}
for system in data['systems']:
    if (system['position'] and system['position'] != ''):
        sysname = system['name'].lower()
        syspos = system['position'].lower()
        if not sysname in ids:
            ids[sysname] = {}
        ids[sysname][syspos] = system['sid']
cp = configparser.ConfigParser()
cp.read(constellation_file)
for const in cp.sections():
    for (star, links) in cp.items(const):
        const = const.lower()
        star = star.lower()
        if (const in ids and star in ids[const]):
            data['constellations'][ids[const][star]] = []
            for link in links.split(','):
                link = link.lower()
                if (const in ids and link in ids[const]):
                    data['constellations'][ids[const][star]].append(ids[const][link])
                else:
                    print('No ID for link {} {}!'.format(link, const))
        else:
            print('No ID for starting point {} {}!'.format(star, const))

# Save to a JSON datastore
print('Saving to {}'.format(json_file))
with gzip.GzipFile(json_file, 'w') as df:
    df.write(json.dumps(data).encode('utf-8'))
print('...done!')
