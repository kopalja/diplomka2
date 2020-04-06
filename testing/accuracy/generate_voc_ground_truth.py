

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














def test_xml(xml_path, searching_objects, new_width, new_height):
    # private function
    def base_coordinates(mmin, mmax, size, new_size):
        dx = (new_size - (mmax - mmin)) // 2
        or_min = mmin
        or_max = mmax
        mmin -= dx
        mmax = mmin + new_size
        if mmin < 0:
            tmp = -mmin
            mmin += tmp
            mmax += tmp
        elif mmax > size:
            tmp = mmax - size
            or_tmp = tmp
            mmin -= tmp
            mmax -= tmp
            if mmin < 0:
                raise Exception('mmin < 0. Tgis should not happen')
        return mmin, mmax

    data = parse_xml_to_dict(xml_path)
    if (int(data['size']['width']) < new_width) or (int(data['size']['height']) < new_height):
        return False, []
    
    x_min, y_min, x_max, y_max = 1000, 1000, 0, 0
    interesting_object_exist = False

    for obj in data['object']:
        if obj['name'] in searching_objects:
            interesting_object_exist = True
            x_min = min(x_min, int(obj['bndbox']['xmin']))
            y_min = min(y_min, int(obj['bndbox']['ymin']))
            x_max = max(x_max, int(obj['bndbox']['xmax']))
            y_max = max(y_max, int(obj['bndbox']['ymax']))

    if interesting_object_exist and (x_max - x_min <= new_width) and (y_max - y_min <= new_height):
        x_min, x_max = base_coordinates(x_min, x_max, int(data['size']['width']), new_width)
        y_min, y_max = base_coordinates(y_min, y_max, int(data['size']['height']), new_height)
        return True, [x_min, y_min, x_max, y_max]
    return False, []



def resize_and_copy_image(src_image, dst_image, coordinates):
    img = cv2.imread(src_image)
    img = img[coordinates[1] : coordinates[3], coordinates[0] : coordinates[2]]
    cv2.imwrite(dst_image, img)



def generate_txt(src_xml, dst, coordinates, searching_objects):
    detections_file = open(dst, 'w+')
    data = parse_xml_to_dict(src_xml)

    or_width, or_height = int(data['size']['width']), int(data['size']['height'])
    min_size = 10
    for obj in data['object']:
        if not obj['name'] in searching_objects:
            continue

        name = obj['name']
        if name == "bus":
            name = "truck"

        xmin = int(obj['bndbox']['xmin']) - coordinates[0]
        xmax = int(obj['bndbox']['xmax']) - coordinates[0]
        ymin = int(obj['bndbox']['ymin']) - coordinates[1]
        ymax = int(obj['bndbox']['ymax']) - coordinates[1]
        detections_file.write("{0} {1} {2} {3} {4} \n".format(name, xmin, ymin, xmax, ymax))
    detections_file.close()
        

            



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--type', type = All_Day_Night, choices=list(All_Day_Night))
    parser.add_argument('--width', type = int)
    parser.add_argument('--height', type = int)
    args = parser.parse_args()


    voc_folder = os.path.join(os.environ['LOCAL_GIT'], 'testing', 'VOC2012')
    dst_folder = os.path.join(os.environ['LOCAL_GIT'], 'testing/exported', 'voc_' + str(args.width) + 'x' + str(args.height))

    xmls_folder = os.path.join(voc_folder, 'Annotations')
    images_folder = os.path.join(voc_folder, 'JPEGImages')


    # prepare testing tree
    dst_images_folder = os.path.join(dst_folder, 'images')
    dst_txts_folder = os.path.join(dst_folder, 'txts')
    mkdir(dst_folder)
    mkdir(dst_images_folder)
    mkdir(dst_txts_folder)

    searching_objects = ["bus", "car", "motorbike", "truck"]


    i = 0
    for xml_name in get_files(xmls_folder):
        name = xml_name[:-4]
        xml_path = os.path.join(xmls_folder, xml_name)
        passed, coordinates = test_xml(xml_path, searching_objects, args.width, args.height)
        if passed:
            resize_and_copy_image(os.path.join(images_folder, name + ".jpg"), os.path.join(dst_images_folder, name + ".jpg"), coordinates)
            generate_txt(xml_path, os.path.join(dst_txts_folder, name + ".txt"), coordinates, searching_objects)

            
    generate_drawings(dst_images_folder, dst_txts_folder, os.path.join(dst_folder, 'draw'))

















