
import time

import argparse
import platform
import subprocess
from os.path import isfile, join, isdir
from os import listdir
from PIL import Image
from PIL import ImageDraw
import cv2

from os.path import isfile, join
from os import listdir
import os
import shutil
import numpy as np
import  ffmpeg 
import sys
sys.path.insert(0, os.environ['PROJECT_ROOT'])
from python_tools.functions import mkdir



def check_rotation(path_video_file):
    # this returns meta-data of the video file in form of a dictionary
    meta_dict = ffmpeg.probe(path_video_file)

    # from the dictionary, meta_dict['streams'][0]['tags']['rotate'] is the key
    # we are looking for
    rotateCode = None
    rotate = meta_dict.get('streams', [dict(tags=dict())])[0].get('tags', dict()).get('rotate', 0)
    if rotate == 0:
        return None

    if int(meta_dict['streams'][0]['tags']['rotate']) == 90:
        rotateCode = cv2.ROTATE_90_CLOCKWISE
    elif int(meta_dict['streams'][0]['tags']['rotate']) == 180:
        rotateCode = cv2.ROTATE_180
    elif int(meta_dict['streams'][0]['tags']['rotate']) == 270:
        rotateCode = cv2.ROTATE_90_COUNTERCLOCKWISE

    return rotateCode

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=str)
    parser.add_argument('--batch_name', type=str)
    parser.add_argument('--frame', type=int, default=300)
    args = parser.parse_args()


    output_root = os.path.join(os.environ['LOCAL_GIT'], 'dataset', 'processed', args.batch_name)
    tmp_day = os.path.join(output_root, "tmp_day")
    tmp_night = os.path.join(output_root, "tmp_night")

    mkdir(tmp_day, force = True)
    mkdir(tmp_night, force = True)


    categories = [f for f in listdir(args.root) if isdir(join(args.root, f))]


    index = 0
    for category in categories:
        videos_folder = os.path.join(args.root, category)
        videos_names = [f for f in listdir(videos_folder) if isfile(join(videos_folder, f))]



        for video in videos_names:
            video_path = os.path.join(videos_folder, video)

            #print(video_path)
            vidcap = cv2.VideoCapture(video_path)
            rotateCode = check_rotation(video_path)
            i = 0
            success = True
            while success:
                success, img = vidcap.read()
                i += 1
                if not success:
                    break

                if rotateCode is not None:
                    img = cv2.rotate(img, rotateCode) 

                if i % args.frame == 0:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
                    image = Image.fromarray(img)
                    image_name = "my_" + str(index).zfill(6) + ".jpg"

                    gray_image = Image.fromarray(img).convert('LA')
                    gray_array = np.asarray(gray_image)
                    if np.mean(gray_array) > 164:
                        image.save(tmp_day + '/' + image_name)
                    else:
                        image.save(tmp_night + '/' + image_name)
                    index += 1


