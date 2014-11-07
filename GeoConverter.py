#!/usr/bin/python

import math

# Krasovsky 1940
#
# a = 6378245.0, 1/f = 298.3
# b = a * (1 - f)
# ee = (a^2 - b^2) / a^2;

a = 6378245.0
ee = 0.00669342162296594323
pi = math.pi
x_pi = math.pi * 3000.0 / 180.0

# Transform Geo from World Geodetic System to Mars Geodetic System in China


def wgs2gcj(args):
    (wgLat, wgLon) = args[0:2]
    if outOfChina(wgLat, wgLon):
        return None

    dLat = transformLat(wgLon - 105.0, wgLat - 35.0)
    dLon = transformLon(wgLon - 105.0, wgLat - 35.0)
    radLat = wgLat / 180.0 * pi

    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    SqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * SqrtMagic) * pi)
    dLon = (dLon * 180.0) / (a / SqrtMagic * math.cos(radLat) * pi)
    return [wgLat + dLat, wgLon + dLon]

# Transform Geo from Mars Geodetic System to World Geodetic System in China


def gcj2wgs(args):
    (a, b) = args[0:2]

    locs = wgs2gcj(args)
    if locs == None:
        return None

    c = 2 * a - locs[0]
    d = 2 * b - locs[1]
    locs[0] = c
    locs[1] = d

    for i in xrange(0, 4):
        locs = wgs2gcj(locs)
        if locs == None:
            return None

        gap = abs(locs[0] - a) + abs(locs[1] - b)
        locs[0] = c
        locs[1] = d
        if gap < 1e-6:
            return locs

        locs = search(a, locs, 0)
        if locs == None:
            return None
        locs = search(b, locs, 1)
        if locs == None:
            return None
        c = locs[0]
        d = locs[1]

    return locs


# Transform Geo from Mars Geodetic System to Baidu Map System
def gcj2bd(args):
    (y, x) = args[0:2]
    z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
    return [z * math.sin(theta) + 0.006, z * math.cos(theta) + 0.0065]


# Transform Geo from Baidu Map System to Mars Geodetic System
def bd2gcj(args):
    x = args[1] - 0.0065
    y = args[0] - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
    return [z * math.sin(theta), z * math.cos(theta)]


# Transform Geo from World Geodetic System to Baidu Map System
def wgs2bd(locs):
    locs = wgs2gcj(locs)
    if locs != None:
        locs = gcj2bd(locs)
    return locs


# Transform Geo from Baidu Map System to World Geodetic System
def bd2wgs(locs):
    locs = bd2gcj(locs)
    if locs != None:
        locs = gcj2wgs(locs)
    return locs


# Check whether location is out of China
def outOfChina(lat, lon):
    return lon < 72.004 or lon > 137.8347 or lat < 0.8293 or lat > 55.8271


def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * \
        y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 *
            math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * pi) + 40.0 *
            math.sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * pi) + 320 *
            math.sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformLon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + \
        0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 *
            math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * pi) + 40.0 *
            math.sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * pi) + 300.0 *
            math.sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret


def search(a, locs, pos):
    c = locs[pos]
    low = c - 2
    high = c + 2
    k = locs[1 - pos]
    mid = low + (high - low) / 2

    while (high - low) >= 1e-7:
        locs[pos] = mid
        locs = wgs2gcj(locs)

        if locs == None:
            return None

        locs[1 - pos] = k
        v = locs[pos]

        if v > a:
            high = mid
            mid = mid - (v - a) * 1.01
            if mid <= low:
                mid = low + (high - low) / 2
        elif v < a:
            low = mid
            mid = mid + (a - v) * 1.01

            if mid > high:
                mid = low + (high - low) / 2
        else:
            locs[pos] = mid
            return locs

    locs[pos] = low + (high - low) / 2
    return locs

version = '0.1'
