import random
import json
import re
import math

COCO_ANNOTATIONS="fsoco.json"

class Annotation:
    def __init__(self, jsonPath="./"+COCO_ANNOTATIONS, fileName=""):
        fp = open(jsonPath)
        fileString = fp.read()
        try:
            param_start = fileString.index(fileName)
            param_end = fileString.index('}', param_start)
            params = fileString[param_start:param_end]
        except ValueError:
            print("File(image) of name ["+fileName+"] does not exist on "+jsonPath)
        
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
                print("Annotation values from file(image) of name ["+fileName+"] does not exist on "+jsonPath)
                
            annts.append({
                "category_id": int((re.search('"category_id": (.*?),', boxValues)).group(1)),
                "bbox": [eval(i) for i in bbox.split(',')],
                "area": int((re.search('"area": (.*?),', boxValues)).group(1)),
                "iscrowd": int((re.search('"iscrowd": (.*?),' , boxValues)).group(1))
            })

        
    def imageJson(self, outputJson="fsoco.json"):
        id = random.randint(200000000, 300000000)
        fileNotes = {"file_name": '"'+self.name+'"',
                     "width": self.width,
                     "height": self.height,
                     "id": id}
        annotationNotes = [{"id": id + random.randint(100, 2000),
                           "image_id": id,
                           "category_id": i["category_id"],
                           "bbox": i["bbox"],
                           "area": i["area"],
                           "iscrowd": i["iscrowd"]} for i in self.annts]
        
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
            
    def ifTranslated(self, tranlation=[0,0]):
        for anntValues in self.annts:
            anntValues["bbox"][0] += int(tranlation[0])
            anntValues["bbox"][1] += int(tranlation[1])
            
            if (anntValues["bbox"][0]+anntValues["bbox"][2] > self.width) or anntValues["bbox"][0] < 0:
                self.annts.remove(anntValues)
            if (anntValues["bbox"][1]+anntValues["bbox"][3] > self.height) or anntValues["bbox"][1] < 0:
                if anntValues in self.annts:
                    self.annts.remove(anntValues)

    def ifRotated(self, rotation=0):
        for anntValues in self.annts:
            # Change old box coordinate point to new
            anntValues["bbox"][0] = int((anntValues["bbox"][0] - (self.width-1)/2) * math.cos(rotation) - (anntValues["bbox"][1] - (self.height-1)/2) * math.sin(rotation) + (self.width-1)/2)
            anntValues["bbox"][1] = int((anntValues["bbox"][0] - (self.width-1)/2) * math.sin(rotation) - (anntValues["bbox"][1] - (self.height-1)/2) * math.cos(rotation) + (self.height-1)/2)
            
            # Move new point to parallel box
            anntValues["bbox"][1] -= int(anntValues["bbox"][2]*math.sin(rotation))
            
            # # Change 
            anntValues["bbox"][2] = int(anntValues["bbox"][2]*math.cos(rotation)+anntValues["bbox"][3]*math.sin(rotation))
            anntValues["bbox"][3] = int(anntValues["bbox"][3]*math.cos(rotation)+anntValues["bbox"][2]*math.sin(rotation))
                        
            if (anntValues["bbox"][0]+anntValues["bbox"][2] > self.width) or anntValues["bbox"][0] < 0:
                self.annts.remove(anntValues)
            if (anntValues["bbox"][1]+anntValues["bbox"][3] > self.height) or anntValues["bbox"][1] < 0:
                self.annts.remove(anntValues)
            
            anntValues["area"] = int(anntValues["bbox"][2]*anntValues["bbox"][3])

def createJson(categories=[]):
    annotations = { "categories": categories,
                    "images": [],
                    "annotations": []}
    
    # transform to json
    with open(COCO_ANNOTATIONS, "w") as outfile:
        outfile.write(json.dumps(annotations))
