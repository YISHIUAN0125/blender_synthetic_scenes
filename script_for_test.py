import bpy
from mathutils import *
import numpy as np
import os
import json

def add_light(data):
    light_data = bpy.data.lights.new(name=data["name"], type=data["type"])
    light_object = bpy.data.objects.new(data["name"], light_data)
    bpy.context.scene.collection.objects.link(light_object)
    light_object.location = data["location"]
    light = bpy.data.objects[data["name"]]
    light.data.color = data["color"]
    light.data.energy = data["intensity"]  # intensity
    light_data.shape = 'RECTANGLE'            # 形狀改成矩形
    light_data.size = 0.2                     # 短邊
    light_data.size_y = 4.0                   # 長邊 (像燈管)



# Add a light 
positions = [
    (-4, -1, 3.6),
    ( 2, -1, 3.6),
    (-4,  2, 3.6),
    ( 2,  2, 3.6),
    ( 0, -1, 3.6),
    ( 0,  2, 3.6),
    ( 3.5, -5, 3.6),
]

# 依序建立六盞燈
for i, pos in enumerate(positions, start=1):
    data = {
        "name" : f"Light_{i}",   # 每盞燈要有不同名字
        "type" : "AREA",
        "location" : pos,
        "intensity" : 3000,
        "color" : (1.0, 0.8, 0.5)  # 溫暖黃光
    }
    add_light(data)

# Add a camera
camera_data = bpy.data.cameras.new(name="Camera")
camera_object = bpy.data.objects.new("Camera", camera_data)
bpy.context.scene.collection.objects.link(camera_object)
bpy.context.scene.camera = camera_object
camera_object.location = (2, 0, 1)
camera_object.rotation_euler = (np.deg2rad(75), 0, np.deg2rad(45)) # View

## output dir
OUT_DIR = "E:/NCU/blender_synthetic_scenes/tmp/blender_output"
os.makedirs(OUT_DIR, exist_ok=True)
scene = bpy.context.scene

# set render engine and device
scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
bpy.context.preferences.addons['cycles'].preferences.get_devices()
for device in bpy.context.preferences.addons['cycles'].preferences.devices:
    device.use = True
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.pixel_aspect_x = 1.0
scene.render.pixel_aspect_y = 1.0

view_layer = bpy.context.view_layer
view_layer.use = True

# Enable depth pass
scene = bpy.context.scene
scene.view_layers[0].use_pass_z = True

# Compositor：output RGB and Depth(EXR)
scene.use_nodes = True
scene.render.use_compositing = True
tree = scene.node_tree

# Clear defult nodes
for n in list(tree.nodes):
    tree.nodes.remove(n)

rl = tree.nodes.new("CompositorNodeRLayers")  # Render Layers
rl.location = (-300, 0)

# RGB output
out_rgb = tree.nodes.new("CompositorNodeOutputFile")
out_rgb.label = "RGB Output"
out_rgb.base_path = OUT_DIR
out_rgb.file_slots[0].path = "rgb_" # rgb_0001.png
out_rgb.format.file_format = 'PNG'
out_rgb.location = (200, 100)

# Depth output
out_z = tree.nodes.new("CompositorNodeOutputFile")
out_z.label = "Depth Output"
out_z.base_path = OUT_DIR
out_z.file_slots[0].path = "depth_"  # depth_0001.exr
out_z.format.file_format = 'OPEN_EXR'
out_z.location = (200, -100)

# connect nodes
tree.links.new(rl.outputs["Image"], out_rgb.inputs[0])
tree.links.new(rl.outputs["Depth"], out_z.inputs[0])

# intrinsics / extrinsics output
cam = bpy.context.scene.camera
assert cam is not None, "no scene.camera"

# resolution
W = scene.render.resolution_x
H = scene.render.resolution_y
aspect_x = scene.render.pixel_aspect_x
aspect_y = scene.render.pixel_aspect_y

# Image sensor size（mm）
sensor_w = cam.data.sensor_width
sensor_h = cam.data.sensor_height

# focal length（mm）
f_mm = cam.data.lens

# fx, fy（pixel）
# fx = f_mm * W_px / sensor_w_mm；
# fy = f_mm * H_px / sensor_h_mm
fx = f_mm * W / sensor_w
fy = f_mm * H / sensor_h

# image center(pixel)
cx = W * 0.5
cy = H * 0.5

K = [[fx, 0.0, cx],
     [0.0, fy, cy],
     [0.0, 0.0, 1.0]]

# render
scene.frame_current = 1  # 或你想要的 frame 編號
bpy.ops.render.render(write_still=True)
print(f"[DONE] 輸出影像到：{OUT_DIR}")

## Calculate ground truth
#def export_ground_truth(target_object_name):
#    bboxes_data = {}

#    for obj_name in target_object_name:
#        if obj_name not in bpy.data.objects:
#            print(f"[Warning] '{obj_name}'is not found")
#            continue
#            
#        obj = bpy.data.objects[obj_name]
#        class_name = obj_name.split("_")[0]
#        volumetric_center = list(obj.location)
#        size = list(obj.dimensions)
#        yaw = obj.rotation_euler.z
#        bottom_center_z = volumetric_center[2] - (size[2] / 2.0)
#        bottom_center = [
#            volumetric_center[0],
#            volumetric_center[1],
#            bottom_center_z
#        ]

#        bboxes_data[obj_name] = {
#            "class" : class_name,
#            "bottom_center": bottom_center,
#            "size": size,
#            "heading": yaw,
#            "volumetric_center": volumetric_center, 
#        }

#    with open(os.path.join(OUT_DIR, "ground_truth.json"), "w") as f:
#        json.dump(bboxes_data, f, indent=2)

### Camera extrinsics
### Blender camera 前是 -Z、上是 +Y
### matrix_world 4x4 matrix。
#cam = bpy.context.scene.camera

## Blender camera-to-world
#cam2world = np.array(cam.matrix_world)  # 轉 numpy
#world2cam = np.linalg.inv(cam2world) # 外參（OpenCV常用）
#meta = {
#    "width": W, "height": H,
#    "fx": fx, "fy": fy, "cx": cx, "cy": cy,
#    "sensor_width_mm": sensor_w, "sensor_height_mm": sensor_h,
#    "focal_length_mm": f_mm,
#    "camera_to_world_4x4": cam2world.tolist()
#}

#with open(os.path.join(OUT_DIR, "camera.json"), "w", encoding="utf-8") as f:
#    json.dump(meta, f, indent=2)

#TARGET = ["chair", "table", "table_copy"]

#export_ground_truth(TARGET)

#print("Camera to World:\n", cam2world.tolist())
#print("World to Camera:\n", world2cam.tolist())

#bpy.ops.wm.console_toggle()