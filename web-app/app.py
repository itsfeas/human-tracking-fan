#!/usr/bin/env python
#from multiprocessing import Process
import time
import cv2
import serial
import numpy as np
import tensorflow.compat.v1 as tf
from flask import Flask, render_template, jsonify, request, Response
from py.detector import DetectorAPI

tf.disable_v2_behavior()
app = Flask(__name__)

global odapi
global engaged
# global ser
global feed
global serialOn

serialOn = False
engaged = True
MODEL_FOLDER = 'resources/'
# MODEL_NAME = './ssd_mobilenet_v3_large_coco_2020_01_14'
model_path = MODEL_FOLDER+'/frozen_inference_graph.pb'

odapi = DetectorAPI(path_to_ckpt=model_path)

if serialOn:
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM4'
    ser.open()
    if ser.is_open:
        print("serial connection initiated!")
    else:
        print("serial connection failed!")

cam_no = 0
feed = cv2.VideoCapture(cam_no)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/engageSwitch", methods=['POST'])
def engageSwitch():
    print(request.get_json())
    global engaged
    if request.method == 'POST':
        engaged = not engaged
        message = {'message': 'Switched!'}
        return jsonify(message)


@app.route("/left", methods=['GET'])
def left():
    global engaged, serialOn
    if request.method == 'GET' and not engaged and serialOn:
        message = {'message': 'Moved Left!'}
        shift_left();
        return jsonify(message)


@app.route("/right", methods=['GET'])
def right():
    global engaged, serialOn
    if request.method == 'GET' and not engaged and serialOn:
        message = {'message': 'Moved Right!'}
        shift_right();
        return jsonify(message)

@app.route("/video_feed")
def video_feed():
	return Response(run_fan(),
                 mimetype="multipart/x-mixed-replace; boundary=frame")


def shift_left():
    global serialOn
    if serialOn:
        global ser
        ser.write("l01\n".encode())


def shift_right():
    global serialOn
    if serialOn:
        global ser
        ser.write("r01\n".encode())


def run_fan():
    global odapi
    global feed
    global engaged
    global serialOn
    if serialOn:
        global ser

    threshold = 0.6
    shift = (0, 0)
    prev_pos = (0, 0)
    current_pos = (0, 0)
    vel_check = False
    while True:
        r, img = feed.read()
        # img = cv2.resize(img, (1280, 720))
        height, width, channels = img.shape
        # img = cv2.resize(img, (width//4, height//4))
        # width, height = width//4, height//4
        boxes, scores, classes, num = odapi.processFrame(img)

        # Visualization of the results of a detection.
        if engaged:
            for i in range(len(boxes)):
                # Class 1 represents human
                if classes[i] == 1 and scores[i] > threshold:
                    box = boxes[i]
                    center = ((box[1]+box[3])//2, (box[0]+box[2])//2)
                    # print(center)
                    radius = 50*(abs(box[1]-box[3]) + abs(box[0]-box[2]))//width
                    # print(radius)
                    cv2.circle(img, center, radius, (0, 0, 255), -1)
                    if vel_check:
                        prev_pos = (width//2, height//2)
                        calc_pos = center
                        shift = (calc_pos[0]-prev_pos[0],
                                calc_pos[1]-prev_pos[1])
                        
                        if shift[0] > 0:
                            if 100*abs(shift[0]/width) > 20:
                                prev_pos = current_pos
                                cv2.circle(img, prev_pos, 5, (255, 0, 0), -1)
                                current_pos = center
                                # print("human shifted right by",
                                #       100*abs(shift[0]/width), "%")
                                if serialOn:
                                    ser.write("r10\n".encode())
                            if 100*abs(shift[0]/width) > 10:
                                prev_pos = current_pos
                                cv2.circle(img, prev_pos, 5, (255, 0, 0), -1)
                                current_pos = center
                                # print("human shifted right by",
                                #       100*abs(shift[0]/width), "%")
                                if serialOn:
                                    ser.write("r03\n".encode())
                            elif 100*abs(shift[0]/width) > 2:
                                prev_pos = current_pos
                                cv2.circle(img, prev_pos, 5, (255, 0, 0), -1)
                                current_pos = center
                                # print("human shifted left by",
                                #       100*abs(shift[0]/width), "%")
                                if serialOn:
                                    ser.write("r01\n".encode())
                        elif shift[0] < 0:
                            if 100*abs(shift[0]/width) > 20:
                                prev_pos = current_pos
                                cv2.circle(img, prev_pos, 5, (255, 0, 0), -1)
                                current_pos = center
                                # print("human shifted right by",
                                #       100*abs(shift[0]/width), "%")
                                if serialOn:
                                    ser.write("l10\n".encode())
                            if 100*abs(shift[0]/width) > 10:
                                prev_pos = current_pos
                                cv2.circle(img, prev_pos, 5, (255, 0, 0), -1)
                                current_pos = center
                                # print("human shifted left by",
                                #       100*abs(shift[0]/width), "%")
                                if serialOn:
                                    ser.write("l03\n".encode())
                            elif 100*abs(shift[0]/width) > 2:
                                prev_pos = current_pos
                                cv2.circle(img, prev_pos, 5, (255, 0, 0), -1)
                                current_pos = center
                                # print("human shifted left by",
                                #       100*abs(shift[0]/width), "%")
                                if serialOn:
                                    ser.write("l01\n".encode())
                    else:
                        prev_pos = center
                        current_pos = center
                        vel_check = True

        # cv2.imshow("preview", img)
        r, encoded = cv2.imencode(".jpg", img)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encoded) + b'\r\n')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
