import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
from config import *
import os

for image in os.listdir(OUTPUT_MERGED_IMG):


    im = np.array(Image.open("C:/Users/Groll/PycharmProjects/Bachelor-Thesis/output/merged_img/" + image), dtype=np.uint8)

    # Create figure and axes
    fig,ax = plt.subplots(1)

    # Display the image
    ax.imshow(im)

    # Create a Rectangle patch
    rect = patches.Rectangle((197, 208), 103, 70,linewidth=1.5,edgecolor='r',facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)

    plt.show()


