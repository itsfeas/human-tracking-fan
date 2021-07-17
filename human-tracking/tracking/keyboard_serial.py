# Code adapted from Tensorflow Object Detection Framework
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb
# Tensorflow Object Detection Detector

import time
import cv2
import serial
import numpy as np
# import tensorflow as tf

if __name__ == "__main__":
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM4'
    ser.open()
    if ser.is_open:
        print("serial connection initiated!")
    else:
        print("serial connection failed!")

    while True:
        cam_no = 0
        feed = cv2.VideoCapture(cam_no)
        r, img = feed.read()
        # img = cv2.resize(img, (1280, 720))
        height, width, channels = img.shape
        img = cv2.resize(img, (width//2, height//2))
        # width, height = width//4, height//4

        # Visualization of the results of a detection.
        pos_data = []
        while True:
            cv2.imshow("preview", img)
            key = cv2.waitKey(0)
            if key == ord('a'):
                ser.write("l03\n".encode())
            elif key == ord('d'):
                ser.write("r03\n".encode())
            elif key == ord('q'):
                break