import numpy as np
import matplotlib.pyplot as plt
import ephem
import datetime

# Setup lat long of telescope
home = ephem.Observer()

home.long = np.deg2rad(74.7421430)  # +E
home.lat = np.deg2rad(13.3408810)     # +N
home.elevation = 0 # meters
home.date = datetime.datetime.now()
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

l1 = 'GPS-BIIF-1'
l2 = '1 36585U 10022A   16274.48929751 -.00000086  00000-0  00000+0 0  9991'
l3 = '2 36585  56.0508 350.9177 0054304  43.1031 261.3215  2.00561804 46458'
bf = ephem.readtle(l1,l2,l3)
# Make some datetimes
midnight = datetime.datetime.replace(datetime.datetime.now(), hour=0)
dt  = [midnight + datetime.timedelta(minutes=20*x) for x in range(0, 24*3)]



# Compute satellite locations at each datetime
sat_alt, sat_az = [], []
for date in dt:
    home.date = date
    iss.compute(home)
    sat_alt.append(np.rad2deg(iss.alt))
    sat_az.append(np.rad2deg(iss.az))

# Plot satellite tracks
'''plt.subplot(211)
plt.plot(dt, sat_alt)
plt.ylabel("Altitude (deg)")
plt.xticks(rotation=25)
plt.subplot(212)
plt.plot(dt, sat_az)
plt.ylabel("Azimuth (deg)")
plt.xticks(rotation=25)
plt.show()'''

# Plot satellite track in polar coordinates
plt.polar(np.deg2rad(sat_az), 90-np.array(sat_alt))
plt.ylim(0,90)
plt.show()
