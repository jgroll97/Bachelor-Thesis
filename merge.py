import cv2
import os
import timeit
import numpy as np
import multiprocessing
from config import *


def make_single_merged(args):
    background, image, file_path = args
    b, g, r, a = cv2.split(image)
    image_rgb = np.dstack((b, g, r))
    mask = np.dstack((a, a, a)) / 255.0
    dst = background * (1 - mask) + image_rgb * mask
    cv2.imwrite(file_path, dst)


def make_merged():
    pool = multiprocessing.Pool()

    images = [
        cv2.imread(os.path.join(OUTPUT_IMAGE_DIR, image), cv2.IMREAD_UNCHANGED)
        for image in os.listdir(OUTPUT_IMAGE_DIR)
    ]  # load all rendered images

    w, h, c = images[0].shape  # assume that all render images are same size
    size = (h, w)  # size we resize the background to

    backgrounds = [
        cv2.resize(cv2.imread(os.path.join(INPUT_BACKGROUNDS_DIR, background), cv2.IMREAD_COLOR), size)
        for background in os.listdir(INPUT_BACKGROUNDS_DIR)
    ]  # load and resize all background images to the size of the render images

    for b, background in enumerate(backgrounds):
        pool.map(make_single_merged, [
            (background, image, os.path.join(OUTPUT_MERGED_IMG, str(b) + "_" + str(i) + ".png")) for i,
            image in enumerate(images)])


if __name__ == '__main__':
    print(timeit.timeit(make_merged, number=1))