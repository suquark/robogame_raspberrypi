# coding : utf-8
__author__ = 'suquark'
import serial
import time
import re
from django.http import HttpResponse


class ServoCtl:
    def __init__(self):
        # self.lock = False
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

    def write_file(self, fpath):
        #if not self.lock:
            #self.lock = True
            f = open('action/' + fpath + '.txt')
            data = f.read()
            print 'Servo-Action Loaded'
            for line in data.splitlines():
                line = line.strip()
                self.write(line)
                time.sleep(float(re.sub(r'.*T', '', line))/1000.)
            #self.lock = False
