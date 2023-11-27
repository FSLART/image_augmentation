import imageTransformation as imgt
import random

FULL_HASH = "BSETCRW"
DEFAULT_MAX_F = 2
DEFAULT_SCALE_L = [1.0, 3.0]
DEFAULT_MOVE_L = 50
DEFAULT_ROTATE_L = 45
DEFAULT_BLUR_L = 15
DEFAULT_ERODE_L = 6
DEFAULT_CONTRAST_L = [0.5,1.5]
DEFAULT_BRIGHTNESS_L = 35

class ImageGenerator:
    def __init__(self, filter_hash=FULL_HASH, max_filters_applied=DEFAULT_MAX_F,
                 scaling_limits=DEFAULT_SCALE_L, moving_limit=DEFAULT_MOVE_L, rotation_limit=DEFAULT_ROTATE_L,
                 blur=DEFAULT_BLUR_L, erode=DEFAULT_ERODE_L, contrast=DEFAULT_CONTRAST_L, brightness=DEFAULT_BRIGHTNESS_L):
        self.imageFilters = {
            "B":False,  # Image Blur Filter
            "E":False,  # Image Erode Filter
            "C":False,  # Image Contrast Filter
            "W":False,  # Image Brightness Filter
            "S":False,  # Image Scale Filter
            "T":False,  # Image Translate Filter
            "R":False,  # Image Rotate Filter
        }
        
        ##  transform filters to use by char (remove or add characters that exist on transformFilters)
        self.filter_hash = filter_hash                  # (default: "BSETCRW")
        ##  maximum number of transformation filters to apply for each instance of an image augmentation
        self.max_filters_applied = max_filters_applied  # (default: 2)
        ##  minimum and maximum value of scaling possible to the image, for X and Y coordinates
        self.scaling_limits = scaling_limits            # (default: [1.0, 3.0])
        ##  maximum range to move the image from the center to any side (values between 0 and 1 are recomended)
        self.moving_limit = moving_limit/100            # (default: 0.5)
        ##  maximum rotation to either side in degrees (values between 0 and 90 are recommended)
        self.rotation_limit = rotation_limit            # (default: 45)
        ##  maximum amount of blur to use when applying the filter (values between 10 and 20 recommended)
        self.blur = blur                                # (default: 15)
        ##  maximum amount of erosion to use when applying the filter (values between 4 and 10 recommended)
        self.erode = erode                              # (default: 6)
        ##  minimum and maximum value of contrast to use when applying the filter (values between 0 and 2 recommended)
        self.contrast = contrast                        # (default: [0.5, 1.5])
        ##  maximum amount of brightness to use when applying the filter (values between 10 and 100 recommended)
        self.brightness = brightness                    # (default: 35)


    def basicImageTransform(self, imagePath, scale, translate, rotate, blur, erosion, contrast, brightness):
        imageData = imagePath
        if(type(imagePath) is str):
            imageData = imgt.setImage(imagePath)

        #Blur Filter
        if(self.imageFilters["B"]):
            imageData = imgt.blurFilter(imageData, blur)
        #Erode Filter
        if(self.imageFilters["E"]):
            imageData = imgt.erodeFilter(imageData, erosion)
        #Contrast Filter
        if(self.imageFilters["C"]):
            imageData = imgt.constrastFilter(imageData, contrast)
        #Brightness Filter
        if(self.imageFilters["W"]):
            imageData = imgt.brightnessFilter(imageData, brightness)
        #Scale Filter
        if(self.imageFilters["S"]):
            imageData = imgt.scale(imageData, scale)
        #Translate Filter
        if(self.imageFilters["T"]):
            imageData = imgt.translate(imageData, translate)
        #Rotate Filter
        if(self.imageFilters["R"]):
            imageData = imgt.rotate(imageData, rotate)
        
        return imageData


    def dataGeneration(self, imagePath):
        imageData = imgt.setImage(imagePath)
        for i in range(min(self.max_filters_applied, len(self.filter_hash))):
            self.imageFilters[random.choice(self.filter_hash)] = True;

        self.scale=[random.uniform(self.scaling_limits[0],
                                    self.scaling_limits[1]),
                    random.uniform(self.scaling_limits[0],
                                    self.scaling_limits[1])]
        
        self.translate=[random.randint(-int(imageData.shape[1]*self.moving_limit),
                                        int(imageData.shape[1]*self.moving_limit)), 
                        random.randint(-int(imageData.shape[1]*self.moving_limit),
                                        int(imageData.shape[0]*self.moving_limit))]
        
        self.rotate=random.randint(-self.rotation_limit, self.rotation_limit)
        
        return self.basicImageTransform(imageData,
                            scale=self.scale,
                            translate=self.translate,
                            rotate=self.rotate,
                            blur=random.randint(min(2, self.blur), self.blur),
                            erosion=random.randint(min(2, self.erode), self.erode),
                            contrast=random.uniform(self.contrast[0], self.contrast[1]),
                            brightness=random.randint(min(1, self.brightness), self.brightness))
    
    def imageOutput(self, imageData, imageName, imagePath=""):
        if imgt.setFile(imageData, str(imagePath+imageName)) == -1:
            raise RuntimeError("File not exported successfully")