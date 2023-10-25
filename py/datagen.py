import imageTransformation as imgt
import random

class imageGenerator:
    def __init__(self):        
        self.imageFilters = {
            "B":False,  # Image Blur Filter
            "E":False,  # Image Erode Filter
            "S":False,  # Image Scale Filter
            "T":False,  # Image Translate Filter
            "R":False   # Image Rotate Filter
        }
        
        self.filter_hash = "BESTR"         # (default: "BESTR")     ##  transform filters to use by char (remove or add characters that exist on transformFilters)          #
        self.max_filters_applied = 2       # (default: 2)           ##  maximum number of transformation filters to apply for each instance of an image augmentation        #
        self.scaling_limits = [1.0,3.0]    # (default: [1.0, 3.0])  ##  minimum and maximum value of scaling possible to the image, for X and Y coordinates                 #
        self.moving_limit = 0.5            # (default: 0.5)         ##  maximum range to move the image from the center to any side (values between 0 and 1 are recomended) #
        self.rotation_limit = 45           # (default: 45)          ##  maximum rotation to either side in degrees (values between 0 and 90 are recommended)                #
        self.blur = 15                     # (default: 15)          ##  amount of blur to use when filtering (values between 5 and 20 recommended)                          #
        self.erode = 6                     # (default: 6)           ##  amount of erosion to use when filtering (values between 2 and 10 recommended)                       #

    def basicImageTransform(self, imagePath, scale=[1,1], translate=[0,0], rotate=0, blur=1, erosion=1):
        imageData = imagePath
        if(type(imagePath) is str):
            imageData = imgt.setImage(imagePath)

        if(self.imageFilters["B"]):
            imageData = imgt.blurFilter(imageData, blur)
        if(self.imageFilters["E"]):        
            imageData = imgt.erodeFilter(imageData, erosion)
        if(self.imageFilters["S"]):
            imageData = imgt.scale(imageData, scale)
        if(self.imageFilters["T"]):
            imageData = imgt.translate(imageData, translate)
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
        self.translate=[random.randint(-round(imageData.shape[1]*self.moving_limit),
                            round(imageData.shape[1]*self.moving_limit)), 
            random.randint(-round(imageData.shape[1]*self.moving_limit),
                            round(imageData.shape[0]*self.moving_limit))]
        self.rotate=random.randint(-self.rotation_limit, self.rotation_limit)
        
        return self.basicImageTransform(imageData,
                            scale=self.scale,
                            translate=self.translate,
                            rotate=self.rotate,
                            blur=self.blur,
                            erosion=self.erode)