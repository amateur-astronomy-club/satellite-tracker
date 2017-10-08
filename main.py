from finder import SpaceObject
from Hardware import Hardware
from time import sleep

hardware = Hardware()
hardware.connect()

obj = SpaceObject('27062')
alt, az = obj.getCoordinates()
hardware.set_target(az, alt)

counter = 0
while True:

	try:
		hardware.loop()
        sleep(0.01)
        counter += 1
        if counter == 100:
        	alt, az = obj.getCoordinates()
			hardware.set_target(az, alt)
        	counter = 0

    except KeyboardInterrupt:
    	hardware.stop()
    	break

