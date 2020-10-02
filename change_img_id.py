import cv2
import os
import timeit
import numpy as np
import multiprocessing
import shutil
from config import *
path = "./output/bb_merge"
img_id= 16

for file in os.listdir(path):
    f_path= os.path.join(path, file)
    f= open(f_path, "r+")
    f.seek(2)
    text=f.readline()
    #print(text)
    f.close()

    k = open(f_path, "w")
    k.write(str(img_id) + " " + text)
    k.close()

    k = open(f_path, "r")
    text2= k.readline()
    #print(text2)


