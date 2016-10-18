import math
import threading
import time
from datetime import datetime

import ephem
from auromat.coordinates.spacetrack import Spacetrack
from pathlib2 import Path

from python_send import Sender

degrees_per_radian = 180.0 / math.pi


class Scrape():
    def __init__(self, this_sat):
        self.running = False
        self.id = this_sat
        self.checkTLE(this_sat)
        self.sender = Sender()

    def checkTLE(self, index):
        TLEfileExists = Path("./TLE/" + index + '.txt')
        if (TLEfileExists.is_file() == False):
            self.getnewtle(index)

    def getnewtle(self, index):
        # API credentials
        newsat = Spacetrack("asavari.limaye@gmail.com", "2016AACNITK2017")
        tledata = newsat.query(
            "class/tle_latest/NORAD_CAT_ID/%s/orderby/ORDINAL asc/limit/1/format/3le/metadata/false" % index)

        writefile = open("./TLE/" + index + '.txt', "w")
        writefile.write(tledata)
        writefile.close()

    # change all . to respective folder
    def setDefaultHome(self):
        home = ephem.Observer()
        home.lon = '0.0000'  # +E
        home.lat = '0.0000'  # +N
        home.elevation = 0  # meters
        return home

    def setNITKHome(self):
        home = ephem.Observer()
        home.lon = '74.7937'  # +E
        home.lat = '13.0119'  # +N
        home.elevation = 24  # meters
        return home

    def setCurrentHome(self):
        home = ephem.Observer()
        # TODO: Get current location
        return home

    def printCoordinates(self, index, home):

        tlefile = open('./TLE/' + index + '.txt', 'r').read()
        tlesplit = tlefile.split('\n')

        assert len(tlesplit) >= 3

        sat = ephem.readtle(tlesplit[0], tlesplit[1], tlesplit[2])
        print "Tracking", tlesplit[0][2:]
        while self.running:

            home.date = datetime.utcnow()
            sat.compute(home)
            print '\rsat: altitude %4.1f deg, azimuth %5.1f deg' % (sat.alt * degrees_per_radian,
                                                                    sat.az * degrees_per_radian)

            time.sleep(2)

    def convertToIndex(self, SateliteName):
        # TODO: Given satellite name, convert to index (use dictionary)
        print ('todo')

    def sendCoordinates(self, index, home):
        # Get TLE and convert to coordinates, send to arduino


        tlefile = open('./TLE/' + index + '.txt', 'r').read()
        tlesplit = tlefile.split('\n')

        assert len(tlesplit) >= 3

        sat = ephem.readtle(index, tlesplit[1], tlesplit[2])

        i = 0
        while self.running:
            home.date = datetime.utcnow()
            sat.compute(home)
            print '\rsat: altitude %4.1f deg, azimuth %5.1f deg' % (sat.alt * degrees_per_radian,
                                                                    sat.az * degrees_per_radian)

            i += 1
            if i >= 3:
                i = 3
                self.sender.send(sat.alt * degrees_per_radian, sat.az * degrees_per_radian)

            # TODO: Convert this to sending it to arduino, maybe add arguments
            # print '\rsat: altitude %4.1f deg, azimuth %5.1f deg'% (sat.alt * degrees_per_radian,
            #                                         sat.az * degrees_per_radian)
            time.sleep(2)

    def run(self):
        self.running = True
        home = self.setNITKHome()

        def to_thread():
            # self.printCoordinates(self.id, home)
            self.sendCoordinates(self.id, home)

        t_s = threading.Thread(target=to_thread)
        t_s.setDaemon(True)
        t_s.start()

    def stop(self):
        self.running = False
        self.sender.end()


if __name__ == '__main__':
    scrapper = Scrape('26702')
    scrapper.run()
    raw_input()
    scrapper.stop()
