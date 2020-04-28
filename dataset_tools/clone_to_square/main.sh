#!/bin/bash

### USAGE
# One positionals parameters
# 1. name of the dataset to square.
# Source dataset have to be in  ~/local_git/dataset/processed/ directory
# Ouput dataset will be in the  ~/local_git/dataset/processed/$name_square
# Example: ./main batch_1_day

usage()
{
    echo "Usage: sysinfo_page [[name of the dataset to clone (on path LOCAL_GIT/dataset/processed/) ]"
    exit
}


# Parse arguments
if [ "$#" -ne 1 ]; then
    usage
    exit
fi


PROCESSED_DIR="${LOCAL_GIT}/dataset/processed/${1}"
EXPORTED_DIR="${LOCAL_GIT}/dataset/processed/${1}_square"



# Test input folder
if [ ! -d "${PROCESSED_DIR}" ]; then
    echo "Input folder does not exist."
    exit
fi

# create new folder structure 
rm -Rf "${EXPORTED_DIR}"
mkdir "${EXPORTED_DIR}"
mkdir "${EXPORTED_DIR}/day"
mkdir "${EXPORTED_DIR}/night"
mkdir "${EXPORTED_DIR}/day/draw"
mkdir "${EXPORTED_DIR}/day/images"
mkdir "${EXPORTED_DIR}/day/xmls"
mkdir "${EXPORTED_DIR}/night/draw"
mkdir "${EXPORTED_DIR}/night/images"
mkdir "${EXPORTED_DIR}/night/xmls"


echo "Cloning ..."
python ${PROJECT_ROOT}/dataset_tools/clone_to_square/clone.py --ffrom="${PROCESSED_DIR}" --to="${EXPORTED_DIR}"
if [[ $? = 0 ]]; then
    echo "Clone script finisher succesfully"
else
    echo "Clone script crashed: $?"
    rm -Rf "${EXPORTED_DIR}"
    exit
fi


echo "Drawing day ... "
python ${PROJECT_ROOT}/python_tools/create_draw.py --root "${EXPORTED_DIR}/day"
echo "Drawing night ... "
python ${PROJECT_ROOT}/python_tools/create_draw.py --root "${EXPORTED_DIR}/night"
echo "Done"