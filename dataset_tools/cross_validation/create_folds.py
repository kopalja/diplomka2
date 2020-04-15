
from os.path import isfile, join
from os import listdir
import os
import shutil
import argparse
import numpy as np
from PIL import Image, ImageFont, ImageDraw

import sys
sys.path.insert(0, os.environ['PROJECT_ROOT'])
from python_tools.common import get_files, mkdir





def create_fold_structure(path):
    mkdir(path)
    mkdir(os.path.join(path, 'draw'))
    mkdir(os.path.join(path, 'images'))
    mkdir(os.path.join(path, 'xmls'))





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_dataset', type=str, required = True)
    parser.add_argument('--number_of_folds', type=str, required = True)
    parser.add_argument('--dst_name', type=str, required = True)
    args = parser.parse_args()

    src_draw = os.path.join(args.src_dataset, 'draw')
    src_images = os.path.join(args.src_dataset, 'images')
    src_xmls = os.path.join(args.src_dataset, 'annotations', 'xmls')
    dst_dataset = os.path.join(os.environ['LOCAL_GIT'], 'dataset', 'exported', 'folds', args.dst_name) 
    mkdir(dst_dataset)

    draw_names = get_files(src_draw, sort = True)
    image_names = get_files(src_images, sort = True)
    xml_names = get_files(src_xmls, sort = True)
    fold_size = len(xml_names) // int(args.number_of_folds)

    if len(xml_names) != len(image_names) or len(draw_names) != len(image_names):
        raise Exception('wrong src. Not equeal number of xmls-draw-images') 
    
    for fold_index in range(int(args.number_of_folds)):
        fold_path = os.path.join(dst_dataset, 'fold_' + str(fold_index))
        train_path = os.path.join(fold_path, 'train')
        test_path = os.path.join(fold_path, 'test')

        mkdir(fold_path)
        create_fold_structure(train_path)
        create_fold_structure(test_path)
        mkdir(os.path.join(fold_path, 'model'))

        i, train_index, test_index = 0, 0, 0
        for draw_name, image_name, xml_name in zip(draw_names, image_names, xml_names):
            dst_path = None
            name_index = None
            if i > fold_index * fold_size and i < (fold_index + 1) * fold_size:
                dst_path = test_path
                name_index = test_index
                test_index += 1
            else:
                dst_path = train_path
                name_index = train_index
                train_index += 1

            shutil.copy(os.path.join(src_draw, draw_name), os.path.join(dst_path, 'draw', "my_" + str(name_index).zfill(6) + ".jpg"))
            shutil.copy(os.path.join(src_images, image_name), os.path.join(dst_path, 'images', "my_" + str(name_index).zfill(6) + ".jpg"))
            shutil.copy(os.path.join(src_xmls, xml_name), os.path.join(dst_path, 'xmls', "my_" + str(name_index).zfill(6) + ".xml"))
            i += 1










