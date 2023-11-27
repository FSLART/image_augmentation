import annotations as annt
import datagen as dtg
import configparser as cfgp
from datetime import datetime
import filetype
import json
import os
import re


class DataWriter:
    def __init__(self, configFile="./config.ini"):
        # Get configs
        self.io_c, self.gen_c = getConfigs(configFile)
        
        # Create Annotation and ImageGenerator Objects
        self.generator=dtg.ImageGenerator(*self.gen_c)
        
        # Setting output type
        outputAs = None
        if   self.io_c[3] == "default":
            outputAs = self.__outputByDefault
        elif self.io_c[3] == "filename":
            outputAs = self.__outputByFilename
        elif self.io_c[3] == "batch":
            outputAs = self.__outputByBatch
            self.batch = os.path.abspath("from_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S")) + "/"
            os.mkdir(os.path.abspath(self.batch), 0o755)
            os.mkdir(os.path.abspath(self.batch + "images/"), 0o755)
            os.mkdir(os.path.abspath(self.batch + "annotations/"), 0o755)
            
        if outputAs == None:
            raise ValueError("Output type not supported")
        
        for file in os.listdir(self.io_c[0]):
            filepath = os.path.abspath(self.io_c[0] + file)
            if os.path.isdir(filepath) or not filetype.is_image(filepath):
                continue
            for i in range(self.io_c[4]):
                self.noter=annt.Annotation(self.io_c[2], file)
                outputAs(self.generator.dataGeneration(filepath), file)
        
    
    # Do output by default
    def __outputByDefault(self, image, imageName):
        # create files
        self.__createFiles(image, imageName, os.path.abspath(self.io_c[0]) + "/", os.path.abspath(self.io_c[1]) + "/")
    
    # Do output by filename to image directory
    def __outputByFilename(self, image, imageName):
        imageName = check_file_exists(imageName, self.io_c[0])
        dirname=os.path.abspath(self.io_c[0] + imageName)
        
        # Verify if path already exists and create if not
        if not os.path.exists(dirname):
            os.mkdir(dirname, 0o755)
        else:
            dirname=os.path.abspath(self.io_c[0]
                                    + check_file_exists(imageName, self.io_c[0]))
            os.mkdir(dirname, 0o755)
        if not os.path.isdir(dirname):
            print("Tried to create directory with file name")
            return
        
        # create files
        self.__createFiles(image, imageName, dirname+ "/", dirname+ "/")

    # Do output by batch to base directory
    def __outputByBatch(self, image, imageName):
        imageName = check_file_exists(imageName, self.io_c[0])
        
        # create files
        self.__createFiles(image, imageName, self.batch + "images/", self.batch + "annotations/")
    
    # Create files to output type defined before
    def __createFiles(self, image, filename, imageDir, annotationDir):
        gen = self.generator
        anote = self.noter
        filename = check_file_exists(filename, imageDir)
        try:
            gen_to_annt(self.generator, self.noter)
            gen.imageOutput(image, filename, imageDir)
            anote.imageJSON(filename, annotationDir)
        except RuntimeError as e:
            print(e)
    
   
def getConfigs(configFile):
    print(os.path.abspath(configFile))
    if not os.path.exists(os.path.abspath(configFile)):
        print("Config file does not exist")
        exit()
    
    config = cfgp.ConfigParser()
    config.read(configFile)
    
    IO = config['IO']
    GENERATOR = config['GENERATOR']
    try:
        # Load both config settings to a cons array so configs can be unorganized
        # Load IO configs on a const array
        inOut = [IO["images"] if "images" in IO else "images/",
                 IO["annotations"] if "annotations" in IO else "annotations/",
                 IO["coco_file_to_use"] if "coco_file_to_use" in IO else "annotations/fsoco.json",
                 IO["output_directory_type"] if "output_directory_type" in IO else "default",
                 int(IO["augments_per_image"]) if "augments_per_image" in IO else 1]
        
        # Load GENERATOR configs on a const array
        generator = [__decode_filter_hash(GENERATOR["filter_hash"]) if "filter_hash" in GENERATOR else dtg.FULL_HASH,
                     int(GENERATOR["max_filters_to_apply"]) if "max_filters_to_apply" in GENERATOR else dtg.DEFAULT_MAX_F,
                     json.loads(GENERATOR["scaling_limits"]) if "scaling_limits" in GENERATOR else dtg.DEFAULT_SCALE_L,
                     int(GENERATOR["moving_limit"]) if "moving_limit" in GENERATOR else dtg.DEFAULT_MOVE_L,
                     int(GENERATOR["rotation_limit"]) if "rotation_limit" in GENERATOR else dtg.DEFAULT_ROTATE_L,
                     int(GENERATOR["blur_amount"]) if "blur_amount" in GENERATOR else dtg.DEFAULT_BLUR_L,
                     int(GENERATOR["erode_amount"]) if "erode_amount" in GENERATOR else dtg.DEFAULT_ERODE_L,
                     json.loads(GENERATOR["contrast_amount"]) if "contrast_amount" in GENERATOR else dtg.DEFAULT_CONTRAST_L,
                     int(GENERATOR["brightness_amount"]) if "brightness_amount" in GENERATOR else dtg.DEFAULT_BRIGHTNESS_L]
    
    except ValueError as e:
        print(e)
        exit()
    
    return inOut, generator


def __decode_filter_hash(hash):
    # special card ALL verify 
    if re.match("^ALL", hash.upper()):
        if len(hash) > 3:
            # verify if ALL card is ALL or ALL-
            if hash[3] != '-':
                raise ValueError("Special card 'ALL' not used correctly.")
            if len(hash) < 5:
                raise ValueError("Special card 'ALL' not used correctly."
                                 + "No value given after '-' card.")
            # special card ALL- verification done, create hash by removing values
            for char in hash[4:]:
                if char.upper() not in dtg.FULL_HASH:
                    raise ValueError("Special card 'ALL-' not used correctly.\n'"
                                      + str(char) + "' is not an accepted filter value.")
        return ''.join(char for char in dtg.FULL_HASH if char not in hash[4:].upper())
    
    # create hash by adding values
    for char in hash:
        if char.upper() not in dtg.FULL_HASH:
            raise ValueError("'" + str(char) + "' is not an accepted filter value.")
    return hash


def check_file_exists(name, path):
        # divide filename by name and extension
        filename, extension = os.path.splitext(name)
        i=1
        # loop while numberred file exists
        while os.path.exists(os.path.abspath(path + name)):
            name = filename + "_" + str(i) + extension
            i+=1
        return name


def gen_to_annt(generator, annotator):
    # apply matrix scaling from image to annotations
    if generator.imageFilters["S"]:
        annotator.ifScaled(generator.scale)
    # apply matrix translation from image to annotations
    if generator.imageFilters["T"]:
        annotator.ifTranslated(generator.translate)
    # apply matrix rotation from image to annotations
    if generator.imageFilters["R"]:
        annotator.ifRotated(generator.rotate)