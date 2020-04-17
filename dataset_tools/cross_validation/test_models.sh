
#!/bin/bash


usage(){
    echo "Usage: sysinfo_page [[-n name of model ], [-t type of new dataset {all, day, night, voc}]]"
    exit
}


MODELS_ROOT_DIR="${PROJECT_ROOT}/training/output/folds"
#MODELS_ROOT_DIR="${PROJECT_ROOT}/training/output"
MODEL_NAME=""
TYPE="all"

# 0. parse arguments
if [ "$1" = "" ]; then usage; fi
while [ "$1" != "" ]; do
    case $1 in
        -n | --name )           
            shift
            MODEL_NAME="$1"
            MODEL_DIR="${MODELS_ROOT_DIR}/$1"
            NUM_OF_FOLDS=$(ls ${MODEL_DIR} | wc -l)
            #NUM_OF_FOLDS="5"
            if [ ! -d "${MODEL_DIR}" ]; then
                echo "Folder ${MODEL_DIR} doesn't exist."
                exit
            fi
            ;;
        # test type
        -t | --type ) 
            shift 
            if [ "$1" != "all" ] && [ "$1" != "day" ] && [ "$1" != "night" ] && [ "$1" != "voc" ] && [ "$1" != "detrac" ] && [ "$1" != "train" ] && [ $1 != "fold" ]; then
                usage
            fi  
            TYPE=$1
            ;;
        -h | --help )           
            usage
            ;;
        * )                     
            usage
    esac
    shift
done



#NUM_OF_FOLDS="$(($NUM_OF_FOLDS-1))"

for ((i=0;i<"${NUM_OF_FOLDS} ";i++)); 
do 
    FINAL_TYPE="${TYPE}"
    if [ "${FINAL_TYPE}" == "fold" ]; then
        FINAL_TYPE="fold_${i}"
    fi

    cd "${PROJECT_ROOT}/testing/accuracy/" 
    ./main.sh -n "folds/${MODEL_NAME}/model_${i}" -t "${FINAL_TYPE}"
    #./main.sh -n "${MODEL_NAME}" -t "${FINAL_TYPE}"
done


