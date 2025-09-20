import bpy
import numpy as np


def add_texture_node(nodes, path, colorspace='sRGB'):
    tex_node = nodes.new("ShaderNodeTexImage")
    img = bpy.data.images.load(path)
    tex_node.image = img
    tex_node.image.colorspace_settings.name = colorspace
    return tex_node

def transformation(obj, location=None, scale=None, rotation_euler=None):
    if scale:
        obj.scale = scale
    if rotation_euler:
        obj.rotation_euler = rotation_euler
    if location:
        obj.location = location


# ====== Build table and chair ======
obj = bpy.context.scene.objects["chair"]
dim = obj.dimensions
transformation(
    obj,
    location=(0, 2.2, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(180))
)
obj = bpy.context.scene.objects["chair_copy1"]
dim = obj.dimensions
transformation(
    obj,
    location=(0-1.5, 2.2, dim.z/2)
)

obj = bpy.context.scene.objects["chair_copy2"]
dim = obj.dimensions
transformation(
    obj,
    location=(0, 1.1, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(0))
)

obj = bpy.context.scene.objects["chair_copy3"]
dim = obj.dimensions
transformation(
    obj,
    location=(0-1.5, 1.1, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(0))
)
obj = bpy.context.scene.objects["chair_copy4"]
dim = obj.dimensions
transformation(
    obj,
    location=(-3.5, 1.1, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(0))
)
obj = bpy.context.scene.objects["chair_copy5"]
dim = obj.dimensions
transformation(
    obj,
    location=(-3.5-1.5, 1.1, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(0))
)
obj = bpy.context.scene.objects["chair_copy6"]
dim = obj.dimensions
transformation(
    obj,
    location=(-3.5, 2.2, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(180))
)
obj = bpy.context.scene.objects["chair_copy7"]
dim = obj.dimensions
transformation(
    obj,
    location=(-3.5-1.5, 2.2, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(180))
)


obj = bpy.context.scene.objects["table"]
dim = obj.dimensions
transformation(
    obj,
    location=(0, 2, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(90))
)

obj = bpy.context.scene.objects["table_copy1"]
dim = obj.dimensions
transformation(
    obj,
    location=(0-2*dim.x-0.05, 2, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(90))
)
obj = bpy.context.scene.objects["table_copy2"]
dim = obj.dimensions
transformation(
    obj,
    location=(0, 2-1/2*dim.y+0.05, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(-90))
)
obj = bpy.context.scene.objects["table_copy3"]
dim = obj.dimensions
transformation(
    obj,
    location=(0-2*dim.x-0.05, 2-1/2*dim.y+0.05, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(-90))
)
obj = bpy.context.scene.objects["table_copy4"]
dim = obj.dimensions
transformation(
    obj,
    location=(-3.5, 2, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(90))
)
obj = bpy.context.scene.objects["table_copy5"]
dim = obj.dimensions
transformation(
    obj,
    location=(-3.5, 2-1/2*dim.y+0.05, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(90))
)
obj = bpy.context.scene.objects["table_copy6"]
dim = obj.dimensions
transformation(
    obj,
    location=(-3.5-2*dim.x-0.05, 2-1/2*dim.y+0.05, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(-90))
)
obj = bpy.context.scene.objects["table_copy7"]
dim = obj.dimensions
transformation(
    obj,
    location=(-3.5-2*dim.x-0.05, 2, dim.z/2),
    rotation_euler=(0, 0, np.deg2rad(90))
)