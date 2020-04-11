


cd "${LOCAL_GIT}/object_detection/"

INPUT_TENSORS='normalized_input_image_tensor'
OUTPUT_TENSORS='TFLite_Detection_PostProcess,TFLite_Detection_PostProcess:1,TFLite_Detection_PostProcess:2,TFLite_Detection_PostProcess:3'


CKPT_DIR="${PROJECT_ROOT}/training/configs/configs_to_process/inception"


CKPT_NAME="$(basename $CKPT_DIR)"
OUTPUT_I="${PROJECT_ROOT}/training/output/${CKPT_NAME}"

MODEL_DIR="${OUTPUT_I}/model"
TRAIN_DIR="${OUTPUT_I}/train"
ckpt_number=55000
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

# Delete all unnessesary model files
# delete_train_files "${TRAIN_DIR}"
# delete_model_files "${MODEL_DIR}"

echo "---Additional informations---" >> "${MODEL_DIR}/output_tflite_graph_edgetpu.log"
echo "width: ${WIDTH}" >> "${MODEL_DIR}/output_tflite_graph_edgetpu.log"
echo "height: ${HEIGHT}" >> "${MODEL_DIR}/output_tflite_graph_edgetpu.log"