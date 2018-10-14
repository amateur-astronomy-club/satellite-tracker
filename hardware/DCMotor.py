import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class DCMotor:
    """
        Class to Interface with a DC motor through a motor driver (L293D).
        DC motor controls the azimuth of the pointer.
    """

    def __init__(self, pin1, pin2, PWM_freq):
        """
        Initialize pins and setup PWM with appropriate frequency
        :param pin1: rotates pointer clockwise (while looking from above)
        :param pin2: rotates pointer counter-clockwise (while looking from above)
        """
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.setup(pin2, GPIO.OUT)
        self.pin1 = GPIO.PWM(pin1, PWM_freq)  # default: 1000 Hz PWM
        self.pin2 = GPIO.PWM(pin2, PWM_freq)  # keep PWM freq sufficiently above control loop freq (def.: 100 hz)

    def start(self):
        """
        start PWM
        """
        self.pin1.start(0)
        self.pin2.start(0)  # 0 duty cycle initially

    def rotate_clockwise(self, duty):
        """
        rotate the dc motor clockwise with specified duty cycle
        :param duty: in percentage
        """
        self.pin2.ChangeDutyCycle(0)
        self.pin1.ChangeDutyCycle(duty)

    def rotate_counter_clockwise(self, duty):
        """
        rotate the dc motor counter clockwise with specified duty cycle
        :param duty: in percentage
        """
        self.pin1.ChangeDutyCycle(0)
        self.pin2.ChangeDutyCycle(duty)

    def set(self, value):
        """
        rotates the motor in the direction and with duty specified with value
        :param value: duty cycle can be positive or negative to determine the direction
        """
        abs_value = abs(value)
        abs_value = min(100, abs_value)  # duty cycle can't be more than 100

        # as per convention (clockwise for azimuth)
        if value >= 0: self.rotate_clockwise(abs_value)
        else: self.rotate_counter_clockwise(abs_value)

    def stop(self):
        """
        stop PWM
        """
        self.pin1.stop()
        self.pin2.stop()
