
import os
import argparse
import sys
sys.path.insert(0, os.environ['PROJECT_ROOT'])
from python_tools.functions import mkdir


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_name', type=str)
    args = parser.parse_args()

    output_root = os.path.join(os.environ['LOCAL_GIT'], 'dataset/processed', args.batch_name)
    day = os.path.join(output_root, "day")
    night = os.path.join(output_root, "night")

    mkdir(output_root, force = True)
    mkdir(day)
    mkdir(night)
    for c in ["draw", "images", "xmls"]:
        mkdir(os.path.join(day, c))
        mkdir(os.path.join(night, c))
