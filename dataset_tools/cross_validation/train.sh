#!/bin/bash





# Exit script on error.
set -e
# Echo each command, easier for debugging.
# set -x

# keep only tensorboard data
delete_train_files(){   
    for NAME in $1/*; do
        if [ "$(basename $NAME)" != "eval_0" ]; then
            rm -r "${NAME}";
        fi
    done
}

# keep only final edge_tpu model(and log)
delete_model_files(){
    for NAME in $1/*; do
        if [ "$(basename $NAME)" != "output_tflite_graph_edgetpu.tflite" ] && [ "$(basename $NAME)" != "output_tflite_graph_edgetpu.log" ]; then
            rm "${NAME}";
        fi
    done 
}

copy_model_into_obj_api(){
    TYPE=$(cat "$1/pipeline.config" | grep '\stype:' | sed 's/[a-z]*: \"//g' | sed 's/\"//g' | sed 's/\s//g')
    ARCHITECTURE_DIR="$2/${TYPE}"
    #copy model to obj API
    cp "${ARCHITECTURE_DIR}/model.ckpt.data-00000-of-00001" "model.ckpt.data-00000-of-00001"
    cp "${ARCHITECTURE_DIR}/model.ckpt.index" "model.ckpt.index"
    cp "${ARCHITECTURE_DIR}/model.ckpt.meta" "model.ckpt.meta" 
}


usage(){
    echo "Usage: sysinfo_page [[-d name of dataset (from {Local_git}/dataset/exported ) ], [-s number of training steps]]"
    exit
}

# 0. parse arguments
if [ "$1" = "" ]; then usage; fi
while [ "$1" != "" ]; do
    case $1 in
        -d | --dataset )           
            shift
            DATASET="${LOCAL_GIT}/dataset/exported/$1"
            if ! [ -d "${DATASET}" ]; then 
                echo "Dataset on path ${DATASET} doesn't exist." 
                usage; 
            fi
            ;;
        -s | --step ) 
            shift 
            re='^[0-9]+$'
            if ! [[ $1 =~ $re ]]; then
                echo "Steps is not a number."
                usage
            fi  
            num_training_steps="$1"
            ;;
        -i | --index ) 
            shift 
            INDEX="$1"
            ;;
        -h | --help )           
            usage
            ;;
        * )                     
            usage
    esac
    shift
done

# set variables 
INPUT_TENSORS='normalized_input_image_tensor'
OUTPUT_TENSORS='TFLite_Detection_PostProcess,TFLite_Detection_PostProcess:1,TFLite_Detection_PostProcess:2,TFLite_Detection_PostProcess:3'

cd "${LOCAL_GIT}/object_detection/"


# number_to_process=$(ls "${PROJECT_ROOT}/training/configs/configs_to_process/" | wc -l)

# echo ${number_to_process}
# exit

number_to_process=$(ls "${PROJECT_ROOT}/training/configs/configs_to_process/" | wc -l)
if [ "${number_to_process}" != '0' ]; then
    for CKPT_DIR in ~/diplomka/training/configs/configs_to_process/*/ ; do


        echo "CONVERTING dataset to TF Record..."
        python dataset_tools/create_pet_tf_record2.py \
            --data_dir="${DATASET}" \
            --output_dir="${LOCAL_GIT}/dataset/exported/tf_records"

        echo "tf records done"

        CKPT_NAME="$(basename $CKPT_DIR)"
        BASE_FOLDER="${PROJECT_ROOT}/training/output/folds/${CKPT_NAME}"
        if [ -d "${BASE_FOLDER}" ]; then 
            echo "base exist"; 
        else
            mkdir "${BASE_FOLDER}";
        fi


        OUTPUT_I="${BASE_FOLDER}/model_${INDEX}"
        if [ -d "${OUTPUT_I}" ]; then rm -Rf ${OUTPUT_I}; fi
        mkdir "${OUTPUT_I}"


        copy_model_into_obj_api "${CKPT_DIR}" "${HOME}/local_git/architectures"
        cp "${CKPT_DIR}/pipeline.config" "${OUTPUT_I}/pipeline.config"
        
        TRAIN_DIR="${OUTPUT_I}/train"
        echo "Start training..."
        python model_main.py \
            --pipeline_config_path="${CKPT_DIR}/pipeline.config" \
            --model_dir="${TRAIN_DIR}" \
            --num_train_steps="${num_training_steps}" \
            --num_eval_steps="500"



        MODEL_DIR="${OUTPUT_I}/model"
        ckpt_number=${num_training_steps}
        echo "EXPORTING frozen graph from checkpoint..."
        python export_tflite_ssd_graph.py \
            --pipeline_config_path="${CKPT_DIR}/pipeline.config" \
            --trained_checkpoint_prefix="${TRAIN_DIR}/model.ckpt-${ckpt_number}" \
            --output_directory="${MODEL_DIR}" \
            --add_postprocessing_op=true


        # Parse width and height from pipeline.config file
        HEIGHT=$(cat "${CKPT_DIR}/pipeline.config" | grep "height:" | sed "s/[a-z]*://g")
        WIDTH=$(cat "${CKPT_DIR}/pipeline.config" | grep "width:" | sed "s/[a-z]*://g")

        echo "CONVERTING frozen graph to TF Lite file..."
        tflite_convert \
            --output_file="${MODEL_DIR}/output_tflite_graph.tflite" \
            --graph_def_file="${MODEL_DIR}/tflite_graph.pb" \
            --inference_type=QUANTIZED_UINT8 \
            --input_arrays="${INPUT_TENSORS}" \
            --output_arrays="${OUTPUT_TENSORS}" \
            --mean_values=128 \
            --std_dev_values=128 \
            --input_shapes=1,"${HEIGHT}","${WIDTH}",3 \
            --change_concat_input_ranges=false \
            --allow_nudging_weights_to_use_fast_gemm_kernel=true \
            --allow_custom_ops

        # Compile model for edge tpu
        edgetpu_compiler "${MODEL_DIR}/output_tflite_graph.tflite" -o "${MODEL_DIR}"



        echo "---Additional informations---" >> "${MODEL_DIR}/output_tflite_graph_edgetpu.log"
        echo "width: ${WIDTH}" >> "${MODEL_DIR}/output_tflite_graph_edgetpu.log"
        echo "height: ${HEIGHT}" >> "${MODEL_DIR}/output_tflite_graph_edgetpu.log"
        
        cp -r "${OUTPUT_I}" "${LOCAL_GIT}/tensorboard/${CKPT_NAME}"
        rm -r "${OUTPUT_I}/train"

        # Delete all unnessesary model files
        #delete_train_files "${TRAIN_DIR}"
        delete_model_files "${MODEL_DIR}"
    
    done
fi

# cd "${PROJECT_ROOT}/"
# git add -A
# git commit -m 'pc finished training'
# git push


# shutdown now
















