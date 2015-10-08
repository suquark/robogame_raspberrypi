import serial
import numpy as np
import time
import os
import cv2
import imaging
from servoctl import ServoCtl
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
# ttyACM0

from django.conf.urls import include, url
# from django.contrib import admin

ser = ServoCtl()


def servoctl(requests, str0):
    return HttpResponse(ser.write(str0))


def welcome(request):
    return HttpResponse('<html><script>alert("Hello");</script></html>')


def camera(request):
    os.system("fswebcam -d /dev/video0 -r 1600*1200 --no-banner --no-timestamp /home/pi/webcam.bmp")
    wrapper = FileWrapper(open("/home/pi/webcam.bmp", "rb"))
    return HttpResponse(wrapper, "image/jpeg")


def process_image():
    myimg = cv2.imread("/home/pi/webcam.bmp")
    image = cv2.cvtColor(myimg, cv2.COLOR_RGB2GRAY)
    # w=img.shape[1]
    # h=img.shape[0]
    # newimg=np.zeros((h,w),np.uint8)
    # image=cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,2)
    cv2.threshold(image, 140, 255, 0, image)
    cv2.imwrite("/home/pi/image_threshold.bmp", image)
    imaging.clipResizeImg("/home/pi/image_threshold.bmp", 24, 24).save("/home/pi/image_resize.bmp")


def camera_tiny(request):
    os.system("fswebcam -d /dev/video0 -r 1600*1200 --no-banner --no-timestamp /home/pi/webcam.bmp")
    process_image();
    wrapper = FileWrapper(open("/home/pi/image_resize.bmp", "rb"))
    return HttpResponse(wrapper, "image/jpeg")


def camera_digital(request):
    os.system("fswebcam -d /dev/video0 -r 1600*1200 --no-banner --no-timestamp /home/pi/webcam.bmp")
    process_image();
    myimg = cv2.imread("/home/pi/image_resize.bmp")

    w = myimg.shape[1]
    h = myimg.shape[0]
    newimg = np.zeros((h, w), np.uint8)
    iTmp = cv2.CreateImage(size, image.depth, 1)
    for i in range(image.height):
        for j in range(image.width):
            iTmp[i, j] = 255 - image[i, j]

    print str(myimg)

    return HttpResponse(str(myimg))





urlpatterns = [
    url(r'^servoctl/(?P<str0>\S+)', servoctl),
    url(r'^welcome', welcome),
    url(r'^camera$', camera),
    url(r'^camera_tiny$', camera_tiny),
    url(r'^camera_digital$', camera_digital),
]
