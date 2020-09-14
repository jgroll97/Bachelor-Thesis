import sys
sys.path.insert(1, "./")
import cv2
import os
import timeit
import numpy as np
import multiprocessing
import shutil
from config import *


path = "./output/merged_img"
path2 = "./output/boundingbox"
for m in os.listdir(path):
    for bb in os.listdir(path2):
        path_m = os.path.join(OUTPUT_MERGED_IMG, m)
        path_bb = os.path.join(OUTPUT_BOUNDINGBOX_DIR, bb)

        single_m = m.split(".")
        print(single_m[0])
        m_background = m.split(" ")
        #print(m_background[3])
        single_bb= bb.split(".")
        #print(single_bb[0])
        pre_m = m.split("= ")
        #print(pre_m[3])
        #print(m)

        if single_m[0] == single_bb[0]:
            src = path_bb
            dst = OUTPUT_MERGED_IMG
            shutil.copy(src, dst)

            dst_file = os.path.join(dst, bb)
            new_name = m + ".txt"
            new_dst_file_name = os.path.join(dst, new_name)
            os.rename(dst_file, new_dst_file_name)


