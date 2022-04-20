from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import imutils
import time
import cv2
import os
import urllib.request
import numpy as np
from django.conf import settings
import os

prototxtPath = os.path.join(
    settings.BASE_DIR, "face_detector", "deploy.prototxt")

weightsPath = os.path.join(
    settings.BASE_DIR, "face_detector", "res10_300x300_ssd_iter_140000.caffemodel")
faceNet = cv2.dnn.readNetFromCaffe(prototxtPath, weightsPath)


class Detect(object):
    def __init__(self):
        self.vs = VideoStream(src=0).start()

    def __del__(self):
        self.vs.stop()

    def detect(self, frame, faceNet):

        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                     (104.0, 177.0, 123.0))

        faceNet.setInput(blob)
        detections = faceNet.forward()

        faces = []
        locs = []

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.5:

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                text = "{:.2f}%".format(confidence * 100)
                if (startY - 10) > 10:
                    y = (startY - 10)
                else:
                    y = (startY + 10)
                cv2.rectangle(frame, (startX, startY),
                              (endX, endY), (0, 0, 255), 2)
                cv2.putText(frame, text, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

                locs.append((startX, startY, endX, endY))

        return locs

    def get_frame(self):
        frame = self.vs.read()
        frame = imutils.resize(frame, width=650)
        frame = cv2.flip(frame, 1)

        locs = self.detect(frame, faceNet)

        for box in locs:
            (startX, startY, endX, endY) = box

            cv2.rectangle(frame, (startX, startY),
                          (endX, endY), (255, 0, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes(), locs
