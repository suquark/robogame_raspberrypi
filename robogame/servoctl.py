__author__ = 'suquark'
import serial
from django.http import HttpResponse


class ServoCtl:
    def __init__(self):
        self.ser = None
        try:
            self.ser = serial.Serial("/dev/ttyACM0", 115200)
        except Exception, e:
            print 'Error: No Servo Found'

    def write(self, str0):
        if self.ser is None:
            try:
                self.ser = serial.Serial("/dev/ttyACM0", 115200)
            except Exception, e:
                print 'Error: No Servo Found'
        n = self.ser.write(str0.replace("_", "#") + "\r\n")
        return 'Servoctl - %d bytes write.' % n
