import datetime
import threading
from datetime import timedelta
import scraper
import ephem
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap


class Plot():
    def __init__(self,this_sat):
        self.running = False
        self.id = this_sat
        scraper.checkTLE(this_sat)

    def to_run(self):
        # Setup lat long of telescope
        home = ephem.Observer()

        home.long = np.deg2rad(74.7421430)  # +E
        home.lat = np.deg2rad(13.3408810)  # +N
        home.elevation = 0  # meters
        home.date = datetime.datetime.now()

        print './TLE/' + self.id + '.txt', 'r'
        tlefile = open('./TLE/' + self.id + '.txt', 'r').read()
        tlesplit = tlefile.split('\n')

        assert len(tlesplit) >= 3
        print './TLE/' + self.id + '.txt', 'r'
        satellite = ephem.readtle(self.id, tlesplit[1], tlesplit[2])
        print satellite
        # Make some datetimes
        current_time = datetime.datetime.now()
        past_time = current_time + timedelta(hours=-1)
        dt = [current_time + timedelta(seconds=1 * x) for x in range(0, 24 * 60 * 60)]
        dt_past = [past_time + timedelta(seconds=1 * x) for x in range(0, 60 * 60)]

        # Compute satellite locations at each datetime
        sat_lat, sat_lon, sat_latp, sat_lonp = [], [], [], []
        for date in dt:
            home.date = date
            satellite.compute(home)
            sat_lon.append(np.rad2deg(satellite.sublong))
            sat_lat.append(np.rad2deg(satellite.sublat))

        for date in dt_past:
            home.date = date
            satellite.compute(home)
            sat_lonp.append(np.rad2deg(satellite.sublong))
            sat_latp.append(np.rad2deg(satellite.sublat))

        for i in range(len(sat_lon)):
            if sat_lon[i] < 0:
                sat_lon[i] = 360 + sat_lon[i]
        for i in range(len(sat_lonp)):
            if sat_lonp[i] < 0:
                sat_lonp[i] = 360 + sat_lonp[i]

        # miller projection
        map = Basemap(projection='mill', lon_0=180)
        # plot coastlines, draw label meridians and parallels.
        map.drawcoastlines()
        map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
        map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
        # fill continents 'coral' (with zorder=0), color wet areas 'aqua'
        map.drawmapboundary(fill_color='aqua')
        # map.fillcontinents(color='coral',lake_color='aqua')
        # shade the night areas, with alpha transparency so the
        # map shows through. Use current time in UTC.
        date = datetime.datetime.utcnow()
        x, y = map(sat_lon, sat_lat)
        x = np.atleast_1d(x)
        y = np.atleast_1d(y)

        xp, yp = map(sat_lonp, sat_latp)
        xp = np.atleast_1d(xp)
        yp = np.atleast_1d(yp)

        CS = map.nightshade(date)

        plt.scatter(xp, yp, color='y', s=5, label="Past Hour")
        plt.ion()

        for i in range(len(sat_lon)):
            plt.scatter(x[i], y[i], color='r', label="realtime")
            plt.pause(1)

        while self.running:
            plt.pause(1)

        # plt.title('Day/Night Map for %s (UTC)' % date.strftime("%d %b %Y %H:%M:%S"))
        # plt.show()

        plt.close('all')

    def run(self):
        self.running = True

        def to_thread():
            self.to_run()

        t_s = threading.Thread(target=to_thread)
        t_s.setDaemon(True)
        t_s.start()

    def stop(self):
        self.running = False


if __name__ == "__main__":
    plotter = Plot('26702')
    plotter.run()
    raw_input()
    plotter.stop()
