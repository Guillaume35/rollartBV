# Rollart unchained
# Copyright (C) 2021  Skaters Team community

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Contributors :
# Guillaume MODARD <guillaumemodard@gmail.com>

import sqlite3
from pathlib import Path

# dict_factory()
# convert data to dict
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# getDb()
# get database connection
def getDb():
    home_path = str(Path.home())
    db_path = home_path + '/.rollartBV/structure.db'
    conn = sqlite3.connect(db_path)

    return conn

# floatVal()
# convert value to float even for None value
def floatVal(value):
    if not value:
        value = 0.0
    return float(value)

# compulsoryPatterns()
# get all compulsory patterns
def compulsoryPatterns():
    patterns = {
        'Quickstep': (2, 'QSS$L&'), 
        'Starlight': (2, 'SW$L&'), 
        'Harris Tango Solo': (2, 'HT$L&'), 
        'Harris Tango Couples': (2, 'HTCD$L&'), 
        'Tango Delanco': (2, 'TD$L&'), 
        'Midnight Blues': (2, 'MB$M&'), 
        'Fourteen Step': (1, 'FTSt&'), 
        'Rocker Foxtrot': (1, 'RFox&'), 
        'Blues Pattern': (2, 'B$L&'), 
        'Terenzi Pattern': (2, 'TW$L&'), 
        'Westminster Waltz': (1, 'WW&'), 
        'Viennese Waltz': (1, 'VWz&'), 
        'Paso Doble Pattern': (1, 'PD&'), 
        'Argentine Tango Solo': (2, 'ATS$L&'), 
        'Argentine Tango': (2, 'AT$L&'), 
        'Italian Foxtrot': (2, 'IF$L&'), 
        'Castel March': (2, 'CM$L&'), 
        'City Blues': (1, 'CBSt&'), 
        'Carlos Tango': (1, 'CTSt&'), 
        'Skaters March': (1, 'SML&'), 
        'La Vista Cha Cha': (1, 'LCSt&'), 
        'Canasta Tango': (1, 'CGSt&'), 
        'Denver Shuffle': (1, 'DSSt&'), 
        'Tudor Waltz': (1, 'TWSt&'), 
        'Easy Paso': (1, 'EPSt&'), 
        'Association Waltz': (2, 'AW$ST&'), 
        'Killian': (2, 'KI$St&'), 
        'Shaken Samba': (2, 'SS$L&'), 
        'Tango Delancha': (2, 'TH$L&'), 
        'Tango Iceland': (2, 'TI$L&'), 
        'Loran Rumba': (2, 'LR$L&'), 
        'Golden Samba': (2, 'GS$L&'), 
        'Roller Samba Couples': (2, 'RSC$L&'), 
        'Roller Samba Solo': (2, 'RS$L&'), 
        'Cha Cha Patin': (2, 'CC$L&'), 
        'Little Waltz Couples': (2, 'LWC$L&'), 
        'Little Waltz Solo': (2, 'LW$L&'), 
        'Flirtation Waltz Solo': (2, 'FWS$L&'), 
        'Federation Foxtrot Solo': (2, 'FFS$L&'), 
        'Kent Tango Solo': (2, 'KTS$L&'), 
        'Siesta Tango SandC': (2, 'ST$L&'), 
        'Swing Foxtrot Couple': (2, 'SFC$L&')
    }

    return patterns