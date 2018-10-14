from helpers.Ticker import Ticker

from Magnetometer import Magnetometer
from DCMotor import DCMotor
from Servo import Servo

from PID import PID


class Control(Ticker):
    """
    Controls hardware components.
    Threaded using threading library

    altitude control happens using Servo
    Azimuth control is based on a PID feedback loop. A DC motor controls azimuth.
    """

    def __init__(self, freq=100, verbose=1):
        """
        Sets up PID, and initialize variables
        :param freq: frequency of control loop in Hz
        :param verbose: control logging, 0 for no log, 1 for important events, 2 for event update every loop
        """

        # set up PID
        self.pid = PID(2, 0.10, 20)  # 3 0.8 20 # Trial and Error values, tuned values
        self.pid.setWindup(75)  # 100

        self.azimuth_target = None  # Current target for PID
        self.altitude_target = None  # Servo target

        # components
        self.motor = DCMotor(pin1=18, pin2=17, PWM_freq=1000)  # sufficiently high PWM rate
        self.servo = Servo(pin=22)
        self.mag = Magnetometer(i2c_bus=1)

        self.verbose = verbose  # control logging

        self.error_report = None  # for reporting azimuth error of the controller externally
        self.pid_report = None  # for reporting PID output externally

        super(Control, self).__init__(freq)

    def set_target(self, azimuth, altitude):
        """
        set target point
        :param azimuth: azimuth of target
        :param altitude: altitude of target
        """
        self.altitude_target = altitude
        self.azimuth_target = azimuth

        # directly set the servo as it doesn't involve a PID loop
        self.servo.set(altitude + 90)  # servo angle range is from 0 to 180

    def start(self):
        """
        Initialize HW components and starts thread
        """

        if self.verbose >= 1: print("Initializing HW Components...")
        self.motor.start()
        self.servo.start()
        self.mag.setup()
        if self.verbose >= 1: print("Initialized HW Components...")

        if self.verbose >= 1: print("Starting Control Loop...")
        super(Control, self).start()

    def target_available(self):
        """
        checks if targets are available
        :return: true if azimuth and altitude target is available
        """
        if self.altitude_target is not None and self.azimuth_target is not None:
            return True
        else:
            return False

    def step(self):
        """
        One control loop update.
        Calculates error and logs data
        """
        if not self.target_available():
            self.motor.set(0)
            return  # don't execute if targets not available

        error = self.find_error()
        self.pid.update(error)
        self.motor.set(-self.pid.output)  # negative of PID output; correction is in opp. direction

        self.error_report = error
        self.pid_report = self.pid.output

        if self.verbose >= 2: print("Az. Error: ", error, " , ", "PID Resp. : ", self.pid.output)

    def find_error(self):
        """
        Find the error between azimuth target and current live azimuth
        :return:
        """
        mag = self.mag.get_heading()

        error = self.azimuth_target - mag

        if error < 0: error = 360 + error  # convert to 0 - 360 from -x to -x + 360
        if error > 180: error = -(360 - error)  # convert to -180 to 180
        return error

    def stop(self):
        """
        Stops Thread and resets necessary variables
        """
        if self.verbose >= 1: print("Stopping Control Loop...")
        super(Control, self).stop()
        if self.verbose >= 1: print("Loop Successfully Stopped...")

        self.motor.stop()
        self.servo.stop()
        self.mag.close()

        self.azimuth_target = None
        self.altitude_target = None
        self.error_report = None
        self.pid_report = None

        self.pid.clear()

    def report(self):
        """
        reports error and pid output for external logging if necessary
        :return:
        """
        return self.error_report, self.pid_report
