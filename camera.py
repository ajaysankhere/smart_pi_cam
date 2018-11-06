import imutils
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import os
import sys

class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiCamera()
        self.vs.resolution = (320, 240)
        self.vs.framerate = 30
        self.flip = flip
        self.rawCapture = PiRGBArray(self.vs, size=(320, 240))
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def get_frame(self):
        for frame in camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # frame = self.flip_if_needed(self.vs.read()).copy() 
            image = frame.array
            jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()

    def get_object(self, classifier):
        found_objects = False
        
        for frame in camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # frame = self.flip_if_needed(self.vs.read()).copy() 
            image = frame.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            objects = classifier.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            if len(objects) > 0:
                found_objects = True

            # Draw a rectangle around the objects
            for (x, y, w, h) in objects:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            ret, jpeg = cv2.imencode('.jpg', image)
            return (jpeg.tobytes(), found_objects)


