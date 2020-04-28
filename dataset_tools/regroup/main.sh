#!/bin/bash


### USAGE
# One parameter (path to processed folder)
# Delete, rename and redraw all files to update new changes

# Example ./main /home/kopi/local_git/dataset/processed/batch_2


usage()
{
    echo "Usage: sysinfo_page [[-n name of hte dataset to regroup ]]"
    exit
}

NAME=""
# parse arguments
while [ "$1" != "" ]; do
    case $1 in
        -n | --name )           
            shift
            NAME=$1
            ;;
        -h | --help )           
            usage
            ;;
        * )                     
            usage
    esac
    shift
done

if [ "${NAME}" == "" ]; then
    usage
fi

#cd "${PROJECT_ROOT}/training/dataset_tools/regroup"

dataset_root="${LOCAL_GIT}/dataset/processed/${NAME}"

mkdir "${dataset_root}/day/draw_tmp"
mkdir "${dataset_root}/day/images_tmp"
mkdir "${dataset_root}/day/xmls_tmp"

mkdir "${dataset_root}/night/draw_tmp"
mkdir "${dataset_root}/night/images_tmp"
mkdir "${dataset_root}/night/xmls_tmp"

python regroup.py --root "${dataset_root}"


rm -r "${dataset_root}/day/draw"
rm -r "${dataset_root}/day/images"
rm -r "${dataset_root}/day/xmls"

rm -r "${dataset_root}/night/draw"
rm -r "${dataset_root}/night/images"
rm -r "${dataset_root}/night/xmls"


mv "${dataset_root}/day/draw_tmp" "${dataset_root}/day/draw" 
mv "${dataset_root}/day/images_tmp" "${dataset_root}/day/images"
mv "${dataset_root}/day/xmls_tmp" "${dataset_root}/day/xmls"

mv "${dataset_root}/night/draw_tmp" "${dataset_root}/night/draw" 
mv "${dataset_root}/night/images_tmp" "${dataset_root}/night/images"
mv "${dataset_root}/night/xmls_tmp" "${dataset_root}/night/xmls"


echo "Change drawings"
rm -r "${dataset_root}/day/draw"
rm -r "${dataset_root}/night/draw"

mkdir "${dataset_root}/day/draw"
mkdir "${dataset_root}/night/draw"

python ${PROJECT_ROOT}/python_tools/create_draw.py --root "${dataset_root}/day"
python ${PROJECT_ROOT}/python_tools/create_draw.py --root "${dataset_root}/night"