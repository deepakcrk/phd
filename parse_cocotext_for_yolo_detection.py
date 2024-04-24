import json
import os
import cv2
import sys

os.system("mkdir -p yolo_output/train2017/")
os.system("mkdir -p yolo_output/val2017/")

f = open('cocotext.v2.json')
 
data = json.load(f)

imgids = {}
imgset = {}

imgs = data['imgs']

for k, v in imgs.items():
    
    id1 = v['id']
    fn = v['file_name']
    set1 = v['set']
    if k not in imgids.keys():
        imgids[id1] = fn
        imgset[id1] = set1

anns = data['anns']

for k, v in anns.items():
    cls = v['class'] # machine printed / hand
    box = v['bbox'] 
    id2 = v['image_id'] 
    id1 = v['id'] 
    lang = v['language']
    word = v['utf8_string']
    legi = v['legibility']
    
    fn = imgids[id2]
    set1 = imgset[id2]

    fn2 = "train2014/" + fn
    img = cv2.imread(fn2)
    hh, ww, cc = img.shape
    #print (img.shape)

    x, y, w, h = box
    
    if x<0:
        x = 0
    if y<0:
        y = 0
    if w < 1 or h < 1:
        continue
    
    cx = x + w / 2.0
    cy = y + h / 2.0

    cx = cx / ww
    cy = cy / hh
    w = w / ww
    h = h / hh
    
    cx = str(cx)
    cy = str(cy)
    w = str(w)
    h = str(h)

    q = " "
    ss =  "0 " + cx + q + cy + q + w + q + h + "\n" 

    fn2 = fn.replace(".jpg", ".txt") 

    write_file = "yolo_output/train2017/" + fn2
    
    if set1 == "val":
        write_file = "yolo_output/val2017/" + fn2

    with open(write_file, "a") as filex:
        filex.write(ss)


"""
  "anns": {
    "45346": {
      "class": "machine printed",
      "bbox": [ 468.9, 286.7, 24.1, 9.1 ],
      "image_id": 217925,
      "id": 45346,
      "language": "english",
      "area": 206.06,
      "utf8_string": "New",
      "legibility": "legible"
    }
"""

