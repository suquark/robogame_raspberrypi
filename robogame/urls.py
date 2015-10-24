import serial
import numpy as np
import time
import os
import cv2
import imaging
from servoctl import ServoCtl
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import unused.OCR2 as OCR
import camctl
import multiprocessing
# ttyACM0

from django.conf.urls import include, url
# from django.contrib import admin

print 'Setting Camera...'
cameractl = camctl.CameraCtl()
print 'Starting ServoCtl...'
ser = ServoCtl()
print 'Connecting to OCR_Azure_Server...'
ocr_host = None#OCR.OnlineOCR()


def servoctl(requests, str0):
    return HttpResponse(ser.write(str0))


def servoctl_trans(fpath):
    print 'Trans..'
    ser.write_file(fpath)

def servoctl_file(requests, fpath):
    # p = multiprocessing.Process(target=servoctl_trans, args=fpath)
    # p.start()
    servoctl_trans(fpath)
    return HttpResponse('New process started.')


def welcome(request):
    return HttpResponse('<html><script>alert("Hello");</script></html>')


def camera(request):
    cameractl.snapshot()
    wrapper = FileWrapper(open(cameractl.path, "rb"))
    return HttpResponse(wrapper, "image/jpeg")


def ocr(request):
    cameractl.snapshot()
    return HttpResponse(ocr_host.recg(cameractl.path))


def process_image():
    myimg = cv2.imread(cameractl.path)
    image = cv2.cvtColor(myimg, cv2.COLOR_RGB2GRAY)
    # w=img.shape[1]
    # h=img.shape[0]
    # newimg=np.zeros((h,w),np.uint8)
    # image=cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,2)
    cv2.threshold(image, 140, 255, 0, image)
    cv2.imwrite("/home/pi/image_threshold.bmp", image)
    imaging.clipResizeImg("/home/pi/image_threshold.bmp", 24, 24).save("/home/pi/image_resize.bmp")


def camera_tiny(request):
    cameractl.snapshot()
    process_image()
    wrapper = FileWrapper(open("/home/pi/image_resize.bmp", "rb"))
    return HttpResponse(wrapper, "image/jpeg")


def camera_digital(request):
    cameractl.snapshot()
    process_image()
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
    url(r'^welcome', welcome),
    url(r'^servoctl_file/(?P<fpath>\S+)', servoctl_file),
    url(r'^servoctl/(?P<str0>\S+)', servoctl),
    url(r'^ocr$', ocr),
    url(r'^camera$', camera),
    url(r'^camera_tiny$', camera_tiny),
    url(r'^camera_digital$', camera_digital),
]
