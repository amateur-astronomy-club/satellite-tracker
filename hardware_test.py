from hardware import Hardware
from time import sleep

hardware = Hardware()
hardware.connect()
hardware.set_target(0, 0)

try:
    while True:
        hardware.loop()
        sleep(0.01)
except KeyboardInterrupt:
    hardware.stop()

