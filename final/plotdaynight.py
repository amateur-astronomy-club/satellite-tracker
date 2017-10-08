import datetime
import threading
import ephem
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from auromat.coordinates.spacetrack import Spacetrack
from pathlib2 import Path
from datetime import timedelta

class Plot:

    """Plot class that iisused to nteractively plot real time position of satellite
  
    """

    def __init__(self, this_sat):
        self.running = False
        self.id = this_sat

        # Check if TLE exists, else make API call
        self.checkTLE(this_sat)

    def checkTLE(self, index):
        """Check if TLE exists for given satellite, else call getnewtle()
        
        Args:
            index (str): NORAD ID of satellite
        """
        TLEfileExists = Path("./TLE/" + index + '.txt')
        if (TLEfileExists.is_file() == False):
            self.getnewtle(index)

    def getnewtle(self, index):
        """Make Spactrack API call and download TLE for current satellite and save it locally
        
        Args:
            index (str): NORAD ID of satellite
        """

        # API credentials
        newsat = Spacetrack("asavari.limaye@gmail.com", "2016AACNITK2017")
        
        # Get TLE for specified index(NORAD ID)
        tledata = newsat.query(
            "class/tle_latest/NORAD_CAT_ID/%s/orderby/ORDINAL asc/limit/1/format/3le/metadata/false" % index)

        # Save TLE to file
        writefile = open("./TLE/" + index + '.txt', "w")
        writefile.write(tledata)
        writefile.close()

    def to_run(self):
        """Interactive plotting of satellite postion after data generation.
           This is the function that the thread runs.

        """
        # Setup lat long of telescope
        home = ephem.Observer()

        # NITK credentials
        home.long = np.deg2rad(74.7421430)  # +E
        home.lat = np.deg2rad(13.3408810)  # +N
        home.elevation = 0  # meters
        home.date = datetime.datetime.now()

        # Read TLE file
        tlefile = open('./TLE/' + self.id + '.txt', 'r').read()
        tlesplit = tlefile.split('\n')

        assert len(tlesplit) >= 3

        satellite = ephem.readtle(tlesplit[0], tlesplit[1], tlesplit[2])

        # Make some datetimes
        # We will plot the path for thepast hour then start real time tracking
        # We pre compute values for 24 hours
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

        # Calibrate everything to have positive values
        for i in range(len(sat_lon)):
            if sat_lon[i] < 0:
                sat_lon[i] = 360 + sat_lon[i]
        for i in range(len(sat_lonp)):
            if sat_lonp[i] < 0:
                sat_lonp[i] = 360 + sat_lonp[i]

        # miller projection using Basemap
        mymap = Basemap(projection='mill', lon_0=180)

        # plot coastlines, draw label meridians and parallels.
        mymap.drawcoastlines()
        mymap.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
        mymap.drawmeridians(np.arange(mymap.lonmin, mymap.lonmax + 30, 60), labels=[0, 0, 0, 1])
        
        # fill continents 'coral' (with zorder=0), color wet areas 'aqua'
        mymap.drawmapboundary(fill_color='aqua')

        # shade the night areas, with alpha transparency so the
        # mymap shows through. Use current time in UTC.
        # Prepare values to plot
        date = datetime.datetime.utcnow()

        # convert to map projection co-ordinates
        x, y = mymap(sat_lon, sat_lat)
        xp, yp = mymap(sat_lonp, sat_latp)

        # Convert to numpy arrays
        # atleast_1d makes sure arrays are atleast 1-d, unnecessary check for scalars
        x = np.atleast_1d(x)
        y = np.atleast_1d(y)
        xp = np.atleast_1d(xp)
        yp = np.atleast_1d(yp)

        # compute night shade for the given date
        CS = mymap.nightshade(date)
        
        # Set some properties for the plot window
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()

        # Plot the past hour data
        plt.scatter(xp, yp, color='y', s=5, label="Past Hour")
        
        # Now we start plotting interactively
        plt.ion()
        plt.scatter(x[0], y[0], color='#FF3F35', label="Real time")

        # Position legend and set transparency
        leg = plt.legend(fancybox=True, shadow=True, loc=4)
        leg.get_frame().set_alpha(0.1)

        # We have calculated data for every second for 24 hours from current time
        # We plot eachdata point with one second delaytosimulate real time plotting

        for i in range(1, len(sat_lon)):
            plt.scatter(x[i], y[i], color='#FF3F35', label="Real time")
            plt.pause(1)

        # If done plotting everything, just pause
        while self.running:
            plt.pause(1)

        plt.close('all')

    def run(self):
        self.running = True

        #def to_thread():
            #self.to_run()

        t_s = threading.Thread(target=self.to_run)
        t_s.setDaemon(True)
        t_s.start()

    def stop(self):
        self.running = False


if __name__ == "__main__":
    plotter = Plot('26702')
    plotter.run()
    raw_input()
    plotter.stop()
