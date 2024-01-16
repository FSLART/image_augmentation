
# Image Augmentation

This repository houses a image augmentation toolkit, designed to enhance our database of training images by restructuring the same images for further use.

## Getting Started:

### Requirements
* Python 3.9 or higher
* Images with a COCO formated annotation file

### Installing
Step1. Clone this repository.

`git clone https://github.com/FSLART/image_augmentation.git`

Step2. (Optional) Create a python environment

`virtualenv py_env`

Step3. Install the required libraries

`pip install -r requirements.txt`

## Usage
Create new images from original ones by tranforming them with differente atributes like blur, erosion, scale, rotation, etc.
Increase your dataset without the need to create new images.

### Required files
To use the image augmentor start by populating the **"images/"** directory with images to be augmented.
For more information about the images directory go to [IMAGES.md](images/IMAGES.md).
Next add the COCO formated annotation files to the **"annotations/"** directory.
For more information about the annotations directory go to [ANNOTATIONS.md](annotations/ANNOTATIONS.md)

### Configuration
Before configuring anything try searching all config files inside **"configs/"** to see if any suit your needs. If none do, to create your configuration file follow the rules in [CONFIG.md](configs/CONFIG.md).
To know what each configuration option does, there is a template config file on "**configs/**[template.ini](configs/template.ini)" that as a description to all config properties that you can modify.

### How to run
To launch the image augmentor go to the base directory of this commit and use one of the following commands on your shell:
```shell
# Basic augmentor call for any config
python3 py/augmentIMG.py --config configs/config_file_path
# or
python3 py/augmentIMG.py -c configs/config_file_path

# Use default values
python3 py/augmentIMG.py
```