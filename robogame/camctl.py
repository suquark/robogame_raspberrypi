__author__ = 'suquark'
import os
class CameraCtl:
    def __init__(self):
        self.path = '/home/pi/webcam.bmp'

    def snapshot(self):
        os.system("fswebcam -d /dev/video0 -r 1600*1200 --no-banner --no-timestamp " + self.path)
