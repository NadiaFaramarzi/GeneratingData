import cv2
import numpy as np
import os
import numpy.random as npr

anno_file='E:/Mask_Data/anno_mask.txt'
prefix ='E:/Mask_Data/GenDataMask'
text_file='E:/Mask_Data/anno_rotated.txt'

with open(anno_file, 'r') as f:
    annotations = f.readlines()

i=0
   
for annotation in annotations:
    
        if i% 100==0:
            print('%d images done'%(i))
    
        annotation = annotation.strip().split(' ')
        im_path = os.path.join(prefix,annotation[0])
        bbox = list(map(float, annotation[1:]))
        boxes = np.array(bbox, dtype=np.int32).reshape(-1, 4)
        img = cv2.imread(im_path)
        
        x1, y1, x2, y2 = boxes[0]
        w = x2 + x1
        h = y2 + y1
        (cX, cY) = (int(w // 2), int(h //2))
        
        img_name=im_path.strip().split('/')[-1]
        
        degreeP= npr.randint(9,15)
        MP = cv2.getRotationMatrix2D((cX, cY), degreeP, 1.0)
        rotatedP = cv2.warpAffine(img, MP, (w, h))
        
        #cv2.rectangle(rotated, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
        #cv2.imshow("Rotated by 15 Degrees", rotatedP)
        cv2.imwrite("E:\Mask_Data\Rotated/2_%s"%(img_name),rotatedP)

        degreeN = npr.randint(-15,-9)
        MN = cv2.getRotationMatrix2D((cX, cY), degreeN, 1.0)
        rotatedN = cv2.warpAffine(img, MN, (w, h))
        
        #cv2.rectangle(rotated, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
        #cv2.imshow("Rotated by -15 Degrees", rotatedN)
        cv2.imwrite("E:\Mask_Data\Rotated/3_%s"%(img_name),rotatedN)
        
        #cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
        #cv2.imshow("the main image", img)
        cv2.imwrite("E:\Mask_Data\Rotated/1_%s"%(img_name),img)
        #cv2.waitKey(0)
        
        with open(text_file, 'a') as f:
            f.write("E:/Mask_Data/Rotated/1_%s %d %d %d %d \n"%(img_name, x1, y1, x2, y2))
            f.write("E:/Mask_Data/Rotated/2_%s %d %d %d %d \n"%(img_name, x1, y1, x2, y2))
            f.write("E:/Mask_Data/Rotated/3_%s %d %d %d %d \n"%(img_name, x1, y1, x2, y2))
        f.close()
        i += 1
    
    
'''start_x, start_y, end_x, end_y=boxes[0] 
    
img_bg = cv2.imread('E:\Mask_Data\Rotated/1_Aaron_Eckhart_0001_0000.jpg')
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
thickness = 2

(w, h), baseline = cv2.getTextSize('hello', font, font_scale, thickness)
#cv2.rectangle(img_bg, (int(start_x), int(start_y - (2 * baseline + 5))), (int(start_x + w), int(start_y)), (0, 255, 255), -1)
cv2.rectangle(img_bg, (int(start_x), int(start_y)), (int(end_x), int(end_y)), (0, 255, 255), 2)
#cv2.putText(img_bg, str(confidence), (int(start_x), int(start_y)), font, font_scale, (0, 0, 0), thickness)

img_resized=cv2.resize(img_bg, (960, 680)) 
cv2.imshow('NMS', img_resized)
cv2.waitKey(0)'''