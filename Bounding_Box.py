import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
from config import *
import os

for image in os.listdir(OUTPUT_MERGED_IMG):


    im = np.array(Image.open('C:/Users/Groll/PycharmProjects/Blender Code/output/merged_img/'+ image), dtype=np.uint8)

    # Create figure and axes
    fig,ax = plt.subplots(1)

    # Display the image
    ax.imshow(im)

    # Create a Rectangle patch
    rect = patches.Rectangle((758, 423),415, 283,linewidth=1,edgecolor='r',facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)

    plt.show()


