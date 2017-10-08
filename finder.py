import time
import math
import ephem
from auromat.coordinates.spacetrack import Spacetrack
from pathlib2 import Path
from datetime import datetime
# from plotdaynight import Plot
degrees_per_radian = 180.0 / math.pi


class SpaceObject():
    def __init__(self, this_object):
        """Summary
        
        Args:
            this_object (str or Ephem Body Instance): Pass NORAD ID of satellite or pass a Ephem Body Instance
        """
        self.running = False
        if type(this_object) is str:
            self.sat = True
            self.id = this_object
            self.checkTLE()
            self.loadTLE()
        else:
            self.object = this_object

        self.home = self.setNITKHome()

    def checkTLE(self):
        #Check if provided TLE is already present in TLE folder, else download from Spacetrack
        if self.sat:
            TLEfileExists = Path("./TLE/" + self.id + '.txt')
            if (TLEfileExists.is_file() == False):
                self.getnewtle()
        else:
            print "Not a satellite."

    def getnewtle(self):
        #Get new TLE from SpaceTrack API and sve in TLE folder
        # API credentials
        if self.sat:
            newsat = Spacetrack("asavari.limaye@gmail.com", "2016AACNITK2017")
            tledata = newsat.query(
                "class/tle_latest/NORAD_CAT_ID/%s/orderby/ORDINAL asc/limit/1/format/3le/metadata/false" % self.id)

            writefile = open("./TLE/" + self.id + '.txt', "w")
            writefile.write(tledata)
            writefile.close()

        else:
            print "Not a satellite."

    
    def setNITKHome(self):
        #provides lon lat details of NITK Surathkal. MOdify according to your location
        home = ephem.Observer()
        home.lon = '74.7937'  # +E
        home.lat = '13.0119'  # +N
        home.elevation = 24  # meters
        return home


    def convertToIndex(self, SateliteName):
        # TODO: Given satellite name, convert to index (use dictionary)
        print ('todo')

    def loadTLE(self):
        if self.sat:
            tlefile = open('./TLE/' + self.id + '.txt', 'r').read()
            tlesplit = tlefile.split('\n')

            assert len(tlesplit) >= 3

            self.object = ephem.readtle(self.id, tlesplit[1], tlesplit[2])
            print "Done loading TLE for NORAD ID ", self.id
            # plotter = Plot(self.id)
            # plotter.run()
        else:
            print "Not a satellite."


    def getCoordinates(self):
        # Get TLE and convert to coordinates, send to arduino

        
        self.home.date = datetime.utcnow()
        self.object.compute(self.home)
        return self.object.alt * degrees_per_radian, self.object.az * degrees_per_radian

        


if __name__ == '__main__':
    scrapper = SpaceObject('26702')

    alt, az = scrapper.getCoordinates()
    print alt, az


