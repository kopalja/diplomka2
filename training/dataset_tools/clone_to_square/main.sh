#!/bin/bash

### USAGE
# Three positionals parameters
# 1. name of new exported dataset. New fodler will be created in ~/local_git/dataset/exported/{name}
# 2. type of new dataset [all, day, night]
# 3. included batches. Names of folders in ~/local_git/dataset/processed/... (e.g. --batch "batch_1 bath_3")

# Example ./main -n test -t night -b "batch_1 batch_2"

usage()
{
    echo "Usage: sysinfo_page [[-f name of the dataset to clone (on path LOCAL_GIT/dataset/processed/) ]"
    exit
}
#cd "${PROJECT_ROOT}/training/dataset_tools/export/clone_to_square"

SQUARE=false
# parse arguments
while [ "$1" != "" ]; do
    case $1 in
        -f | --from )           
            shift
            FROM=$1
            ;;
        -h | --help )           
            usage
            ;;
        * )                     
            usage
    esac
    shift
done

if [ "${FROM}" == "" ]; then
    usage
fi



PROCESSED_DIR="${LOCAL_GIT}/dataset/processed/${FROM}"
EXPORTED_DIR="${LOCAL_GIT}/dataset/processed/${FROM}_square"


# Create new empty dataset
if [ -d "${EXPORTED_DIR}" ]; then rm -Rf "${EXPORTED_DIR}"; fi
mkdir "${EXPORTED_DIR}"
mkdir "${EXPORTED_DIR}/day"
mkdir "${EXPORTED_DIR}/night"
mkdir "${EXPORTED_DIR}/day/draw"
mkdir "${EXPORTED_DIR}/day/images"
mkdir "${EXPORTED_DIR}/day/xmls"
mkdir "${EXPORTED_DIR}/night/draw"
mkdir "${EXPORTED_DIR}/night/images"
mkdir "${EXPORTED_DIR}/night/xmls"

# # Create new empty dataset
# if [ -d "${EXPORTED_DIR}/${NAME}" ]; then rm -Rf ${EXPORTED_DIR}/${NAME}; fi
# mkdir "${EXPORTED_DIR}/${NAME}"
# mkdir "${EXPORTED_DIR}/${NAME}/images"
# mkdir "${EXPORTED_DIR}/${NAME}/draw"
# mkdir "${EXPORTED_DIR}/${NAME}/annotations"
# mkdir "${EXPORTED_DIR}/${NAME}/annotations/xmls"

echo "Cloning ..."
python clone_rectangle.py --ffrom="${PROCESSED_DIR}" --to="${EXPORTED_DIR}"


echo "Drawing day ... "
python create_draw.py --root "${EXPORTED_DIR}/day"
echo "Drawing night ... "
python create_draw.py --root "${EXPORTED_DIR}/night"


echo "Done"