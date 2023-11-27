import random
import json
import re
import math
import gc

class Annotation:
    def __init__(self, cocoPath="./fsoco.json", fileName=""):
        fp = open(cocoPath)
        fileString = fp.read()
        fp.close()
        
        try:
            param_start = fileString.index(fileName)
            param_end = fileString.index('}', param_start)
            params = fileString[param_start:param_end]
        except ValueError:
            print("File(image) of name ["+fileName+"] does not exist on "+cocoPath)
        fp.close()
        
        self.coco=cocoPath
        self.name=fileName
        self.width=int((re.search('"width": (.*?),' , params)).group(1))
        self.height=int((re.search('"height": (.*?),' , params)).group(1))

        annts = self.annts = []
        subAnnt = '"image_id": '+str((re.search('"id": (.*)' , params)).group(1))
        for subStr in re.finditer(subAnnt, fileString):
            try:
                boxValues_start = subStr.end()+1
                boxValues_end = fileString.index('}', boxValues_start)
                boxValues = fileString[boxValues_start:boxValues_end]
                bbox = (re.search('"bbox": \[(.*?)\]', boxValues)).group(1)
            except ValueError:
                print("Annotation values from file(image) of name ["+fileName+"] does not exist on "+cocoPath)
                
            annts.append({
                "category_id": int((re.search('"category_id": (.*?),', boxValues)).group(1)),
                "bbox": [eval(i) for i in bbox.split(',')],
                "area": int((re.search('"area": (.*?),', boxValues)).group(1)),
                "iscrowd": int((re.search('"iscrowd": (.*?),' , boxValues)).group(1))
            })
        del fileString
        gc.collect()
    # End of __init__
    
    
    ## Create a json file for coco    
    def imageJSON(self, newname, cocoPath=""):
        id = random.randint(200000000, 1000000000)
        fileNotes = [{'file_name': newname,
                     'width': self.width,
                     'height': self.height,
                     'id': id}]
        annotationNotes = [{'id': id + random.randint(100, 2000),
                           'image_id': id,
                           'category_id': i["category_id"],
                           'bbox': i["bbox"],
                           'area': i["area"],
                           'iscrowd': i["iscrowd"]} for i in self.annts]
        fp = open(self.coco)
        fileString = fp.read()
        fp.close()
        
        try:
            categories_start = fileString.index('[')
            categories_end = fileString.index(']', categories_start)+1
            categories = fileString[categories_start:categories_end]
            del fileString
            gc.collect()
        except ValueError:
            print("File(image) of name ["+self.name+"] does not exist on "+self.coco)
            return -1
        
        data = "{'categories': " + str(json.loads(categories)) + ", 'images': " + str(fileNotes) + ", 'annotations': " + str(annotationNotes) + "}"
        data = data.replace("\'", "\"")
        with open(cocoPath+"coco_"+newname+".json", "w") as file:
            json.dump(json.loads(data), file)
        
        return 0;
    # End of imageJson
        
    ## If image was scaled apply this geometric alteration to get new bounding boxes' locations ##
    def ifScaled(self, scale=[1,1]):
        # FROM PARAMS
        self.width = int(self.width*scale[0])
        self.height = int(self.height*scale[1])
        
        # FROM ANNOTATIONS
        for annt in self.annts:
            annt["bbox"][0] = int(annt["bbox"][0]*scale[0])
            annt["bbox"][1] = int(annt["bbox"][1]*scale[1])
            annt["bbox"][2] = int(annt["bbox"][2]*scale[0])
            annt["bbox"][3] = int(annt["bbox"][3]*scale[1])
            annt["area"] = int(annt["bbox"][2]*annt["bbox"][3])
    # End of ifScaled
            
    ## If image was translated apply this geometric alteration to get new bounding boxes' locations ##
    def ifTranslated(self, tranlation=[0,0]):
        toRemove = []
        for anntValues in self.annts:
            anntValues["bbox"][0] += int(tranlation[0])
            anntValues["bbox"][1] += int(tranlation[1])
            
            if (anntValues["bbox"][0]+anntValues["bbox"][2] > self.width) or anntValues["bbox"][0] < 0:
                toRemove.append(anntValues)
            if (anntValues["bbox"][1]+anntValues["bbox"][3] > self.height) or anntValues["bbox"][1] < 0:
                if anntValues not in toRemove:
                    toRemove.append(anntValues)
        
        self.annts = [i for i in self.annts if i not in toRemove]
    # End of ifTranslated

    ## If image was rotated apply this geometric alteration to get new bounding boxes' locations ##
    def ifRotated(self, rotation):
        radianation = math.radians(rotation) # rotation in degrees to radians
        
        # Set center of rotation
        centerX=(self.width-1)/2
        centerY=(self.height-1)/2
        
        # Set rotation values
        radCos = math.cos(radianation)
        radSin = math.sin(radianation)
        
        toRemove = []
        for anntValues in self.annts:
            
            # Var original values for better understanding and optimization
            x, y, width, height = anntValues["bbox"] # old box values
            
            # Shifted x and y
            shiftedX = x-centerX
            shiftedY = centerY-y
            
            # Change old box coordinate point to new
            anntValues["bbox"][0] = int(centerX +shiftedX*radCos -shiftedY*radSin)
            anntValues["bbox"][1] = int(centerY -shiftedX*radSin -shiftedY*radCos)
            
            ## Create new unrotated rectangle to accommodate rotated rectangle
            # reposition X or Y coordinate for new box size
            if rotation > 0:
                anntValues["bbox"][1] -= int(width*abs(radSin))
            else:
                anntValues["bbox"][0] -= int(height*abs(radSin))
            
            # Change box size to accomodate new unrotated rectangle
            anntValues["bbox"][2] = int(width*abs(radCos) + height*abs(radSin))
            anntValues["bbox"][3] = int(height*abs(radCos) + width*abs(radSin))
            
            anntValues["area"] = anntValues["bbox"][2] * anntValues["bbox"][3]
            
            if (anntValues["bbox"][0]+anntValues["bbox"][2] > self.width) or anntValues["bbox"][0] < 0:
                toRemove.append(anntValues)
            if (anntValues["bbox"][1]+anntValues["bbox"][3] > self.height) or anntValues["bbox"][1] < 0:
                if anntValues not in toRemove:
                    toRemove.append(anntValues)
        
        self.annts = [i for i in self.annts if i not in toRemove]
    # End of ifRotated