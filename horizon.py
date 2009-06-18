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
import solar
import datetime as dt
import simulate as sim
import radiation as rad

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

#    for r in range(half_width):
#        for theta in range(int(full_circle)):
#            (inx, iny) = (round(r * cos(theta/1000.0)) + half_width, round(r * sin(theta/1000.0)) + half_width)
#            (outx, outy) = (width - width * (theta/full_circle) - 1, r)
#            outpix[outx, outy] = inpix[inx, iny]

    theta_range = range(int(full_circle))
    t_1000_range = [t / 1000.0 for t in theta_range]
    thetas = zip([cos(t) for t in t_1000_range],
    [sin(t) for t in t_1000_range],
    [t / full_circle for t in theta_range])

    for r in range(half_width):
        for t_cos, t_sin, t_full_circle in thetas:
            (inx, iny) = (round(r * t_cos) + half_width,
            round(r * t_sin) + half_width)
            outx = width - width * (t_full_circle) - 1
#            print inpix, outx, r, inx, iny
            outpix[outx, r] = inpix[inx, iny]
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
    horizon = []

    for x in range(width):
        for y in range(height - 1):
            (R, G, B) = pix[x, y]
            if R + G + B > threshold:
                pix[x, y] = (255, 0, 0)
                horizon.append(y)
                break
    return (im, horizon)

def addSunPaths(im, latitude_deg, longitude_deg, horizon, d):
    pix = im.load()

    alt_zero = getAltitudeZero()
    az_zero = getAzimuthZero()

    for m in range(24 * 60):
        alt = solar.GetAltitude(latitude_deg, longitude_deg, d + dt.timedelta(minutes = m))
        az = solar.GetAzimuth(latitude_deg, longitude_deg, d + dt.timedelta(minutes = m))

        x = az_zero + int(az * 1944.0/360.0)
        y = alt_zero - int(alt_zero * sin(radians(alt)))
        if y < horizon[x]:
            pix[x % 1944, y] = (255, 193, 37)
    
    return im

def getAzimuthZero():
    return 1100

def getAltitudeZero():
    return 380

if __name__ == '__main__':
    horizon = []

    im = Image.open('spherical.jpg').convert("L")
    im = squareImage(im)

    print 'Starting despherification . . .'
    lin = despherifyImage(im)

    print 'Despherification complete. Calculating horizon . . .'
    d = differentiateImageColumns(lin).convert("RGB")
    r, horizon = redlineImage(d)
    print 'Horizon calculated.'

    (latitude_deg, longitude_deg) = (42.206, -71.382)
    summer = dt.datetime(2009, 6, 21, 5, 0, 0, 0)
    fall = dt.datetime(2009, 9, 21, 5, 0, 0, 0)
    winter = dt.datetime(2009, 12, 21, 5, 0, 0, 0)
    step_minutes = 5

    power_densities = [radiation for (time, alt, az, radiation, shade) in sim.SimulateSpan(latitude_deg, longitude_deg, horizon, summer, winter, step_minutes)]
    print power_densities

    energy = sum(power_densities) * step_minutes * 60
    print str(energy/1000000) + ' MJ per m^2 per year'

    sp = addSunPaths(r, latitude_deg, longitude_deg, horizon, summer)
    sp2 = addSunPaths(r, latitude_deg, longitude_deg, horizon, fall)
    sp3 = addSunPaths(r, latitude_deg, longitude_deg, horizon, winter)

    sp3.show()

#   sp3.save('sun_path.jpg')
