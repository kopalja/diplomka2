#!/bin/bash

### USAGE
# One parameter (path to raw_footage folder)
# Creates new folder in ~/local_git/dataset/processed.

# CREATED FOLDER STRUCTURE
#           {BATCH_name}
#           /         \
#         day        night
#      /  |  \      /  |  \
#     d   i  x     d   i   x
###############################

# Example ./main ${LOCAL_GIT}/dataset/raw_footage/batch_2

cd "${PROJECT_ROOT}/training/dataset_tools/process_video"

OUTPUT_ROOT="${LOCAL_GIT}/dataset/processed/$(basename $1)"

if [ -d "${OUTPUT_ROOT}" ]; then
    echo "Processed batch already exist"
    exit
fi


echo "Preparing images..."
python prepare_dir.py --batch_name "$(basename $1)"
python video_to_images.py --root "$1" --batch_name "$(basename $1)"


echo "Labeling images..."
cd "${LOCAL_GIT}/yolo_v3"
python yolo_video.py --input "${OUTPUT_ROOT}/tmp_day" --output "${OUTPUT_ROOT}/day"
python yolo_video.py --input "${OUTPUT_ROOT}/tmp_night" --output "${OUTPUT_ROOT}/night"


rm -r "${OUTPUT_ROOT}/tmp_day"
rm -r "${OUTPUT_ROOT}/tmp_night"

#cp -rf "${OUTPUT_ROOT}" "${OUTPUT_ROOT}/../../processed_backup/$(basename $1)"

echo "Done."