#!/usr/bin/env python2
import cv2
import os, sys
from os import path
from os.path import join

import numpy as np

MSE_THRESHOLD = 0.5
# threshold of mse value that will consider it as a duplicate.

if len(sys.argv) < 3:
    print "Usage: %s [input_dir] [output_dir]"
    print "Author: Kiyoon Kim (yoonkr33@gmail.com)"
    print "Remove the duplicates of videos."
    sys.exit()

input_dir = sys.argv[1]
output_dir = sys.argv[2]

if output_dir.endswith('/'):
    output_dir = output_dir[:-1]

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
            out_file = join(root.replace(input_dir, output_dir, 1), video)
            out_dir = os.path.dirname(out_file)
            print "(%d/%d) Generating to %s" % (i+j+1, total, out_file)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            cap = cv2.VideoCapture(in_file)
            ret, frame = cap.read()
            if not ret:
                raise Exception('Unable to read the video.')
            vid_writer = cv2.VideoWriter(out_file, fourcc, 25.0, (frame.shape[1],frame.shape[0]))
            vid_writer.write(frame)

            prev_frame = frame
            ret, frame = cap.read()
            while ret:
                if ((frame - prev_frame)**2).mean() > MSE_THRESHOLD:
                    vid_writer.write(frame)
                prev_frame = frame
                ret, frame = cap.read()
            cap.release()
            vid_writer.release()
        i += len(videos)

