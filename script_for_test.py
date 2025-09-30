import bpy
import numpy as np


def transformation(obj, location=None, scale=None, rotation_euler=None, dimensions=None):

    if dimensions:
        orig_dim = obj.dimensions
        scale = (
            dimensions[0] / orig_dim.x if orig_dim.x > 0 else 1,
            dimensions[1] / orig_dim.y if orig_dim.y > 0 else 1,
            dimensions[2] / orig_dim.z if orig_dim.z > 0 else 1,
        )
    if scale:
        obj.scale = scale
    if rotation_euler:
        obj.rotation_euler = rotation_euler
    if location:
        obj.location.x = location[0]
        obj.location.y = location[1]
        obj.location.z = obj.dimensions.z/2    

    if dimensions:
        obj.location.z = dimensions[2] / 2


def duplicate_object(src_name, new_name, location=None, rotation_euler=None, scale=None, dimensions=None):

    src_obj = bpy.data.objects[src_name]
    new_obj = src_obj.copy()
    new_obj.data = src_obj.data.copy()
    new_obj.animation_data_clear()
    new_obj.name = new_name

    # keep original material
    new_obj.data.materials.clear()
    for mat in src_obj.data.materials:
        new_obj.data.materials.append(mat)

    bpy.context.collection.objects.link(new_obj)

    transformation(new_obj, location, scale, rotation_euler, dimensions)
    return new_obj


# ====== Layout ======
layout_plan = {
    "chair": [
        {"suffix": "copy1", "loc": (-1.5, 2.2, None), "rot": (0, 0, np.deg2rad(0))},
        {"suffix": "copy2", "loc": (0, 1.1, None), "rot": (0, 0, np.deg2rad(0))},
        {"suffix": "copy3", "loc": (-1.5, 1.1, None), "rot": (0, 0, np.deg2rad(0))},
        {"suffix": "copy4", "loc": (-3.5, 1.1, None), "rot": (0, 0, np.deg2rad(0))},
        {"suffix": "copy5", "loc": (-5.0, 1.1, None), "rot": (0, 0, np.deg2rad(0))},
        {"suffix": "copy6", "loc": (-3.5, 2.2, None), "rot": (0, 0, np.deg2rad(180))},
        {"suffix": "copy7", "loc": (-5.0, 2.2, None), "rot": (0, 0, np.deg2rad(180))},
    ],
    "table": [
        {"suffix": "copy1", "loc": (-4.05, 2, None), "rot": (0, 0, np.deg2rad(90))},
        {"suffix": "copy2", "loc": (0, 1.5, None), "rot": (0, 0, np.deg2rad(-90))},
        {"suffix": "copy3", "loc": (-4.05, 1.5, None), "rot": (0, 0, np.deg2rad(-90))},
        {"suffix": "copy4", "loc": (-3.5, 2, None), "rot": (0, 0, np.deg2rad(90))},
        {"suffix": "copy5", "loc": (-4.05, 2, None), "rot": (0, 0, np.deg2rad(90))},
        {"suffix": "copy6", "loc": (0, 1.5, None), "rot": (0, 0, np.deg2rad(-90))},
        {"suffix": "copy7", "loc": (-4.05, 1.5, None), "rot": (0, 0, np.deg2rad(-90))},
    ],
}

## auto generate
#for base_name, copies in layout_plan.items():
#    base_obj = bpy.data.objects[base_name]
#    dim = base_obj.dimensions
#    for cfg in copies:
#        z = cfg["loc"][2] if cfg["loc"][2] is not None else dim.z / 2
#        new_name = f"{base_name}_{cfg['suffix']}"
#        duplicate_object(
#            base_name,
#            new_name,
#            location=(cfg["loc"][0], cfg["loc"][1], z),
#            rotation_euler=cfg["rot"],
#        )

double_door_cabinet = bpy.context.scene.objects["double_door_cabinet"]
transformation(
    double_door_cabinet,
    location=(-3.32, 3.15, 0),
    dimensions=(0.45, 0.85, 1.8),
    rotation_euler=(0, 0, -np.deg2rad(90))
)
