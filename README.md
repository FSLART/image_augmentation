
# Image Augmentation

This repository houses a image augmentation toolkit, designed to enhance our database of training images by restructuring the same images for further use.

## Getting Started:

### Requirements
* Python 3.9 or higher
* Images with a COCO formated annotation file

### Installing
Step1. Clone this repository.

`git clone https://github.com/FSLART/image_augmentation.git`

Step2. Install the required libraries

`pip install -r requirements.txt`

Step3. (Optional) Create a python environment

`virtualenv py_env`

## Usage

### Required files
To use the image augmentor start by populating the **"images/"** directory with images to be augmented.
For more information about the images directory go to [IMAGES.md](images/IMAGES.md).
Next add the COCO formated annotation files to the **"annotations/"** directory.
For more information about the annotations directory go to [ANNOTATIONS.md](annotations/ANNOTATIONS.md)

### Configuration
Before configuring anything try searching all config files inside **"configs/"** to see if any suit your needs. If none do, to create your configuration file follow the rules in [CONFIG.md](configs/CONFIG.md).

### How to run

To launch the image augmentor go to the base directory of this commit and use one of the following commands on your shell:
```shell
# Basic augmentor call for any config
python3 augmentIMG.py --config config_file_path
# or
python3 augmentIMG.py -c config_file_path

# Use default values
python3 augmentIMG.py
```