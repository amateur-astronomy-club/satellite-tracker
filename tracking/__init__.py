import ephem
import urllib
import os

# observer coordinates for NITK. Set your location
NITK = ephem.Observer()
NITK.lon = '74.7937'  # +E
NITK.lat = '13.0119'  # +N
NITK.elevation = 24  # meters

KNOWN_OBJS = {"mercury": ephem.Mercury(),
              "venus": ephem.Venus(),
              "mars": ephem.Mars(),
              "jupiter": ephem.Jupiter(),
              "saturn": ephem.Saturn(),
              "uranus": ephem.Uranus(),
              "neptune": ephem.Neptune(),
              "pluto": ephem.Pluto(),
              "sun": ephem.Sun(),
              "moon": ephem.Moon()}

TLE_FILE_PATH = os.path.join(os.path.dirname(__file__), 'orbit_data',
                             'tle.txt')  # a constant path that doesn't change with imports


def get_norad_id(tle):
    """
    Extracts norad id from TLE
    """
    l1, l2, l3 = tle
    return int(l3.split()[1])


def load_tle():
    """
    Load saved TLE files
    """
    with open(TLE_FILE_PATH, 'r') as f:
        lines = f.readlines()

    try:
        assert len(lines) % 3 == 0
    except:
        print("Coudn't Load TLE data...")
        return {}

    tles = [(lines[i + 0], lines[i + 1], lines[i + 2]) for i in xrange(0, len(lines), 3)]

    ids = map(get_norad_id, tles)
    ephem_objects = map(lambda x: ephem.readtle(*x), tles)

    sats = dict(zip(ids, ephem_objects))

    return sats


KNOWN_SATS = load_tle()


def parser(name):
    """
    converts text (name or id) into ephem object
    """
    name = name.lower()
    if name in KNOWN_OBJS.keys():
        return KNOWN_OBJS[name]
    elif name.isdigit() and int(name) in KNOWN_SATS.keys():
        return KNOWN_SATS[int(name)]
    else:
        return None


def update_tle():
    """
    Update TLE files from http://celestrak.com/NORAD/elements/active.txt
    """
    testfile = urllib.URLopener()
    try:
        testfile.retrieve("http://celestrak.com/NORAD/elements/active.txt", TLE_FILE_PATH)
    except:
        print("Unable to update TLE files...")
