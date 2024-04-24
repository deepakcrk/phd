import json
import os
import cv2
import sys

#os.system("rm -fr output/")
os.system("mkdir -p output/")
os.system("rm -fr result.txt")
f = open('cocotext.v2.json')
 
data = json.load(f)

#print (type(data))
#print (data.keys())

imgids = {}
imgset = {}

imgs = data['imgs']

for k, v in imgs.items():
    
    id1 = v['id']
    fn = v['file_name']
    set1 = v['set']
    #print (k, v)
    #print (k, set1, fn, id1)
    if k not in imgids.keys():
        imgids[id1] = fn
        imgset[id1] = set1


anns = data['anns']

nn = 100000
nn1 = nn

out_file = open("result.txt", "w") 

for k, v in anns.items():
    cls = v['class'] # machine printed / hand
    box = v['bbox'] 
    id2 = v['image_id'] 
    id1 = v['id'] 
    lang = v['language']
    word = v['utf8_string']
    legi = v['legibility']
    
    if len(word) < 1:
        continue

    fn = imgids[id2]
    set1 = imgset[id2]

    #print (cls, id1, id2, lang, word, legi)
    #print (fn, set1)
    #print ("--")

    fn2 = "train2014/" + fn
    img = cv2.imread(fn2)
    #print (img.shape)

    #crop
    x, y, w, h = box
    x, y, w, h = int(x), int(y), int(w+0.5), int(h+0.5)
    if x<0:
        x = 0
    if y<0:
        y = 0
    if w < 1 or h < 0:
        continue
    crop = img[y:y+h, x:x+w]
    
    #print (img.shape)
    #print (x, y, w, h, "==", y+h, x+w)
    
    #if len(word) < 5:
    #    continue
    #if w < 100 or h < 50:
    #    continue
    
    if nn%1000 == 0:
        print ("Saved", nn - nn1)
    nn = nn + 1    
    q = "_"
    suff = set1 + q + cls + q + str(id1) + q + str(id2) + q + lang + q + legi + q + str(nn) + "___" + word
    suff = suff.replace(" ", "")

    crop_fn = "output/" + fn.replace(".jpg", "___") + suff + ".jpg"
    #print (crop_fn)

    cv2.imwrite(crop_fn, crop)
    #print (fn2)
    #sys.exit()
    out = crop_fn  + "," + word + "\n"
    out_file.write(out)

out_file.close()

print ("Output: images saved in output/")
print ("Output: result.txt")

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

