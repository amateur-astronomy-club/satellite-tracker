import serial

from PID import PID


class Hardware:
    def __init__(self):
        self.pid = PID(3, 2, 20)  # 3 0.8 20 # Trial and Error values
        self.pid.setWindup(50)  # 100
        self.top_arduino = None
        self.base_arduino = None

        self.base_target = None

    def connect(self, port1="COM4", port2="COM6"):
        print "Initializing Bluetooth Connection..."
        self.top_arduino = serial.Serial(port1, 9600, timeout=1)  # open serial port that Arduino is using
        print "Connecting to Arduino..."
        self.base_arduino = serial.Serial(port2, 9600, timeout=1)  # open serial port that Arduino is using
        self.top_arduino.flushInput()  # clear buffer because Arduino has been sending values

    def set_motor(self, val):
        val = int(val)
        if val > 255: val = 255
        if val < -255: val = -255
        self.base_arduino.write(str(val) + '\n')

    def read_mag(self):
        try:
            return float(self.top_arduino.readline().strip())
        except:
            return None

    def set_servo(self, angle):

        if angle > 90: angle = 90
        if angle < -90: angle = -90
        angle += 90  # 0 - 180 range
        angle = 180 - angle  # invert because of placement of servo

        val = float(angle) / 180 * 1800 + 550  # convert to range as found by testing
        val = str(int(val)) + '!'  # endline convention as adopted; also followed in Arduino
        # padding 0 as convention adopted
        while len(val) < 5:
            val = '0' + val

        self.top_arduino.write(val)

    def convert_mag(self, mag):
        if mag != 0: mag = 360 - mag  # counter clockwise to clockwise
        mag -= 26  # fixed error of magnetometer
        if mag < 0: mag = 360 + mag  # warp around
        return mag

    def stop(self):
        self.top_arduino.close()
        self.base_arduino.close()
        self.pid.clear()

    def find_error(self):
        mag = self.read_mag()
        if mag is None: return None
        mag = self.convert_mag(mag)
        error = self.base_target - mag
        if error < 0: error = 360 + error  # convert to 0 - 360 from -x to -x + 360
        if error > 180: error = -(360 - error) # convert to -180 to 180
        return error

    def set_target(self, azimuth, elevation):
        self.set_servo(elevation)
        self.base_target = azimuth

    def loop(self):
        if self.base_target is None: return None
        error = self.find_error()
        if error is None: return
        self.pid.update(error)
        self.set_motor(self.pid.output)
        return error


