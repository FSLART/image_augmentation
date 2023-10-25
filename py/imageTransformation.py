import numpy as np
import cv2

##### SET IMAGE STRING TO IMAGE MATRIX #####
def setImage(imagePath=''):
    imgM = cv2.imread(imagePath)
    assert imgM is not None, "Error: File not found: Image file path could not be read"
    return imgM


##### IMAGE GEOMETRIC TRANSFORMATIONS #####
## image scaling - resizing ##
def scale(image, scale=[1,1]):
    if(type(image) is str):
        image = setImage(image)
        
    return cv2.resize(image,
                      None,
                      fx=scale[0],
                      fy=scale[1],
                      interpolation = cv2.INTER_LINEAR)

## image translation - moving ##
def translate(image, translate=[0,0]):
    if(type(image) is str):
        image = setImage(image)
        
    return cv2.warpAffine(image,
                          np.float32([[1, 0, translate[0]],[0, 1, translate[1]]]),
                          (image.shape[1], image.shape[0]))

## image rotation ##
def rotate(image, rotateDegrees=0):
    if(type(image) is str):
        image = setImage(image)
        
    rotationFilter = cv2.getRotationMatrix2D(((image.shape[1]-1)/2.0,(image.shape[0]-1)/2.0),
                                             rotateDegrees,
                                             1)
    return cv2.warpAffine(image,
                          rotationFilter,
                          (image.shape[1], image.shape[0]))

## image three point shift ##
#Additional description:
# Select 3 parallel points on the original image
# and 3 new points to move the original ones to
# the new points location
def parallelShift(image, originPoints=[[0,0],[0,0],[0,0]], shiftedPoints=[[0,0],[0,0],[0,0]]):
    if(type(image) is str):
        image = setImage(image)
        
    return cv2.warpAffine(image,
                          cv2.getAffineTransform(np.float32(originPoints), np.float32(shiftedPoints)),
                          (image.shape[1], image.shape[0]))

## image perspective shift##
#Additional description:
# Select 4 origin points that have the area of
# the desired object and 4 coordinates to
# create an image with the 4 coordinates size
# of the given area of the origin points
def perspectiveShift(image, perspectivePoints=[[0,0],[0,0],[0,0],[0,0]], finalImageSize=[0,0]):
    if(type(image) is str):
        image = setImage(image)
        
    perspectiveFinalSize=[finalImageSize,
                         [finalImageSize[0], 0],
                         [0, finalImageSize[1]],
                         [finalImageSize[0], finalImageSize[1]]]
    return cv2.warpPerspective(image,
                               cv2.getPerspectiveTransform(np.float32(perspectivePoints), np.float32(perspectiveFinalSize)),
                               (image.shape[1], image.shape[0]))

##### IMAGE FILTERING #####
def blurFilter(image, blurSize=1):
    if(type(image) is str):
        image = setImage(image)
        
    return cv2.filter2D(image, -1,
                        np.ones((blurSize, blurSize), np.float32)/(blurSize*blurSize))
    
def erodeFilter(image, erodeSize=1):
    if(type(image) is str):
        image = setImage(image)
        
    
    return cv2.erode(image, np.ones((erodeSize, erodeSize), np.uint8))