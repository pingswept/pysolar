#!/usr/bin/python
 
# Script for detecting angle to solar obstructions from
# spherically distorted images
 
# Copyright 2009 Brandon Stafford
#
# This file is part of Pysolar.
#
# Pysolar is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Pysolar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with Pysolar. If not, see <http://www.gnu.org/licenses/>.

from PIL import Image
from math import *
import numpy as np

def squareImage(im):
    (width, height) = im.size
    box = ((width - height)/2, 0, (width + height)/2, height)
    return im.crop(box)

def despherifyImage(im):
    (width, height) = im.size
    half_width = im.size[0]/2
    half_height = im.size[1]/2

    inpix = im.load()
    out = Image.new("L", (width, half_height))
    outpix = out.load()

    full_circle = 1000.0 * 2 * pi

    for r in range(half_width):
        for theta in range(int(full_circle)):
            (inx, iny) = (round(r * cos(theta/1000.0)) + half_width, round(r * sin(theta/1000.0)) + half_width)
            (outx, outy) = (width - width * (theta/full_circle) - 1, r)
            outpix[outx, outy] = inpix[inx, iny]
    return out

def differentiateImageColumns(im):
    (width, height) = im.size
    pix = im.load()

    for x in range(width):
        for y in range(height - 1):
            pix[x, y] = min(10 * abs(pix[x, y] - pix[x, y + 1]), 255)

    return im

def redlineImage(im):
    (width, height) = im.size
    pix = im.load()

    threshold = 300

    for x in range(width):
        for y in range(height - 1):
            (R, G, B) = pix[x, y]
            if R + G + B > threshold:
                pix[x, y] = (255, 0, 0)
                break
    return im

im = Image.open('spherical.jpg').convert("L")
im = squareImage(im)

lin = despherifyImage(im)
d = differentiateImageColumns(lin).convert("RGB")
r = redlineImage(d)

r.show()

