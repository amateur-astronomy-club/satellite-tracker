#This is a fork from http://www.sharebrained.com/2011/10/18/track-the-iss-pyephem/
#Lots of changes to be made

import math
import time
from datetime import datetime
import ephem

degrees_per_radian = 180.0 / math.pi

home = ephem.Observer()

home.lon = '74.7421430'   # +E
home.lat = '13.3408810'      # +N
home.elevation = 0 # meters

print home
# Always get the latest ISS TLE data from:
# http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html
iss = ephem.readtle('ISS',
                    '1 25544U 98067A   16274.50033672  .00016717  00000-0  10270-3 0  9003',
                    '2 25544  51.6383 252.7108 0006713  21.8902 338.2536 15.54019889 21364'
                   )

hst = ephem.readtle('HST',
                    '1 20580U 90037B   16274.23805914  .00001113  00000-0  58355-4 0  9992',
                    '2 20580  28.4700 284.9185 0002511 256.0834 203.4566 15.08518057250982')

while True:
    home.date = datetime.utcnow()
    hst.compute(home)
    print '\rhst: altitude %4.1f deg, azimuth %5.1f deg'% (hst.alt * degrees_per_radian,
                                                         hst.az * degrees_per_radian)
    time.sleep(1)
