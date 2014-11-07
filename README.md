GeoConverter
============

Geo Converter between WGS/GCJ/BD

API:

locs: [latitude, longitude]

Transform Geo from World Geodetic System to Mars Geodetic System in China:
locs wgs2gcj(locs)

Transform Geo from Mars Geodetic System to World Geodetic System in China:
locs gcj2wgs(locs)

Transform Geo from Mars Geodetic System to Baidu Map System:
locs gcj2bd(locs)

Transform Geo from Baidu Map System to Mars Geodetic System:
locs bd2gcj(locs)

Transform Geo from World Geodetic System to Baidu Map System:
locs wgs2bd(locs)

Transform Geo from Baidu Map System to World Geodetic System:
locs bd2wgs(locs)
