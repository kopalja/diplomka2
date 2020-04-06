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
from python_tools.common import mkdir, get_files


image_width = 960
image_height = 540
name_index = 0


test_image = "/home/kopi/local_git/testing/detrac/train/images/MVI_20011/img00001.jpg"


class Box:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.compute_center()
        self.left = None
        self.right = None

    def compute_center(self):
        self.x_center = (self.x_max + self.x_min) // 2
        self.y_center = (self.y_max + self.y_min) // 2

    def crop(self, box):
        if self.left != None:
            self.left.crop(box)
            self.right.crop(box)
            return
        
        if self.x_center > box.x_center:
            if self.y_center > box.y_center:
                self.left = Box(max(self.x_min, box.x_max), self.y_min, self.x_max, self.y_max)
                self.right = Box(self.x_min, max(self.y_min, box.y_max), self.x_max, self.y_max)
            else:
                self.left = Box(max(self.x_min, box.x_max), self.y_min, self.x_max, self.y_max)
                self.right = Box(self.x_min, self.y_min, self.x_max, min(self.y_max, box.y_min))
        else:
            if self.y_center > box.y_center:
                self.left = Box(self.x_min, self.y_min, min(self.x_max, box.x_min), self.y_max)
                self.right = Box(self.x_min, max(self.y_min, box.y_max), self.x_max, self.y_max)
            else:
                self.left = Box(self.x_min, self.y_min, min(self.x_max, box.x_min), self.y_max)
                self.right = Box(self.x_min, self.y_min, self.x_max, min(self.y_max, box.y_min))
        self.compute_center()

    def get_best(self):
        if self.left != None:
            score_l, box_l = self.left.get_best()
            score_r, box_r = self.right.get_best()
            if score_l > score_r:
                return score_l, box_l
            else:
                return score_r, box_r

        return (self.x_max - self.x_min) * (self.y_max - self.y_min), self



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


def load_xml(xml_path):
    import tensorflow as tf
    from lxml import etree
    with tf.gfile.GFile(xml_path, 'rb') as fid:
        xml_str = fid.read()
    xml = etree.fromstring(xml_str)
    return xml   



def compute_frame_window(node):
    frame = Box(0, 0, image_width, image_height)
    # img = Image.open(test_image)
    # img = img.copy()
    # draw = ImageDraw.Draw(img)
    for box in node:
        box = [float(box.attrib["left"]), float(box.attrib["top"]), float(box.attrib["left"]) + float(box.attrib["width"]), float(box.attrib["top"]) + float(box.attrib["height"])]
        frame.crop(Box(*[round(t) for t in box]))
        #draw.rectangle([box[0], box[1], box[2] + 3, box[3]], outline="red")
        #break

    _, frame = frame.get_best()
    return frame
    #return frame.x_min, frame.y_min, frame.x_max, frame.y_max
    # draw.rectangle([frame.x_min, frame.y_min, frame.x_max, frame.y_max],  outline="blue")
    # img.show()
    


def parse_frame(node, frame, width, height):
    records = []
    for target in node[0]: 
        box = target[0].attrib
        atr = target[1].attrib

        if len(target) != 2:
            continue

        name = atr["vehicle_type"]
        if name == "van":
            name = "car"
        elif name == "bus":
            name = "truck"

        x_min = int(max(0, float(box["left"]) - frame.x_min))
        x_max = int(min(width, float(box["left"]) + float(box["width"]) - frame.x_min))
        y_min = int(max(0, float(box["top"]) - frame.y_min))
        y_max = int(min(height, float(box["top"]) + float(box["height"]) - frame.y_min))

        if len(target) != 2 or (name != "car" and name != "truck") or x_max < 10 or y_max < 10 or x_min >= width - 10 or y_min >= height - 10:
            continue
        records.append([name, x_min, y_min, x_max, y_max])

    return records






def process_detrac_xml(xml_path, width, height, folders, name_index):
    root = load_xml(xml_path)
    image_index = 0
    frame = None
    for node in root:
        if node.tag == "ignored_region":
            frame = compute_frame_window(node)
            # frame is too small
            if frame.x_max - frame.x_min < width or frame.y_max - frame.y_min < height:
                break
            else:
                # recompute frame possition
                frame.x_min = frame.x_center - (width // 2)
                frame.x_max = frame.x_min + width
                frame.y_min = frame.y_center - (height // 2)
                frame.y_max = frame.y_min + height 
        elif node.tag == "frame":
            image_index += 1
            if image_index % 100 == 5:
                records = parse_frame(node, frame, width, height)
                if len(records) > 0:
                    create_testing_sample(frame, records, width, height, folders, image_index, name_index)
                    name_index += 1

    return name_index


def create_testing_sample(frame, records, width, height, folders, image_index, name_index):
    # create image
    img_name = "img" + str(image_index).zfill(5) + ".jpg"
    #print(os.path.join(folders[0], img_name))
    img = cv2.imread(os.path.join(folders[0], img_name))
    img = img[frame.y_min : frame.y_max, frame.x_min : frame.x_max]
    cv2.imwrite(os.path.join(folders[2], str(name_index).zfill(8) + '.jpg'), img)

    #create txt
    detections_file = open(os.path.join(folders[3], str(name_index).zfill(8) + '.txt'), 'w+')
    for record in records:
        detections_file.write("{0} {1} {2} {3} {4} \n".format(*record))
    detections_file.close()







if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type = int, default=300)
    parser.add_argument('--height', type = int, default=300)
    args = parser.parse_args()



    src_folder = os.path.join(os.environ['LOCAL_GIT'], 'testing', 'detrac', 'train')
    src_xmls_folder = os.path.join(src_folder, 'xmls')
    src_images_folder = os.path.join(src_folder, 'images')

    dst_folder = os.path.join(os.environ['LOCAL_GIT'], 'testing', 'exported', 'detrac_' + str(args.width) + "x" + str(args.height))
    dst_images_folder = os.path.join(dst_folder, 'images')
    dst_txts_folder = os.path.join(dst_folder, 'txts')
    dst_draw_folder = os.path.join(dst_folder, 'draw')
    mkdir(dst_folder)
    mkdir(dst_images_folder)
    mkdir(dst_txts_folder)
    mkdir(dst_draw_folder)


    # folde paths
    folders = [src_images_folder, src_xmls_folder, dst_images_folder, dst_txts_folder]

    name_index = 0
    for xml_name in get_files(src_xmls_folder, sort=True):
        name = xml_name[:-4]
        folders[0] = os.path.join(src_images_folder,  name)
        xml_path = os.path.join(src_xmls_folder, xml_name)
        name_index = process_detrac_xml(xml_path, args.width, args.height, folders, name_index)
        #break

    generate_drawings(folders[2], folders[3], dst_draw_folder)
