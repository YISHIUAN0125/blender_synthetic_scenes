import numpy as np
import open3d as o3d
import json
import visualizer

COLOR_TABLE = {
    "table": (0.0, 1.0, 0.0),  # 綠色
    "chair": (0.0, 0.5, 1.0),  # 藍色
    # 您可以在這裡加入更多類別...
    # "sofa": (1.0, 0.0, 0.0), # 紅色
    "default": (0.5, 0.5, 0.5) # 灰色
}

input_path = r"tmp\scene_output\colored_point_cloud.ply"
input_path_gt = r"tmp\blender_output\ground_truth.json"

vis = visualizer.Visualizer()
pcd = vis.read_point_cloud(input_path)

# with open(input_path_gt, "r") as f:
#     gt_data = json.load(f)

# linesets = []

# print(gt_data.keys())
# for obj_name, bbox_data in gt_data.items():
#     volumetric_center = bbox_data["volumetric_center"]
#     yaw = bbox_data["heading"]
#     size = bbox_data["size"]
#     class_name = bbox_data.get("class", "default")
#     color = COLOR_TABLE.get(class_name, COLOR_TABLE["default"])
#     R = o3d.geometry.get_rotation_matrix_from_xyz((0, 0, yaw))
#     obb = o3d.geometry.OrientedBoundingBox(volumetric_center, R, size)
#     lineset = o3d.geometry.LineSet.create_from_oriented_bounding_box(obb)
#     lineset.paint_uniform_color(color)
#     linesets.append(lineset)

o3d.visualization.draw_geometries([pcd])




