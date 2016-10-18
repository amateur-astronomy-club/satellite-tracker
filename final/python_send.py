import serial
import serial.tools.list_ports


class Sender:
    def __init__(self):
        try:
            self.arduino.close()
        except:
            pass

        ports = list(serial.tools.list_ports.comports())

        port_loc = None

        for p in ports:
            if "2341" in p[2].lower():
                port_loc = p[0]

                print "Arduino Found!"
                break

        if port_loc is None:
            raise Exception("Arduino not found.")

        self.arduino = serial.Serial(port_loc)

        print "Connected to Arduino"

        self.last_az = 0
        self.greater_than_180 = False

    def convert_to_999(self, angle):

        value_999 = int(angle)
        out = str(value_999)

        while len(out) < 3:
            out = '0' + out

        return out

    def process_data(self, alt, az):
        angle_per_step = 1.8

        """
        map to servo coordinates
        :param alt:
        :param az:
        :return:
        """
        alt *= -1
        alt += 90
        alt %= 360

        az *= -1
        az_out = 0
        if abs(az - self.last_az) >= 1.8:
            az_out = int((az - self.last_az) / angle_per_step)
            self.last_az += az_out * angle_per_step

        if alt >= 180 and not self.greater_than_180:
            self.greater_than_180 = True
            az_out = 180 / angle_per_step

        if alt < 180 and self.greater_than_180:
            self.greater_than_180 = False
            az_out = -180 / angle_per_step

        az_out += 400
        return (alt % 180), az_out

    def send(self, alt, az):
        value1, value2 = self.process_data(alt, az)
        string_send = self.convert_to_999(value1) + self.convert_to_999(value2) + '!'
        print "String Send: ", string_send
        self.arduino.write(string_send)
        # print "Value received from arduino: ", self.arduino.read(5)
        print "Send values to Arduino"

    def end(self):
        self.arduino.close()
