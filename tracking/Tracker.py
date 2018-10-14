from helpers.Ticker import Ticker
from tracking import NITK
from math import degrees

from datetime import datetime  # ensure your datetime is correct


class Tracker(Ticker):
    """
    Finds position in the sky of any ephem space object given observer location
    Periodically updates the position
    """

    def __init__(self, home=NITK, freq=1, verbose=1):
        """
        Initialize
        :param home: Observer object
        :param freq: update frequency
        :param verbose: control logging, 0 for no log, 1 for important events, 2 for event update every loop
        """
        self.space_object = None
        self.home = home

        self.azimuth = None
        self.altitude = None

        self.verbose = verbose

        self.callback = None  # function to call at end of each step. Used to interface with hardware class

        # print a reminder
        if self.verbose >= 1: print("Ensure your device date/time is set correctly for accurate functioning...")

        super(Tracker, self).__init__(freq)

    def set_callback(self, callback):
        """
        Sets callback function
        :param callback: function to be called back at end of every step
        """
        self.callback = callback

    def set_object(self, space_object):
        """
        Set object to track
        :param space_object: ephem object to track
        """
        self.space_object = space_object

    def get_position(self):
        """
        Get latest position of objects being tracked
        :return: azimuth and altitude of object being tracked
        """
        return self.azimuth, self.altitude

    def step(self):
        """
        One update of position of space object
        """
        # Get orbit_data and convert to coordinates, send to arduino

        if self.space_object is None:  # can't track if object not available
            self.altitude = None
            self.azimuth = None
        else:
            self.home.date = datetime.utcnow()
            self.space_object.compute(self.home)

            self.altitude = degrees(self.space_object.alt)
            self.azimuth = degrees(self.space_object.az)

            if self.verbose >= 2: print('Track Updated; Alt: ', self.altitude, ', ', 'Az: ', self.azimuth)

        if callable(self.callback): self.callback()

    def start(self):
        """
        Start tracking and updating position
        """
        if self.verbose >= 1: print("Starting Tracker Thread...")
        super(Tracker, self).start()

    def stop(self):
        """
        Stop tracking and updating position
        """
        if self.verbose >= 1: print("Stopping Tracker Thread...")
        super(Tracker, self).stop()
        if self.verbose >= 1: print("Tracker Successfully Stopped...")

        self.azimuth = None
        self.altitude = None
        self.space_object = None
