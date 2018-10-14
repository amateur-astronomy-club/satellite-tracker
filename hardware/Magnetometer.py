from math import pi, atan2
import smbus


DEVICE_ADDRESS = 0x1e  # HMC5883L address
FIXED_ERROR = 0  # error of magnetometer in deg. Includes declination (deviation from true north)


class Magnetometer:
    """
    class to interface with HMC5883L magnetometer
    """
    def __init__(self, i2c_bus):
        """
        open I2C BUS
        :param i2c_bus: bus number on rpi to be used
        """
        self.bus = smbus.SMBus(i2c_bus)

    def setup(self):
        """
        setup magnetometer to read in continuous measurement mode. Refer data-sheet for more detail.
        """
        self.bus.write_byte_data(DEVICE_ADDRESS, 0x00, 0x70)
        self.bus.write_byte_data(DEVICE_ADDRESS, 0x01, 0xA0)
        self.bus.write_byte_data(DEVICE_ADDRESS, 0x02, 0x00)

    def read_data(self, address):
        """
        read data from registers of HMC5883L
        Used to read measurement for each axis
        refer data-sheet for details

        :param address: address of register to read from
        :return: final measurement
        """
        msb = self.bus.read_byte_data(DEVICE_ADDRESS, address)
        lsb = self.bus.read_byte_data(DEVICE_ADDRESS, address + 1)
        data = (msb << 8) | lsb

        if data > 32768:
            data = data - 65536

        return data

    def read_axis(self):
        """
        Read magnetometer data for each axis
        :return:
        """
        x = self.read_data(0x03)
        z = self.read_data(0x05)
        y = self.read_data(0x07)

        return x, y, z

    def get_heading(self):
        """
        Calculates the heading angle from measurements.
        Returns angle in clockwise from north format.

        Placement of sensor:
        -Assumes axis x and z are on the plane on which heading is calculated
        -Axis x should point eastwards when z points north to get measurements
            clockwise from north (azimuth convention)

        :return: heading angle in degrees
        """

        x, y, z = self.read_axis()  # read measurements

        heading_angle = atan2(-x, -z)  # neg. of x and z used to get clockwise angle
        heading_angle = heading_angle % (2*pi)

        return heading_angle * 180 / pi + FIXED_ERROR

    def close(self):
        """
        close bus
        """
        self.bus.close()
