# -*- coding: utf-8 -*-
import time
import cv2

class Face:
    def __init__(self, debug):
        self.cascade = cv2.CascadeClassifier('./haar.xml');
        self.camera = cv2.VideoCapture(0)
        self.is_error = 0;
        if self.camera.isOpened() is False:  # check if we succeeded
            self.is_error = 1;

        self.cur_interval = 0
        
        #self.camera.Device()
        #self.camera.set(1,10000)
        #self.camera.set(4,1024)
        #self.camera.set(15, -8.0);
        self.debug = debug

    def __detect(self, image):
        small = cv2.resize(image, (0,0), fx=0.2, fy=0.2) 
        faces = self.cascade.detectMultiScale(small, 1.2, 1);
        is_face = False
        for (x, y, w, h) in faces:
            is_face = True
            cv2.rectangle(image, (x*5, y*5), ( (x+w)*5, (y+h)*5 ), (0, 0, 255), 2)

        if self.debug is True:
            cv2.imshow('face', image)
            if cv2.waitKey(10) == 0x1b:
                return is_face
        return is_face

    def read(self):
        try:
            i = 50
            while i:
                _, frame = self.camera.read()
                i -= 1
        except:
            print('Error!')
        is_face = self.__detect(frame)

        return is_face
