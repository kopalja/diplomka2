from os.path import isfile, join
from os import listdir
import os
import shutil
import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=str)
    args = parser.parse_args() 

    day_folder = os.path.join(args.root, 'day')
    night_folder = os.path.join(args.root, 'night')


    for category_root in [day_folder, night_folder]:
        draw_folder = os.path.join(category_root, 'draw')
        images_folder = os.path.join(category_root, 'images')
        xmls_folder = os.path.join(category_root, 'xmls')

        dst_draw_folder = os.path.join(category_root, 'draw_tmp')
        dst_images_folder = os.path.join(category_root, 'images_tmp')
        dst_xmls_folder = os.path.join(category_root, 'xmls_tmp')


        name_index = 0
        images_name = sorted([f for f in listdir(draw_folder) if isfile(join(draw_folder, f))])
        #copy files
        for image_name in images_name:
            or_name = image_name[:-4]
            name = 'my_' + str(name_index).zfill(6)
            shutil.copy(os.path.join(images_folder, or_name + '.jpg'), os.path.join(dst_images_folder, name + '.jpg'))
            shutil.copy(os.path.join(xmls_folder, or_name + '.xml'), os.path.join(dst_xmls_folder, name + '.xml'))
            shutil.copy(os.path.join(draw_folder, or_name + '.jpg'), os.path.join(dst_draw_folder, name + '.jpg'))
            name_index += 1  



    