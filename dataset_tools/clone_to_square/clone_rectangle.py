
from os.path import isfile, join
from os import listdir
import os
import shutil
import argparse
import cv2
from PIL import Image
import tensorflow as tf
from lxml import etree


def process_image(image_path, base):
    im = cv2.imread(image_path, 1)
    height = im.shape[0]
    return \
        im[0 : height, base[0] : base[0] + height], \
        im[0 : height, base[1] : base[1] + height], \
        im[0 : height, base[2] : base[2] + height]
    

def create_xml(source_xml_path, x_start):
    with tf.gfile.GFile(source_xml_path, 'r') as fid:
        xml_str = fid.read()
    xml = etree.fromstring(xml_str)

    height = int(xml[1][1].text)
    min_size = 0
    for child in xml:
        if child.tag == 'size':
            child[0].text = str(height)
        elif child.tag == 'object':
            new_xmin = int(child[4][0].text) - x_start
            new_xmax = int(child[4][2].text) - x_start
            # object is not in the new frame
            if new_xmax < 0 + min_size:
                xml.remove(child)
            elif new_xmin >= height - min_size:
                xml.remove(child)
            else:
                # remap coordinates to new base
                child[4][0].text = str(max(1, new_xmin))
                child[4][2].text = str(min(new_xmax, height))
    if len(xml) == 2:
        return None
    return xml

def process_xml(xml_path, base):
    return create_xml(xml_path, base[0]), create_xml(xml_path, base[1]), create_xml(xml_path, base[2]) 


def generate_data(src_img, src_xml, dst_img, dst_xml, width = 1920, height = 1080):
    base = [0, int(width / 2 - height / 2), width - height]
    name_index = len([f for f in listdir(dst_xml) if isfile(join(dst_xml, f))])
    for image_name in [f for f in listdir(src_img) if isfile(join(src_img, f))]:
        name = 'my_' + str(name_index).zfill(6)
        
        images = process_image(os.path.join(src_img, image_name), base)
        xmls = process_xml(os.path.join(src_xml, image_name[:-4] + '.xml'), base)
        for image, xml in zip(images, xmls):
            if xml ==  None:
                continue
            # create new examples
            name = 'my_' + str(name_index).zfill(6)
            cv2.imwrite(os.path.join(dst_img, name + '.jpg'), image)
            file = open(os.path.join(dst_xml, name + '.xml'), 'wb+')
            st = etree.tostring(xml, pretty_print = True)
            file.write(st)
            file.close()
            name_index += 1

 




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ffrom', type=str)
    parser.add_argument('--to', type=str)
    args = parser.parse_args()


    for t in ['day', 'night']:
        src_images = os.path.join(args.ffrom, t, 'images')
        src_xmls = os.path.join(args.ffrom, t, 'xmls')
        dst_images = os.path.join(args.to, t, 'images')
        dst_xmls = os.path.join(args.to, t, 'xmls')
        generate_data(src_images, src_xmls, dst_images, dst_xmls)





    
