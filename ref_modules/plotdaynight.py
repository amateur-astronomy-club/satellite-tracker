import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

import ephem
import datetime

# Setup lat long of telescope
home = ephem.Observer()

home.long = np.deg2rad(74.7421430)  # +E
home.lat = np.deg2rad(13.3408810)     # +N
home.elevation = 0 # meters
home.date = datetime.datetime.now()

# Always get the latest ISS TLE data from:
# http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html
iss = ephem.readtle('ISS',
                    '1 25544U 98067A   16274.50033672  .00016717  00000-0  10270-3 0  9003',
                    '2 25544  51.6383 252.7108 0006713  21.8902 338.2536 15.54019889 21364'
                   )

# Make some datetimes
midnight = datetime.datetime.replace(datetime.datetime.now())
dt  = [midnight + datetime.timedelta(seconds=1*x) for x in range(0, 24*60*60)]



# Compute satellite locations at each datetime
sat_lat, sat_lon = [], []
for date in dt:
    home.date = date
    iss.compute(home)
    sat_lon.append(np.rad2deg(iss.sublong))
    sat_lat.append(np.rad2deg(iss.sublat))


for i in range(len(sat_lon)):
    if sat_lon[i]<0:
        sat_lon[i]=360+sat_lon[i]



# miller projection
map = Basemap(projection='mill',lon_0=180)
# plot coastlines, draw label meridians and parallels.
map.drawcoastlines()
map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])
# fill continents 'coral' (with zorder=0), color wet areas 'aqua'
map.drawmapboundary(fill_color='aqua')
#map.fillcontinents(color='coral',lake_color='aqua')
# shade the night areas, with alpha transparency so the
# map shows through. Use current time in UTC.
date = datetime.datetime.utcnow()
x,y=map(sat_lon,sat_lat)
x = np.atleast_1d(x)
y = np.atleast_1d(y)
CS=map.nightshade(date)

#plt.scatter(x,y,color='r')
plt.ion()

for i in range(len(sat_lon)):
    plt.scatter(x[i],y[i],color='r')
    plt.pause(1)

while True:
    plt.pause(1)

plt.title('Day/Night Map for %s (UTC)' % date.strftime("%d %b %Y %H:%M:%S"))
plt.show()
