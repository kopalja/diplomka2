

from os.path import isfile, join
from os import listdir
import os
import shutil
import argparse
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import tensorflow as tf
from lxml import etree
import sys
sys.path.insert(0, os.environ['PROJECT_ROOT'])
from python_tools.common import parse_xml_to_dict




def check_validation(data):
    x = 0
    if not 'object' in data:
        return False
    if len(data['object']) > 11:
        return False

    w = np.ones(1921)
    for obj in data['object']:
        if w[int(obj['bndbox']['xmin'])] == 0:
            #return False
            x += 1
        w[int(obj['bndbox']['xmin'])] = 0
    w = np.ones(1921)
    for obj in data['object']:
        if w[int(obj['bndbox']['xmax'])] == 0:
            #return False
            x += 1
        w[int(obj['bndbox']['xmax'])] = 0
    w = np.ones(1081)
    for obj in data['object']:
        if w[int(obj['bndbox']['ymin'])] == 0:
            #return False
            x += 1
        w[int(obj['bndbox']['ymin'])] = 0
    w = np.ones(1081)
    for obj in data['object']:
        if w[int(obj['bndbox']['ymax'])] == 0:
            #return False
            x += 1
        w[int(obj['bndbox']['ymax'])] = 0

    if x > 3:
        return False
    return True

#########################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=str)
    args = parser.parse_args()


    day_folder = os.pardir.join(args.root, 'day')
    night_folder = os.pardir.join(args.root, 'night')

    for category_root in [day_folder, night_folder]:

        draw_folder = os.path.join(category_root, 'draw')
        xmls_folder = os.path.join(category_root, 'xmls')

        xmls_name = sorted([f for f in listdir(xmls_folder) if isfile(join(xmls_folder, f))])
        for xml_name in xmls_name:
            draw_path = os.path.join(draw_folder, xml_name[:-4] + '.xml')
            xml_path = os.path.join(xmls_folder, xml_name)

            data = parse_xml_to_dict(xml_path)['annotation']   
            if check_validation(data) == False:
                os.remove(draw_folder)



