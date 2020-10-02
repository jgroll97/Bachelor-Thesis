import sys
sys.path.insert(1, "./")
import cv2
import os
import timeit
import numpy as np
import multiprocessing
import shutil
from config import *
folder = "./output/bb_merge"
object_name = "Lego2"
data= ".txt"



for file in os.listdir(folder):
    path_file = os.path.join(folder, file)
    new_file_name= file[:-4]+ "_" + object_name + data
    new_path_file = os.path.join(folder, new_file_name)
    os.rename(path_file, new_path_file)




