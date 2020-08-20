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


# TODO: set these values from program arguments


def _cleardir(dir):
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def setup_light():
    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(3, 2, 6))
    bpy.ops.object.select_by_type(type='LIGHT')
    SIZE = 5
    bpy.context.object.data.size = SIZE
    BRIGHTNESS = 1000
    bpy.context.object.data.energy = BRIGHTNESS

    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(2, -55, 18))
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.context.object.rotation_euler[0] = 1.5708
    bpy.context.object.data.size = SIZE
    bpy.context.object.data.energy = BRIGHTNESS

    # Licht3

    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(2, 55, 18))
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.context.object.rotation_euler[0] = -1.5708
    bpy.context.object.data.size = SIZE
    bpy.context.object.data.energy = BRIGHTNESS

    # Licht4

    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(-55, 4, 30))
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.context.object.rotation_euler[0] = -1.5708
    bpy.context.object.rotation_euler[1] = 1.5708
    bpy.context.object.rotation_euler[2] = 1.5708
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

    # Mittelpunkt
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


def generate_background_images():
    width, height = (1920, 1080)
    mode = 'RGB'
    my_image = Image.new(mode, (width, height))

    # Load all the pixels.
    my_pixels = my_image.load()

    # Loop through all the pixels, and set each color randomly.
    for x in range(width):
        for y in range(height):
            r = randint(0, 255)
            g = r
            b = r
            pixel = (r, g, b)
            my_pixels[x, y] = pixel
    my_image.save("./input/backgrounds/NOISE_PATTERN.png")


# Actual program

initial_pos = np.array([4, 4, 4])  # initial loc of the camera

start = time.time()
if os.path.exists(OUTPUT_DIR):
    _cleardir(OUTPUT_DIR)
else:
    os.mkdir(OUTPUT_DIR)
os.makedirs(OUTPUT_IMAGE_DIR)
os.makedirs(OUTPUT_BOUNDINGBOX_DIR)
os.makedirs(OUTPUT_MERGED_IMG)

generate_background_images()
clear_scene()
model = load_objects()
align_object(model)
bpy.ops.object.shade_smooth()  # Rundere Übergänge
setup_light()
camera = add_camera()

bpy.context.scene.camera = bpy.data.objects["Camera"]
bpy.context.scene.render.engine = 'CYCLES'  # set render engine (will die with default)
bpy.context.scene.render.film_transparent = True  # transparent background

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
            bpy.context.scene.render.filepath = os.path.abspath(os.path.join(OUTPUT_IMAGE_DIR, str(i)))
            model.select_set(state=True)
            bpy.context.view_layer.objects.active = model

            bpy.ops.render.render(write_still=True)
            i += 1
class Box:
    dim_x = 1
    dim_y = 1

    def __init__(self, min_x, min_y, max_x, max_y, dim_x=dim_x, dim_y=dim_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.dim_x = dim_x
        self.dim_y = dim_y

    @property
    def x(self):
        return round(self.min_x * self.dim_x)

    @property
    def y(self):
        return round(self.dim_y - self.max_y * self.dim_y)

    @property
    def width(self):
        return round((self.max_x - self.min_x) * self.dim_x)

    @property
    def height(self):
        return round((self.max_y - self.min_y) * self.dim_y)

    def __str__(self):
        return "<Box, x=%i, y=%i, width=%i, height=%i>" % \
               (self.x, self.y, self.width, self.height)

    def to_tuple(self):
        if self.width == 0 or self.height == 0:
            return (0, 0, 0, 0)
        return (self.x, self.y, self.width, self.height)


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))


def camera_view_bounds_2d(scene, cam_ob, me_ob):
    """
    Returns camera space bounding box of mesh object.

    Negative 'z' value means the point is behind the camera.

    Takes shift-x/y, lens angle and sensor size into account
    as well as perspective/ortho projections.

    :arg scene: Scene to use for frame size.
    :type scene: :class:`bpy.types.Scene`
    :arg obj: Camera object.
    :type obj: :class:`bpy.types.Object`
    :arg me: Untransformed Mesh.
    :type me: :class:`bpy.types.Mesh´
    :return: a Box object (call its to_tuple() method to get x, y, width and height)
    :rtype: :class:`Box`
    """

    mat = cam_ob.matrix_world.normalized().inverted()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = me_ob.evaluated_get(depsgraph)
    me = mesh_eval.to_mesh()
    me.transform(me_ob.matrix_world)
    me.transform(mat)

    camera = cam_ob.data
    frame = [-v for v in camera.view_frame(scene=scene)[:3]]
    camera_persp = camera.type != 'ORTHO'

    lx = []
    ly = []

    for v in me.vertices:
        co_local = v.co
        z = -co_local.z

        if camera_persp:
            if z == 0.0:
                lx.append(0.5)
                ly.append(0.5)
            # Does it make any sense to drop these?
            # if z <= 0.0:
            #    continue
            else:
                frame = [(v / (v.z / z)) for v in frame]

        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y

        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)

        lx.append(x)
        ly.append(y)

    min_x = clamp(min(lx), 0.0, 1.0)
    max_x = clamp(max(lx), 0.0, 1.0)
    min_y = clamp(min(ly), 0.0, 1.0)
    max_y = clamp(max(ly), 0.0, 1.0)

    mesh_eval.to_mesh_clear()

    r = scene.render
    fac = r.resolution_percentage * 0.01
    dim_x = r.resolution_x * fac
    dim_y = r.resolution_y * fac

    # Sanity check
    if round((max_x - min_x) * dim_x) == 0 or round((max_y - min_y) * dim_y) == 0:
        return (0, 0, 0, 0)

    return (
        round(min_x * dim_x),  # X
        round(dim_y - max_y * dim_y),  # Y
        round((max_x - min_x) * dim_x),  # Width
        round((max_y - min_y) * dim_y)  # Height
    )
print(camera_view_bounds_2d(bpy.context.scene, bpy.context.scene.camera, bpy.context.object))
end = time.time() - start
print(end, "s")