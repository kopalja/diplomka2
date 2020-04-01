# Diplomka

This project is for retraining mobile object detection architectures such as mobilenets on a custom dataset. Included scripts makes it easy to prepare datasets with different image resolutions, number of samples and various types(day, night, both).
The main project is divided into two parts **Training** and **Testing**.


## Training
Constains pipeline to get from raw footage(videos of cars) to retrained model. 
Its divided into three parts **Dataset tools**, **Configs** and **Output**.

#### Dataset tools
Dataset tools is responsible for creating dataset on which we can perform training

#### Configs
Configs contains user specified configurations of model architecture and training configuration.

### Output
Ouput is where traing results are saved. For each configuration contains both final model and traing events(for tensorboard)


## Testing
Testing part is diveded into two parts **Accuracy** and **Speed**
**Speed** part is inteded to be performed primary on embeded devices to test model speed on restricted hardware recourses.
While **Accuracy** is meant to be performed on desktop pc, which containes large testing dataset.


## Getting Started

To keep this repositori small it does not contains any large files such as models architectures or any kind of dataset.
However it contains only tools which operates with those large files.

To run this project locali you have to also clone second repositori named LOCAL_GIT from here(not available yet) and create system variable.

```
export LOCAL_GIT=<path to LOCAL_GIT on your pc>
export PROJECT_ROOT=<path to cloned repository>

```

### Prerequisites

Prerequisites for running are:

```
Tensorflow Object Detection API
ffmpeg
```


