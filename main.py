from time import sleep

from hardware import Hardware
from finder import SpaceObject

import ephem

hardware = Hardware()
hardware.connect()

obj = SpaceObject(ephem.Jupiter())
alt, az = obj.getCoordinates()
hardware.set_target(az, alt)

print hardware.run_loop()

while True:
    try:
        sleep(1)
        alt, az = obj.getCoordinates()
        print alt, az
        hardware.set_target(az, alt)

    except KeyboardInterrupt:
        hardware.stop()
        break
hardware.stop()
