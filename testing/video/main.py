# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""A demo for object detection.

For Raspberry Pi, you need to install 'feh' as image viewer:
sudo apt-get install feh

Example (Running under edgetpu repo's root directory):

  - Face detection:
    python3 edgetpu/demo/object_detection.py \
    --model='test_data/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite' \
    --input='test_data/face.jpg' \
    --keep_aspect_ratio

  - Pet detection:
    python3 edgetpu/demo/object_detection.py \
    --model='test_data/ssd_mobilenet_v1_fine_tuned_edgetpu.tflite' \
    --label='test_data/pet_labels.txt' \
    --input='test_data/pets.jpg' \
    --keep_aspect_ratio

'--output' is an optional flag to specify file name of output image.
At this moment we only support SSD model with postprocessing operator. Other
models such as YOLO won't work.
"""

import time

import argparse
import platform
import subprocess
from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils
from PIL import Image
from PIL import ImageDraw


###
#from CarTracking import CarTracking
#tracking = CarTracking(300, 300, 30)

#from IOUTracker import IOUTracker
#iou_tracker = IOUTracker(0, 0.5, 0.5, 15)



import cv2
import numpy


def resizeArray(img):
  height, width, channels = img.shape
  border = (width - height) // 2
  # flip color representation
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  # crop central square
  img = img[0 : height, border : border + height]
  # downscale resolution
  img = cv2.resize(img, (300, 300))
  # ndarray to PIL 
  image = Image.fromarray(img)
  return image, img



def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--model',
      help='Path of the detection model, it must be a SSD model with postprocessing operator.',
      required=True)
  parser.add_argument('--label', help='Path of the labels file.')
  parser.add_argument(
      '--input', help='File path of the input image.', required=True)
  parser.add_argument('--output', help='File path of the output image.')
  parser.add_argument(
      '--keep_aspect_ratio',
      dest='keep_aspect_ratio',
      action='store_true',
      help=(
          'keep the image aspect ratio when down-sampling the image by adding '
          'black pixel padding (zeros) on bottom or right. '
          'By default the image is resized and reshaped without cropping. This '
          'option should be the same as what is applied on input images during '
          'model training. Otherwise the accuracy may be affected and the '
          'bounding box of detection result may be stretched.'))
  parser.set_defaults(keep_aspect_ratio=False)
  args = parser.parse_args()

  if not args.output:
    output_name = 'object_detection_result.jpg'
  else:
    output_name = args.output

  # Initialize engine.
  engine = DetectionEngine(args.model)
  labels = dataset_utils.ReadLabelFile(args.label) if args.label else None


  vidcap = cv2.VideoCapture(args.input)
  
  output_frames = []





  start = time.time()
  i = 0
  success = True
  while success:
    i += 1
    # Open image.
    #img = Image.open(args.input)
    success, img = vidcap.read()
    if not success:
      break

    # if  not i % 2 == 0:
    #   continue


    # image = Image.fromarray(img)
    image, img = resizeArray(img)





    draw = ImageDraw.Draw(image)



  

    # Run inference.
    ans = engine.DetectWithArray(
        img,
        threshold=0.4,
        keep_aspect_ratio=args.keep_aspect_ratio,
        relative_coord=False,
        top_k=10)



    # Display result.
    if ans:

      # boxes = []
      # for obj in ans:
      #   boxes.append(obj.bounding_box.flatten().tolist())
      # print(boxes)
      # tracking.setPoints(boxes)

      #iou_tracker.update_tracks(ans)

      

      for obj in ans:
        print('-----------------------------------------')
        if labels:
          print(labels[obj.label_id])
        print('score = ', obj.score)
        box = obj.bounding_box.flatten().tolist()
        print('box = ', box)
        draw.rectangle(box, outline='red')
      #img.save(output_name)
      if platform.machine() == 'x86_64':
        # For gLinux, simply show the image.
        output_frames.append(numpy.array(image))
        #image.show()
        #print(image.siz)
        #break
      #elif platform.machine() == 'armv7l':
        # For Raspberry Pi, you need to install 'feh' to display image.
        #subprocess.Popen(['feh', output_name])
      #else:
        #print('Please check ', output_name)
    else:
      print('No object detected!')


  print('frames {0}'.format(i))
  print('time {0}'.format(time.time() - start))
  print('cars detected {0}'.format(iou_tracker.get_tracked_number()))


  # size = (300, 300)
  # out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
  # for i in range(len(output_frames)):
  #   out.write(output_frames[i])
  # out.release()


if __name__ == '__main__':
  main()


