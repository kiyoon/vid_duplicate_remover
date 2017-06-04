#!/usr/bin/env python2
import cv2
import os, sys
from os import path
from os.path import join

import numpy as np

MSE_THRESHOLD = 0.5
# threshold of mse value that will consider it as a duplicate.

if len(sys.argv) < 2:
    print "Usage: %s [input_dir]"
    print "Author: Kiyoon Kim (yoonkr33@gmail.com)"
    print "Remove the duplicates of videos."
    sys.exit()

input_dir = sys.argv[1]


i = 0
total = 0
for root, dirs, files in os.walk(input_dir):
    videos = filter(lambda x: x.lower().endswith('.avi') or x.lower().endswith('.mp4'), files)
    total += len( videos)

if cv2.__version__[0] == '2':
    fourcc = cv2.cv.CV_FOURCC(*'HFYU')  # Huffman lossless
else:
    fourcc = cv2.FOURCC(*'HFYU')

for root, dirs, files in os.walk(input_dir):
    videos = filter(lambda x: x.lower().endswith('.avi') or x.lower().endswith('.mp4'), files)
    if len(videos) > 0:
        videos = sorted(videos)
        for j, video in enumerate(videos): 
            in_file = join(root, video)
            cap = cv2.VideoCapture(in_file)
            ret, frame = cap.read()
            if not ret:
                raise Exception('Unable to read the video.')
            cap.release()


