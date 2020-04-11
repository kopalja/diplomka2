


import tensorflow as tf


#model_filepath = '/home/kopi/diplomka/training/configs/cfgs_to_process/resnet/frozen_inference_graph.pb'
#model_filepath = '/home/kopi/local_git/architectures/ssd_resnet50_v1_fpn/frozen_inference_graph.pb'
model_filepath = '/home/kopi/diplomka/training/output/resnet/model/tflite_graph.pb'

with tf.gfile.GFile(model_filepath, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())

    

    names = [n.name for n in graph_def.node if "TFLite_Detection_PostProcess" in n.name ]






print(names)