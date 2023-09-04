import cv2 
import os
import numpy as np
import matplotlib.pyplot as plt

#for next image tap enter
#for relocating bounding boxes tap C
#for finishing the process tap ESC

def click_event(event, x, y, flags,params): 
    global rectangle
    if event == cv2.EVENT_LBUTTONDOWN: 
        rectangle.append((x,y))
        cv2.circle(img, rectangle[-1], 3, (0,255,255), -1) 
        if len(rectangle)>1 and len(rectangle)%2==0:
            cv2.rectangle(img, rectangle[-2], rectangle[-1], (0,0,255), 2) 

if __name__=="__main__": 
    images=[]
    global rectangle
    rectangle=[]
    reclist=[]
    dir='G:/cattle/Camera'
    text_file='G:/cattle/bounding_boxes.txt'
    for f_name in os.listdir(dir):
        if f_name.endswith('.jpg'):
            images.append(os.path.join( dir,f_name))
    
    cv2.imshow('image',0)
    cv2.setMouseCallback('image', click_event,(rectangle)) 
    key=0
    for i in images:
        if key==27:
            break
        img=cv2.imread(i)
        _,height,width=img.shape
        clone=img.copy()
        rectangle=[]
        key=0
        while(key != 13):
            img=cv2.resize(img, (500, 500))
            cv2.imshow('image', img) 
            
            cv2.moveWindow('image', 100, 100)
            key=cv2.waitKey(10)
            if key==ord('c') or key==ord('C'): #character 'c'
                rectangle=[]
                img=clone.copy()
            if key==27:
                break
        coordinates=" ".join([str(item) for x in rectangle for item in x])
        print(i,coordinates) 
        if (len(coordinates) != 0):
            with open(text_file, 'a') as f:
                f.write("%s %s \n"%(i, coordinates))  
            f.close() 
        reclist.append(rectangle)
    k=0
        