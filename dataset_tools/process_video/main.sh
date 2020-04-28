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
# Example: ./main ${LOCAL_GIT}/dataset/raw_footage/batch_2


usage()
{
    echo "Usage: sysinfo_page [[name of the video dataset to process (on path LOCAL_GIT/dataset/raw_footage/) ]"
    exit
}


# Parse arguments
if [ "$#" -ne 1 ]; then
    usage
    exit
fi

cd "${PROJECT_ROOT}/training/dataset_tools/process_video"

INPUT_DIR="${LOCAL_GIT}/dataset/raw_footage/$1"
OUTPUT_DIR="${LOCAL_GIT}/dataset/processed/$1"

if [ ! -d "${INPUT_DIR}" ]; then
    echo "Input directory does not exist"
    exit
fi

if [ -d "${OUTPUT_DIR}" ]; then
    echo "Output directory already exist"
    exit
fi


echo "Preparing images..."
python prepare_dir.py --batch_name "$1"
python video_to_images.py --root "${INPUT_DIR}" --batch_name "$1"






echo "Labeling images..."
cd "${LOCAL_GIT}/yolo_v3"
python yolo_video.py --input "${OUTPUT_DIR}/tmp_day" --output "${OUTPUT_DIR}/day"
python yolo_video.py --input "${OUTPUT_DIR}/tmp_night" --output "${OUTPUT_DIR}/night"


rm -r "${OUTPUT_DIR}/tmp_day"
rm -r "${OUTPUT_DIR}/tmp_night"

#cp -rf "${OUTPUT_ROOT}" "${OUTPUT_ROOT}/../../processed_backup/$(basename $1)"

echo "Done."