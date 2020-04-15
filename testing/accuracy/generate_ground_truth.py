


from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils

from os import listdir
from os.path import isfile, join
from PIL import Image
from PIL import ImageDraw
from PIL import Image, ImageFont, ImageDraw
import argparse
import os
import cv2
import sys
sys.path.insert(0, os.environ['PROJECT_ROOT'])
from python_tools.common import mkdir, All_Day_Night, get_files, parse_xml_to_dict





def generate_drawings(images_folder, annotations_folder, output_folder):
    mkdir(output_folder)
    for image_name, annotation_name in zip(get_files(images_folder, sort=True), get_files(annotations_folder, sort=True)):
        img = Image.open(os.path.join(images_folder, image_name))
        im = img.copy()
        draw = ImageDraw.Draw(im)
        annotations = open(os.path.join(annotations_folder, annotation_name), "r")
        for line in annotations.readlines():
            l = line.split()
            draw.rectangle([float(l[1]), float(l[2]), float(l[3]), float(l[4])], outline="red")
            im.save(os.path.join(output_folder, image_name), "JPEG")




def resize_and_copy_images(src_folder, dst_folder, width, height):
    for image_name in get_files(src_folder):
        image_path = os.path.join(src_folder, image_name)
        img = cv2.imread(image_path)
        img_height, img_width, _ = img.shape
        border = (img_width - img_height) // 2
        #flip color representation
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #crop central square
        img = img[0 : img_height, border : border + img_height]
        #downscale resolution
        img = cv2.resize(img, (width, height))
        cv2.imwrite(os.path.join(dst_folder, image_name), img)



def generate_txts(src_folder, dst_folder, width, height):
    # private function
    def rescale(pos, or_size, new_size):
        return int((int(pos) / or_size) * new_size)

    for xml_name in get_files(src_folder):
        detections_file = open(os.path.join(dst_folder, xml_name[:-4]  + '.txt'), 'w+')
        data = parse_xml_to_dict(os.path.join(src_folder, xml_name))

        or_width, or_height = int(data['size']['width']), int(data['size']['height'])
        min_size = 10
        for obj in data['object']:
            start_x = (or_width - or_height) // 2
            xmin = int(obj['bndbox']['xmin']) - start_x
            xmax = int(obj['bndbox']['xmax']) - start_x

            if obj['name'] == 'bicycle' or xmin >= or_height - min_size or xmax <= 0 + min_size:
                continue 
            xmin = max(0, xmin)
            xmax = min(or_height - 1, xmax)

            xmin = rescale(xmin, or_height, width)
            ymin = rescale(obj['bndbox']['ymin'], or_height, height)
            xmax = rescale(xmax, or_height, width)
            ymax = rescale(obj['bndbox']['ymax'], or_height, height)

            #tmp
            name = obj['name']
            if name == 'truck':
                name = 'car'
            #tmp-end
            detections_file.write("{0} {1} {2} {3} {4} \n".format(name, xmin, ymin, xmax, ymax))
        detections_file.close()
            



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type = All_Day_Night, choices=list(All_Day_Night))
    parser.add_argument('--width', type = int)
    parser.add_argument('--height', type = int)
    args = parser.parse_args()

    testing_name = args.type.value + '_' + str(args.width) + 'x' + str(args.height)
    testing_folder = os.path.join(os.environ['LOCAL_GIT'], 'testing/exported', testing_name)



    # prepare testing tree
    dst_images_folder = os.path.join(testing_folder, 'images')
    dst_txts_folder = os.path.join(testing_folder, 'txts')
    mkdir(testing_folder)
    mkdir(dst_images_folder)
    mkdir(dst_txts_folder)

    # copy images
    src_data_folder = os.path.join(os.environ['LOCAL_GIT'], 'testing/data')

    if args.type is All_Day_Night.all_ or args.type is All_Day_Night.day:
        resize_and_copy_images(os.path.join(src_data_folder, 'day', 'images'), dst_images_folder, args.width, args.height)
        generate_txts(os.path.join(src_data_folder, 'day', 'xmls'), dst_txts_folder, args.width, args.height)


    if args.type is All_Day_Night.all_ or args.type is All_Day_Night.night:
        resize_and_copy_images(os.path.join(src_data_folder, 'night', 'images'), dst_images_folder, args.width, args.height)
        generate_txts(os.path.join(src_data_folder, 'night', 'xmls'), dst_txts_folder, args.width, args.height)

    if args.type is All_Day_Night.train:
        resize_and_copy_images(os.path.join(src_data_folder, 'train', 'images'), dst_images_folder, args.width, args.height)
        generate_txts(os.path.join(src_data_folder, 'train', 'xmls'), dst_txts_folder, args.width, args.height)   


    
    generate_drawings(dst_images_folder, dst_txts_folder, os.path.join(testing_folder, 'draw'))






