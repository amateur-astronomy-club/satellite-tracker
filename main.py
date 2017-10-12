from time import sleep

import ephem

from app import object_setter
from finder import SpaceObject
from hardware import Hardware

hardware = Hardware()
hardware.connect()

obj = None
known_objects = {"Mercury": ephem.Mercury(),
                 "Venus": ephem.Venus(),
                 "Mars": ephem.Mars(),
                 "Jupiter": ephem.Jupiter(),
                 "Saturn": ephem.Saturn(),
                 "Uranus": ephem.Uranus(),
                 "Neptune": ephem.Neptune(),
                 "Pluto": ephem.Pluto(),
                 "Sun": ephem.Sun(),
                 "Moon": ephem.Moon(),
                 "ISS": '25544'}


def set_object():
    global obj
    http_text = obj_s.current_object
    if http_text is None:
        obj = None
    else:
        try:
            obj = SpaceObject(known_objects[http_text])
        except:
            print "Couldn't Find Object..."
    print "Set to object: ", obj


obj_s = object_setter()
current_obj = obj_s.current_object

hardware.set_target(0, 0)

hardware.run_loop(verbose=True)

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

        sleep(1)

        # print hardware.loop()

    except KeyboardInterrupt:
        hardware.stop()
        stopped = True
        break
