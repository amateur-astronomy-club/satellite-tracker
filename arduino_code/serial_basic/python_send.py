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
                break

        if port_loc is None:
            raise Exception("Arduino not found.")

        self.arduino = serial.Serial(port_loc)

    @staticmethod
    def convert_to_999(angle):
        if angle < 0 or angle > 180: raise ValueError


        value_999 = int(angle)

        out = str(value_999)

        while len(out) < 3:
            out = '0' + out

        return out

    def send(self, angle1, angle2):
        self.arduino.write(Sender.convert_to_999(angle1) + Sender.convert_to_999(angle2) + '!')

    def end(self):

        self.arduino.close()

