import cv2
import imageTransformation as imgt        

def displayImage(imagePath, bbox, windowName="Image", thickness=2, colour=(0,0,255)):
    # check if path is None
    if imagePath is None:
        return -1
    
    # transform image if it is a string
    imageData = imagePath
    if type(imagePath) is str:
        imageData = imgt.setImage(imagePath)
    
    # create lines for all bounding boxes
    for box in bbox:
        cv2.line(imageData, (box[0], box[1]), (box[0]+box[2], box[1]), colour, thickness)                  # top left to top right
        cv2.line(imageData, (box[0], box[1]), (box[0], box[1]+box[3]), colour, thickness)                  # top left to bottom left
        cv2.line(imageData, (box[0]+box[2], box[1]), (box[0]+box[2], box[1]+box[3]), colour, thickness)  # top right to bottom left
        cv2.line(imageData, (box[0], box[1]+box[3]), (box[0]+box[2], box[1]+box[3]), colour, thickness)  # bottom left to bottom right
    
    # create and show windows with image
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, (1920, 1080))
    cv2.imshow(windowName, imageData)
    while 1:
        key = cv2.waitKey(0)
        if key & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
    return key

def displayImage(imagePath):
    # check if path is None
    if imagePath is None:
        return -1
    
    # transform image if it is a string
    imageData = imagePath
    if type(imagePath) is str:
        imageData = imgt.setImage(imagePath)
    
    # create and show windows with image
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Image", (1920, 1080))
    cv2.imshow("Image", imageData)
    if cv2.waitKey(0) & 0x0D:
        cv2.destroyAllWindows()
    return 0