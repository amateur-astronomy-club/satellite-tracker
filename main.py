from time import sleep

import ephem  # Don't Remove

from app import object_setter
from finder import SpaceObject
from hardware import Hardware

hardware = Hardware()
hardware.connect()

obj = None
known_objects = {"Jupiter": ephem.Jupiter(), "Saturn": ephem.Saturn(),
                 "Venus": ephem.Venus(), "Sun": ephem.Sun(),
                 "Mars": ephem.Mars(), "Moon": ephem.Moon(),
                 "Pluto": ephem.Pluto()}


def set_object():
    global obj
    http_text = obj_s.current_object
    if http_text is None:
        obj = None
    elif http_text == "ISS":
        obj = SpaceObject('25544')
    else:
        try:
            obj = SpaceObject(known_objects[http_text])
        except:
            print "Couldn't Find Object..."
    print "Set to object: ", obj


obj_s = object_setter()
current_obj = obj_s.current_object

hardware.set_target(0, 0)

# hardware.run_loop(verbose=True)

while True:
    try:
        if current_obj != obj_s.current_object:
            current_obj = obj_s.current_object
            set_object()

        print obj

        if obj is None:
            alt, az = 0, 0
        else:
            alt, az = obj.getCoordinates()
        # print alt, az

        hardware.set_target(az, alt)

        sleep(0.01)

        print hardware.loop()

    except KeyboardInterrupt:
        hardware.stop()
        stopped = True
        break
