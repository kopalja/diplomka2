
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





def create_fold_structure(path, train):
    mkdir(path)
    mkdir(os.path.join(path, 'draw'))
    mkdir(os.path.join(path, 'images'))

    if train:
        mkdir(os.path.join(path, 'annotations'))
        mkdir(os.path.join(path, 'annotations', 'xmls'))
        return open(os.path.join(path, 'annotations', 'trainval.txt'), 'w+')
    else:
        mkdir(os.path.join(path, 'xmls'))
        return None



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

    draw_names = get_files(src_draw, sort = False)
    image_names = get_files(src_images, sort = False)
    xml_names = get_files(src_xmls, sort = False)
    fold_size = len(xml_names) // int(args.number_of_folds)

    if len(xml_names) != len(image_names) or len(draw_names) != len(image_names):
        raise Exception('wrong src. Not equeal number of xmls-draw-images') 
    
    for fold_index in range(int(args.number_of_folds)):
        fold_path = os.path.join(dst_dataset, 'fold_' + str(fold_index))
        train_path = os.path.join(fold_path, 'train')
        test_path = os.path.join(fold_path, 'test')

        mkdir(fold_path)
        trainval_file = create_fold_structure(train_path, train=True)
        create_fold_structure(test_path, train=False)
        mkdir(os.path.join(fold_path, 'model'))

        i, train_index, test_index = 0, 0, 0
        for draw_name, image_name, xml_name in zip(draw_names, image_names, xml_names):
            image_name = draw_name
            xml_name = draw_name[:-4] + '.xml'
            dst_path = None
            name_index = None
            annotation = None
            if i > fold_index * fold_size and i < (fold_index + 1) * fold_size:
                dst_path = test_path
                name_index = test_index
                test_index += 1
                annotation = False
            else:
                dst_path = train_path
                name_index = train_index
                train_index += 1
                annotation = True

            shutil.copy(os.path.join(src_draw, draw_name), os.path.join(dst_path, 'draw', "my_" + str(name_index).zfill(6) + ".jpg"))
            shutil.copy(os.path.join(src_images, image_name), os.path.join(dst_path, 'images', "my_" + str(name_index).zfill(6) + ".jpg"))

            if annotation:
                shutil.copy(os.path.join(src_xmls, xml_name), os.path.join(dst_path, 'annotations', 'xmls', "my_" + str(name_index).zfill(6) + ".xml"))
                trainval_file.write("my_" + str(name_index).zfill(6) + ".xml\n")
            else:
                shutil.copy(os.path.join(src_xmls, xml_name), os.path.join(dst_path, 'xmls', "my_" + str(name_index).zfill(6) + ".xml"))

            i += 1
        trainval_file.close()








