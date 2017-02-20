#!/usr/bin/env python
##************************************************************************##
#            supernova_updates_parser.py  -  K Desktop Planetarium         #
#                             -------------------                          #
#    begin                : 2011/18/06                                     #
#    copyright            : (C) 2011 by Samikshan Bairagya                 #
#    email                : samikshan@gmail.com                            #
##************************************************************************##

##************************************************************************##
#                                                                          #
#   This program is free software; you can redistribute it and/or modify   #
#   it under the terms of the GNU General Public License as published by   #
#   the Free Software Foundation; either version 2 of the License, or      #
#   (at your option) any later version.                                    #
#                                                                          #
##************************************************************************##
"""
### Supernova Updates Parser.
# This program reads data from
# http://www.cbat.eps.harvard.edu/lists/RecentSupernovae.html
### This page gives details on supernovae that have occurred since the start of 2010.
"""

# import re
import urllib.request
# from pathlib import Path
# import csv
import os
# import json
import yaml

SOCK = urllib.request.urlopen("http://cdsarc.u-strasbg.fr/ftp/cats/VI/81/VSOP87D.ear")
# SOCK = urllib.request.urlopen("http://www.cbat.eps.harvard.edu/lists/RecentSupernovae.html")
PAGE_LINES = []
PAGE_LINES += SOCK.readlines()
print(type(PAGE_LINES))

PATH = os.path.abspath('.')
print(PATH)
with open('vsop87d.ear.yaml', 'w') as file:
    for idx in enumerate(PAGE_LINES):
        print(idx)
        yaml.dump(idx, file)
    file.close()

# output = open(KStandardDirs().locateLocal('data','kstars/supernovae.dat'),'w')

SOCK.close()
print("List Update Finished")

with open('vsop87d.ear.yaml', 'r') as file:
    LINE = file.readline()
    print(LINE)
    file.close()
