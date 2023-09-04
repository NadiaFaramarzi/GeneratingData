import sys
sys.path.append("C:/Users/nadia/Documents/DFace-master")

import argparse
import numpy as np
import cv2
import os
import numpy.random as npr
from dface.core.utils import IoU
import dface.config as config

def gen_onet_data(data_dir,anno_file,prefix):

    pos_save_dir =  os.path.join(data_dir,"48/mask_positive")

    for dir_path in [pos_save_dir]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    save_dir = os.path.join(data_dir,"onet")
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    post_save_file = os.path.join(config.ANNO_STORE_DIR,config.ONET_MASK_POSTIVE_ANNO_FILENAME)
    
    f1 = open(post_save_file, 'w')
    
    with open(anno_file, 'r') as f:
        annotations = f.readlines()

    num = len(annotations)
    print("%d pics in total" % num)
    p_idx = 0
    n_idx = 0
    d_idx = 0
    idx = 0
    box_idx = 0
    for annotation in annotations:
        annotation = annotation.strip().split(' ')
        im_path = os.path.join(prefix,annotation[0])
        bbox = list(map(float, annotation[1:]))
        boxes = np.array(bbox, dtype=np.int32).reshape(-1, 4)
        img = cv2.imread(im_path)
            
        idx += 1
        if idx % 50 == 0:
            print(idx, "images done")
        try:
            height, width, channel = img.shape
        except:
            continue

        
        for box in boxes:
            # box (x_left, y_top, x_right, y_bottom)
            x1, y1, x2, y2 = box
            w = x2 - x1 + 1
            h = y2 - y1 + 1

            # ignore small faces
            # in case the ground truth boxes of small faces are not accurate
            if max(w, h) < 40 or x1 < 0 or y1 < 0:
                continue

            # generate positive examples and part faces
            for i in range(4):
                #size = npr.randint(int(min(w, h) * 0.8), np.ceil(1.25 * max(w, h)))
                size = int(max(w, h))
                #new_w = w
                #new_h = h
                
                if i==0:
                # delta here is the offset of box center
                    delta_y = npr.randint(h * 0.1, h * 0.2)
                    delta_x = 0
            
                elif i==1:
                    delta_y = 0
                    delta_x = npr.randint(w * 0.1, w * 0.2) 
                    
                elif i==2:
                    delta_y = npr.randint(h * 0.1, h * 0.2) * -1
                    delta_x = 0
                    
                else:
                    delta_y = 0
                    delta_x = npr.randint(w * 0.1, w * 0.2) * -1
                
                
                
                
                nx1 = x1+delta_x
                ny1 = y1 +delta_y
                nx2 = nx1 + size
                ny2 = ny1 + size

                if nx2 > width or ny2 > height or nx1<0 or ny1<0:
                    continue
                crop_box = np.array([nx1, ny1, nx2, ny2])

                offset_x1 = (x1 - nx1) / float(size)
                offset_y1 = (y1 - ny1) / float(size)
                offset_x2 = (x2 - nx2) / float(size)
                offset_y2 = (y2 - ny2) / float(size)

                cropped_im = img[ny1 : ny2, nx1 : nx2, :]
                resized_im = cv2.resize(cropped_im, (48, 48), interpolation=cv2.INTER_LINEAR)

                box_ = box.reshape(1, -1)
                
                save_file = os.path.join(pos_save_dir, "%s.jpg"%p_idx)
                f1.write(save_file + ' 1 %.2f %.2f %.2f %.2f\n'%(offset_x1, offset_y1, offset_x2, offset_y2))
                cv2.imwrite(save_file, resized_im)
                p_idx += 1
            box_idx += 1
    print("%s images done, pos: %s part: %s neg: %s"%(idx, p_idx, d_idx, n_idx))

    f1.close()


def parse_args():
    parser = argparse.ArgumentParser(description='Test mtcnn',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--dface_traindata_store', dest='traindata_store', help='dface train data temporary folder,include 12,24,48/postive,negative,part,landmark',
                        default='../data/wider/', type=str)
    parser.add_argument('--anno_file', dest='annotation_file', help='wider face original annotation file',
                        default=os.path.join(config.ANNO_STORE_DIR,"anno_mask.txt"), type=str)
    parser.add_argument('--prefix_path', dest='prefix_path', help='annotation file image prefix root path',
                        default='E:/Mask_Data/GenDataMask', type=str)




    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    gen_onet_data(args.traindata_store,'E:/Mask_Data/anno_rotated.txt','E:/Mask_Data/Rotated')
