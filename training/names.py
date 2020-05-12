


import tensorflow as tf
import argparse
import os







if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str)
    args = parser.parse_args()

    model_path = os.path.join('/home/kopi/local_git/architectures', args.name, 'frozen_inference_graph.pb')

    with tf.gfile.GFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        names = [n.name for n in graph_def.node ] #if "TFLite_Detection_PostProcess" in n.name ]


    print(names)
