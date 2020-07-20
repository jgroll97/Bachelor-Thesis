# Bachelor-Thesis

Code Blender


import os
import bpy
from random import randint
import numpy as np


#Vorherige Einträge löschen
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

#Import des Obejektes
path_to_obj_dir = os.path.join('C:\\', 'C:/Users/Groll/Bachelor Thesis/Malm')


file_list = sorted(os.listdir(path_to_obj_dir))


obj_list = [item for item in file_list if item.endswith('.obj')]


for item in obj_list:
    path_to_file = os.path.join(path_to_obj_dir, item)
    bpy.ops.import_scene.obj(filepath = path_to_file, split_mode = "OFF")


#Voreinstellungen

#Mittelpunkt
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))



#Rundere Übergänge
bpy.ops.object.shade_smooth()


#Schwarzer Hintergrund
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.0100219, 0.0100219, 0.0100219, 1)

#Licht1
bpy.ops.object.light_add(type='AREA', align='WORLD', location=(3, 1.9703, 50.2477))
bpy.ops.object.select_by_type(type='LIGHT')
bpy.context.object.data.size = 89
bpy.context.object.data.energy = 10000

#Licht2
bpy.ops.object.light_add(type='AREA', align='WORLD', location=(2, -55, 18))
bpy.ops.object.select_by_type(type='LIGHT')
bpy.context.object.rotation_euler[0] = 1.5708
bpy.context.object.data.size = 89
bpy.context.object.data.energy = 10000

#Licht3
bpy.ops.object.light_add(type='AREA', align='WORLD', location=(2, 55, 18))
bpy.ops.object.select_by_type(type='LIGHT')
bpy.context.object.rotation_euler[0] = -1.5708
bpy.context.object.data.size = 89
bpy.context.object.data.energy = 10000

#Licht4
bpy.ops.object.light_add(type='AREA', align='WORLD', location=(-55, 4, 30))
bpy.ops.object.select_by_type(type='LIGHT')
bpy.context.object.rotation_euler[0] = -1.5708
bpy.context.object.rotation_euler[1] = 1.5708
bpy.context.object.rotation_euler[2] = 1.5708
bpy.context.object.data.size = 89
bpy.context.object.data.energy = 10000

#Licht5
bpy.ops.object.light_add(type='AREA', align='WORLD', location=(55, 4, 30))
bpy.ops.object.select_by_type(type='LIGHT')
bpy.context.object.rotation_euler[0] = 1.5708
bpy.context.object.rotation_euler[1] = 1.5708
bpy.context.object.rotation_euler[2] = 1.5708
bpy.context.object.data.size = 89
bpy.context.object.data.energy = 10000

#Licht6
bpy.ops.object.light_add(type='AREA', align='WORLD', location=(3, 1.9703, -50.2477))
bpy.ops.object.select_by_type(type='LIGHT')
bpy.context.object.rotation_euler[0] = 3.14159
bpy.context.object.data.size = 89
bpy.context.object.data.energy = 10000

number1 = -20
number2 = 20

angle1=-6
angle2=6

G = 1

while G in range(0,15):

    bpy.data.scenes[0]

    for i in range (number1, number2):
        x = randint(number1, number2)
        y = randint(number1, number2)
        z = randint(number1, number2)
        


    for a in range(angle1, angle2):
        A = randint(angle1, angle2)
        B = randint(angle1, angle2)
        C = randint(angle1, angle2)
        
    bpy.context.scene.render.filepath = "C:/Users/Groll/Documents/Blender Versuche/Bild"+str(G)
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(x, y, z), rotation=(A,B,C))
    bpy.context.object.name = "Camera."+str(G)
    #bpy.context.object.data.name = "Camera."+str(G)
    bpy.context.scene.camera = bpy.data.objects["Camera."+str(G)]
    
    bpy.ops.object.constraint_add(type='TRACK_TO')
    bpy.context.object.constraints["Track To"].target = bpy.data.objects["Empty"]
    bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
    bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'
    
    bpy.ops.render.render(write_still=True )
        
    G = G +1


