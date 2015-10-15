import re
import serial


class DistanceSensorService:
    def __init__(self, com_port='COM1'):
        self.serial_port = serial.Serial(com_port, 115200)

    def open(self):
        self.serial_port.open()

    def get_distance_cm(self):
        try:
            serial_data = str(self.serial_port.readline(), 'ascii')

            # Regex Matches [Distance: XXX.XX]
            match = re.search('\[Distance:(\d+\.\d+)\]', serial_data)

            if match:
                return match.group(1)
            else:
                return None
        except serial.SerialException:
            return None

    def close(self):
        self.serial_port.close()

    def __del__(self):
        self.close()
