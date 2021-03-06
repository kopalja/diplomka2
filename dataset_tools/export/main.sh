#!/bin/bash

### USAGE
# Three positionals parameters
# 1. name of new exported dataset. New fodler will be created in ~/local_git/dataset/exported/{name}
# 2. type of new dataset [all, day, night]
# 3. included batches. Names of folders in ~/local_git/dataset/processed/... (e.g. --batch "batch_1 bath_3")

# Example ./main -n test -t night -b "batch_1 batch_2"

usage()
{
    echo "Usage: sysinfo_page [[-n name of new dataset ], [-t type of new dataset {all, day, night}], [-b list of included batches]]"
    exit
}


# parse arguments
while [ "$1" != "" ]; do
    case $1 in
        -n | --name )           
            shift
            NAME=$1
            ;;
        # test type
        -t | --type ) 
            shift 
            if [ "$1" != "all" ] && [ "$1" != "day" ] && [ "$1" != "night" ]; then
                usage
            fi  
            TYPE=$1
            ;;
        # parse batches into array
        -b | --batch ) 
            shift   
            i=0
            for batch in $1
            do
                BATCH[$i]=${batch}
                ((i++))
            done
            ;;
        -h | --help )           
            usage
            ;;
        * )                     
            usage
    esac
    shift
done

PROCESSED_DIR="${LOCAL_GIT}/dataset/processed"
EXPORTED_DIR="${LOCAL_GIT}/dataset/exported/${NAME}"


# Create new empty dataset
rm -Rf "${EXPORTED_DIR}" 
mkdir "${EXPORTED_DIR}"
mkdir "${EXPORTED_DIR}/images"
mkdir "${EXPORTED_DIR}/draw"
mkdir "${EXPORTED_DIR}/annotations"
mkdir "${EXPORTED_DIR}/annotations/xmls"

echo "Creating dataset..."
for batch in "${BATCH[@]}"
do
    python ${PROJECT_ROOT}/dataset_tools/export/merge_to_export.py --processed="${PROCESSED_DIR}/${batch}" --exported="${EXPORTED_DIR}" --type="${TYPE}"
    if [[ $? = 0 ]]; then
        echo "Export script finisher succesfully"
    else
        echo "Export script crashed: $?"
        rm -Rf "${EXPORTED_DIR}"
        exit
    fi
done


python ${PROJECT_ROOT}/python_tools/create_draw.py --root "${EXPORTED_DIR}"


ls "${EXPORTED_DIR}/images" > "${EXPORTED_DIR}/annotations/trainval.txt"
echo "Done"