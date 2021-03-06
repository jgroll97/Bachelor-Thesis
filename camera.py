import sys
sys.path.insert(1, "./")
import os
import bpy
from random import randint
import numpy as np
import time
import math
from PIL import Image
from config import *
import Boundingbox


print(bpy.app.version_string)

def _cleardir(dir):
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def setup_light():
    #light1
    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(3, 2, 6))
    bpy.ops.object.select_by_type(type='LIGHT')
    SIZE = 3
    bpy.context.object.data.size = SIZE
    BRIGHTNESS = 100
    bpy.context.object.data.energy = BRIGHTNESS
    #light2
    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(2, -20, 18))
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.context.object.rotation_euler[0] = 1.5708
    bpy.context.object.data.size = SIZE
    bpy.context.object.data.energy = BRIGHTNESS

    #light3
    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(2, 25, 18))
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.context.object.rotation_euler[0] = -1.5708
    bpy.context.object.data.size = SIZE
    bpy.context.object.data.energy = BRIGHTNESS

    #light4

    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(-25, 4, 15))
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.context.object.rotation_euler[0] = -1.5708
    bpy.context.object.rotation_euler[1] = 1.5708
    bpy.context.object.rotation_euler[2] = 1.5708
    bpy.context.object.data.size = SIZE
    bpy.context.object.data.energy = BRIGHTNESS

    #light5

    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(25, 4, 14))
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.context.object.rotation_euler[0] = 1.5708
    bpy.context.object.rotation_euler[1] = 1.5708
    bpy.context.object.rotation_euler[2] = 1.5708
    bpy.context.object.data.size = SIZE
    bpy.context.object.data.energy = BRIGHTNESS

    #light6

    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(3, 2, -25))
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.context.object.rotation_euler[0] = 3.14159
    bpy.context.object.data.size = SIZE
    bpy.context.object.data.energy = BRIGHTNESS



def align_object(obj):
    obj.select_set(state=True)
    bpy.context.view_layer.objects.active = obj

    if bpy.context.object.dimensions[0] > bpy.context.object.dimensions[1] and bpy.context.object.dimensions[0] > \
            bpy.context.object.dimensions[2]:
        bpy.context.object.dimensions[0] = 1
        bpy.context.object.scale[1] = bpy.context.object.scale[0]
        bpy.context.object.scale[2] = bpy.context.object.scale[0]

    if bpy.context.object.dimensions[1] > bpy.context.object.dimensions[0] and bpy.context.object.dimensions[1] > \
            bpy.context.object.dimensions[2]:
        bpy.context.object.dimensions[1] = 1
        bpy.context.object.scale[0] = bpy.context.object.scale[1]
        bpy.context.object.scale[2] = bpy.context.object.scale[1]

    if bpy.context.object.dimensions[2] > bpy.context.object.dimensions[0] and bpy.context.object.dimensions[2] > \
            bpy.context.object.dimensions[1]:
        bpy.context.object.dimensions[2] = 1
        bpy.context.object.scale[0] = bpy.context.object.scale[2]
        bpy.context.object.scale[1] = bpy.context.object.scale[2]

    # center location
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def load_objects():
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))  # create dummy

    for item in os.listdir(INPUT_MODEL_DIR):
        if item.endswith('.obj'):
            path_to_file = os.path.join(INPUT_MODEL_DIR, item)
            bpy.ops.import_scene.obj(filepath=path_to_file, split_mode="OFF")
            bpy.context.selected_objects[0].name = "Model"
            return bpy.data.objects["Model"]


def add_camera():
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW')
    bpy.context.object.name = "Camera"
    camera = bpy.data.objects["Camera"]
    bpy.ops.object.constraint_add(type='TRACK_TO')
    camera.constraints["Track To"].target = bpy.data.objects["Empty"]
    camera.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
    camera.constraints["Track To"].up_axis = 'UP_Y'
    return camera






# Actual program

start = time.time()
if os.path.exists(OUTPUT_DIR):
    _cleardir(OUTPUT_DIR)
else:
    os.mkdir(OUTPUT_DIR)
os.makedirs(OUTPUT_IMAGE_DIR)
os.makedirs(OUTPUT_BOUNDINGBOX_DIR)
os.makedirs(OUTPUT_MERGED_IMG)



clear_scene()
model = load_objects()
align_object(model)
bpy.ops.object.shade_smooth()
setup_light()
camera = add_camera()

bpy.context.scene.camera = bpy.data.objects["Camera"]
bpy.context.scene.render.engine = 'CYCLES'  # set render engine (will die with default)
bpy.context.scene.render.film_transparent = True  # transparent background

initial_pos = np.array([2, 2, 2])  # initial loc of the camera

i = 0

for alpha in np.linspace(0, 2 * math.pi, ROTATION_STEPS):
    for beta in np.linspace(0, 2 * math.pi, ROTATION_STEPS):
        for gamma in np.linspace(0, 2 * math.pi, ROTATION_STEPS):
            transformation_mat = np.array(
                [[np.cos(gamma), -np.sin(gamma), 0], [np.sin(gamma), np.cos(gamma), 0], [0, 0, 1]]) @ \
                                 np.array([[np.cos(beta), 0, np.sin(beta)], [0, 1, 0],
                                           [-np.sin(beta), 0, np.cos(beta)]]) @ \
                                 np.array([[1, 0, 0], [0, np.cos(alpha), -np.sin(alpha)],
                                           [0, np.sin(alpha), np.cos(alpha)]])

            transformed_pos = transformation_mat @ initial_pos
            camera.location = transformed_pos
            image_save = str(i)+".al= "+ str(alpha)+ " ,be= " + str(beta)+ " ,ga= "+ str(gamma)
            bpy.context.scene.render.filepath = os.path.abspath(os.path.join(OUTPUT_IMAGE_DIR, image_save))
            model.select_set(state=True)
            bpy.context.view_layer.objects.active = model
            bpy.context.scene.render.resolution_x = 512
            bpy.context.scene.render.resolution_y = 512
            bpy.context.scene.render.resolution_percentage = 100
            bpy.ops.render.render(write_still=True)
            x, y, w, h = Boundingbox.camera_view_bounds_2d(bpy.context.scene, bpy.context.scene.camera, bpy.context.object)
            dir = os.path.split(bpy.data.filepath)[0]
            Text_obj = str(i)+".al= "+ str(alpha)+ " ,be= " + str(beta)+ " ,ga= "+ str(gamma)+".txt"
            f_path = os.path.join(OUTPUT_BOUNDINGBOX_DIR, Text_obj)



            with open(f_path, "w") as f:
                c = 16

                X = x/512
                Y = y/512
                W = w/512
                H = h/512
                x2= x+ (w/2)
                y2= y+ (h/2)
                X2= x2/512
                Y2= y2/512
                M = str(c) + " " + str(X2) + " " + str(Y2) + " " + str(W) + " " + str(H)
                f.write((str(M)))

            i += 1


end = time.time() - start
print(end, "s")