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

stopped = False

while True:
    try:
        sleep(1)
        alt, az = obj.getCoordinates()
        print alt, az
        hardware.set_target(az, alt)

    except KeyboardInterrupt:
        hardware.stop()
        stopped = True
        break
if not stopped: hardware.stop()
