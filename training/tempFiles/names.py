
import tensorflow as tf


#model_filepath = '/home/kopi/diplomka/training/configs/cfgs_to_process/resnet/frozen_inference_graph.pb'
model_filepath = '/home/kopi/diplomka/training/configs/cfgs/lr/tflite_graph.pb'

with tf.gfile.GFile(model_filepath, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())

    names = [n.name for n in graph_def.node if "Conv" in n.name ]




print(len(names))