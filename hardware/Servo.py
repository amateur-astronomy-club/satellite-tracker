import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# constants
SERVO_FREQUENCY = 50  # typical rate as per data-sheet
MIN_WIDTH = 500.0  # pulse width in us. From data-sheet for servo. Corrected to map to 0 deg
MAX_WIDTH = 2400.0  # pulse width in us. From data-sheet for servo. Corrected to map to 180 deg

MIN_DUTY = MIN_WIDTH/SERVO_FREQUENCY/10  # min duty cycle in percentage
MAX_DUTY = MAX_WIDTH/SERVO_FREQUENCY/10  # max duty cycle in percentage

assert MIN_DUTY >= 0  # duty cycle cannot be less than 0%
assert MAX_DUTY <= 100  # duty cycle cannot be more than 100%


class Servo:
    """
    Class to control servo motor.
    The servo control the elevation of the pointer.
    """
    def __init__(self, pin):
        """
        setup the PWM pin
        :param pin: pin to use
        """
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, SERVO_FREQUENCY)

    def start(self):
        """
        start PWM
        """
        self.pwm.start(MIN_DUTY)

    def set(self, angle):
        """
        set servo angle
        :param angle: angle to be set in deg (0 - 180 deg)
        """
        #  map angle between 0 to 180
        angle = max(0, angle)
        angle = min(180, angle)

        duty = MIN_DUTY + float(angle)/180*(MAX_DUTY - MIN_DUTY)
        self.pwm.ChangeDutyCycle(duty)

    def stop(self):
        """
        stop PWM
        """
        self.pwm.stop()

