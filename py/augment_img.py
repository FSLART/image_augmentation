import datagen as dtg
import visualise as vis
import annotations as annt

IMAGE_AUG_NUM=10
IMAGE_PATH="images/amz_00807.png"
COCO_PATH="annotations/fsoco_val.json"

gen = dtg.imageGenerator()
noter = annt.Annotation(COCO_PATH, "amz_00807.png")

imageData = gen.dataGeneration(imagePath=IMAGE_PATH)

if gen.imageFilters["S"]:
    noter.ifScaled(gen.scale)
if gen.imageFilters["T"]:
    noter.ifTranslated(gen.translate)
if gen.imageFilters["R"]:
    noter.ifRotated(gen.rotate)

vis.displayImage(imageData, [i["bbox"] for i in noter.annts], thickness=3)

# For future json creation
# "categories" default:
# [{"id": 9993514, "name": "unknown_cone"}, {"id": 9993506, "name": "yellow_cone"}, {"id": 9993511, "name": "blue_cone"}, {"id": 9993512, "name": "orange_cone"}, {"id": 9993513, "name": "large_orange_cone"}]
