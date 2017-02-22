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

import re
import urllib.request
from pathlib import Path
import csv

import os
# import difflib
# from PyKDE4.kdecore import KStandardDirs

def parse(line):
    """
    parse line
    """
    # parsed = to_csv(re.sub('<.*?>', '', line))
    parsed = to_csv(line)
    return parsed

## fixme:
# The extracted data is converted to CSV by inserting commas
# after definite number of characters. There might be a better
# way to do this.
def to_csv(line):
    """
    csv
    """
    comma_interval = [7, 24, 36, 44, 51, 63, 68, 86, 110, 129, 133, 143]
    for index in range(0, len(line)-1):
        if index in comma_interval:
            # edited = line[:index] + "," + line[index + 1:]
            edited = line[:index] + line[index + 1:]
            line = edited
    return line

SOCK = urllib.request.urlopen("http://cdsarc.u-strasbg.fr/ftp/cats/VI/81/VSOP87D.ear")
# SOCK = urllib.request.urlopen("http://www.cbat.eps.harvard.edu/lists/RecentSupernovae.html")
PAGE_LINES = SOCK.readlines()
SOCK.close()
PATH = os.path.abspath('.')
print(PATH)
# output = open(KStandardDirs().locateLocal('data','kstars/supernovae.dat'),'w')
with open('supernovae.dat', 'w') as file:
    WRITER = csv.writer(file)

    def itr_object():
        found = False
        first_line = True
        for itr in PAGE_LINES:
            if found:
                # pre = re.compile(str("</pre>"))
                # match = pre.search(itr)
                # if match:
                    # found = False
                break
            if first_line:
                parsed_line = "#" + str(parse(itr))
                first_line = False
            else:
                parsed_line = str(parse(itr))
                # output.write(parsed_line)

            # pre = re.compile("<pre>")
            # match = str(pre.search(itr))
            # if match:
                # print("found!!" + itr)
            first_line = True
            found = True
    WRITER.writerows(PAGE_LINES)

# output.close()
print("Supernovae List Update Finished")
