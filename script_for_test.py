import bpy
import numpy as np


def transformation(obj, location=None, scale=None, rotation_euler=None):
    if scale:
        obj.scale = scale
    if rotation_euler:
        obj.rotation_euler = rotation_euler
    if location:
        obj.location = location


def duplicate_object(src_name, new_name, location=None, rotation_euler=None, scale=None):
    """複製物件，保留材質與貼圖"""
    src_obj = bpy.data.objects[src_name]
    new_obj = src_obj.copy()
    new_obj.data = src_obj.data.copy()   # 複製 mesh 資料
    new_obj.animation_data_clear()
    new_obj.name = new_name

    # 保留原始材質（避免變成粉紅）
    new_obj.data.materials.clear()
    for mat in src_obj.data.materials:
        new_obj.data.materials.append(mat)

    bpy.context.collection.objects.link(new_obj)

    transformation(new_obj, location, scale, rotation_euler)
    return new_obj

# ====== Layout cfg ======
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
        {"suffix": "copy1", "loc": (-2*2-0.05, 2, None), "rot": (0, 0, np.deg2rad(90))},
        {"suffix": "copy2", "loc": (0, 1.5, None), "rot": (0, 0, np.deg2rad(-90))},
        {"suffix": "copy3", "loc": (-2*2-0.05, 1.5, None), "rot": (0, 0, np.deg2rad(-90))},
        {"suffix": "copy4", "loc": (-3.5, 2, None), "rot": (0, 0, np.deg2rad(90))},
        {"suffix": "copy5", "loc": (-2*2-0.05, 2, None), "rot": (0, 0, np.deg2rad(90))},
        {"suffix": "copy6", "loc": (0, 1.5, None), "rot": (0, 0, np.deg2rad(-90))},
        {"suffix": "copy7", "loc": (-2*2-0.05, 1.5, None), "rot": (0, 0, np.deg2rad(-90))},
    ],
}

for base_name, copies in layout_plan.items():
    base_obj = bpy.data.objects[base_name]
    dim = base_obj.dimensions

    for cfg in copies:
        z = cfg["loc"][2] if cfg["loc"][2] is not None else dim.z / 2
        new_name = f"{base_name}_{cfg['suffix']}"
        duplicate_object(
            base_name,
            new_name,
            location=(cfg["loc"][0], cfg["loc"][1], z),
            rotation_euler=cfg["rot"],
        )
