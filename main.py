from time import sleep

from hardware import Hardware
from finder import SpaceObject

import ephem

hardware = Hardware()
hardware.connect()

obj = SpaceObject('26702')
alt, az = obj.getCoordinates()
hardware.set_target(az, alt)

counter = 0
while True:
    try:
        print hardware.loop()
        sleep(0.01)
        counter += 1
        if counter == 100:
            alt, az = obj.getCoordinates()
            print alt, az
            hardware.set_target(az, alt)
            counter = 0

    except KeyboardInterrupt:
        hardware.stop()
        break
hardware.stop()