
import shutil
import os
from enum import Enum
from os import listdir
from os.path import isfile, join

class All_Day_Night(Enum):
    all_ = 'all'
    day = 'day'
    night = 'night'
    train = 'train'


# Force delete folder if exist
def mkdir(path, force = False):
    try:
        os.mkdir(path)
    except FileExistsError:
        if force:
            shutil.rmtree(path)
            os.mkdir(path)



def parse_xml_to_dict(xml_path):
    # private
    def recursive_parse_xml_to_dict(xml):
        if not len(xml):
            return {xml.tag: xml.text}
        result = {}
        for child in xml:
            child_result = recursive_parse_xml_to_dict(child)
            if child.tag != 'object':
                result[child.tag] = child_result[child.tag]
            else:
                if child.tag not in result:
                    result[child.tag] = []
                result[child.tag].append(child_result[child.tag])
        return {xml.tag: result}

    import tensorflow as tf
    from lxml import etree
    with tf.gfile.GFile(xml_path, 'r') as fid:
        xml_str = fid.read()
    xml = etree.fromstring(xml_str)
    return recursive_parse_xml_to_dict(xml)['annotation']




def get_files(dir, sort = False):
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    if sort:
        return sorted(files)
    return files

def check_rotation(path_video_file):
    import cv2
    import  ffmpeg 
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
