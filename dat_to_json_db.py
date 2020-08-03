import re
from math import pi, sin, cos

MAGNITUDE_LIMIT = '4'
INPUT_DATA = "bright_star_catalog.dat"
OUTPUT_DATA = "star_db_" + MAGNITUDE_LIMIT + ".json"
unit_deg = float(pi / 180)
unit_cm = 1. / 100
# Outer radius of planisphere
r_1 = 8.0 * unit_cm
# Outer rim width with dates marked
r_gap = 1.1 * unit_cm
r_2 = r_1 - r_gap
latitude = 45

def radius(dec, latitude):
    dec_span = (90 + (90 - latitude)) * 1.125
    if latitude >= 0:
        return (90 - dec) / dec_span * r_2
    else:
        return (90 + dec) / dec_span * r_2


# Build a dictionary of stars, indexed by HD number
stars = {}

# Loop through the Yale Bright Star Catalog, line by line
bs_num = 0
for line in open(INPUT_DATA, "rt"):
    # Ignore blank lines and comment lines
    if (len(line) < 100) or (line[0] == '#'):
        continue

    # Counter used too calculated the bright star number -- i.e. the HR number -- of each star
    bs_num += 1
    try:
        # Read the Henry Draper (i.e. HD) number for this star
        hd = int(line[25:31])

        # Read the right ascension of this star (J2000)
        ra_hrs = float(line[75:77])
        ra_min = float(line[77:79])
        ra_sec = float(line[79:82])

        # Read the declination of this star (J2000)
        dec_neg = (line[83] == '-')
        dec_deg = float(line[84:86])
        dec_min = float(line[86:88])
        dec_sec = float(line[88:90])

        # Read the V magnitude of this star
        mag = float(line[102:107])
    except ValueError:
        continue

    # Turn RA and Dec from sexagesimal units into decimal
    ra = (ra_hrs + ra_min / 60 + ra_sec / 3600) / 24 * 360
    dec = (dec_deg + dec_min / 60 + dec_sec / 3600)
    if dec_neg:
        dec = -dec

    # Discard stars fainter than mag 4
    faint_limit = 4  # 3.5
    if mag == "-" or float(mag) > faint_limit:
        continue

    ra = float(ra)
    dec = float(dec)
    r = radius(dec=dec, latitude=latitude)
    if r > r_2:
        continue
    centre_x = -r * cos(ra * unit_deg)*10000
    centre_y = r * sin(ra * unit_deg)*10000
    brightness = (faint_limit - mag)*2

    # Build a dictionary is stars, indexed by HD number
    stars[hd] = [centre_x, centre_y, brightness]
import json
with open(OUTPUT_DATA, 'w') as fp:
    json.dump(stars, fp)