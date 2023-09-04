import os
from PIL import Image
import pylab
import random

text_file='E:/Mask_Data/anno_mask.txt'
Aligned_Path="E:/MLFW/aligned"
w=112
i=0


        

for align in os.listdir(Aligned_Path):
    if align.endswith(".jpg"):
        img=Image.open(os.path.join(Aligned_Path,align))
        
        
        Back_Path=random.choice([x for x in os.listdir('C:/Users/nadia/Pictures/BackGround')])
        Back_Ground=Image.open(os.path.join('C:/Users/nadia/Pictures/BackGround',Back_Path))
        shape=Back_Ground.size
        img=img.resize((w,w))
        
        x1=random.randint(1,shape[0]-w)
        y1=random.randint(1,shape[1]-w)
        x2 = x1 + w
        y2 = y1 + w
        Back_Ground.paste(img,(x1,y1))
        Back_Ground.save("E:\Mask_Data\GenDataMask/%s"%(align),"JPEG")
        with open(text_file, 'a') as f:
            f.write("E:/Mask_Data/GenDataMask/%s %d %d %d %d \n"%(align, x1, y1, x2, y2))
        f.close()
        i += 1
        if i %100==0:
            print('done ',i)
        #img.show()

            
        
'''        
l=[]        
for j in range(5):
    for i in range(10):
        num=random.choice(range(00, 100))
        l.append(num)
print(l)'''
'''figure = pylab.figure()
pylab.imshow(img)
pylab.show()'''