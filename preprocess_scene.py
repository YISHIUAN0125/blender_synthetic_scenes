import json, os
import numpy as np
import OpenEXR, Imath
import cv2

# Path
IN_DIR = r"tmp\blender_output" 
OUT_DIR = r"tmp\scene_output"
depth_exr = os.path.join(IN_DIR, "depth_0001.exr")
rgb_png   = os.path.join(IN_DIR, "rgb_0001.png")
cam_json  = os.path.join(IN_DIR, "camera.json")

# Camera intrinsics / extrinsics
with open(cam_json, "r") as f:
    meta = json.load(f)

W, H = meta["width"], meta["height"]
fx, fy, cx, cy = meta["fx"], meta["fy"], meta["cx"], meta["cy"]
cam2world = np.array(meta["camera_to_world_4x4"])

# RGB
img_rgb = cv2.imread(rgb_png)
img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)

# Read Depth information EXR
exr = OpenEXR.InputFile(depth_exr)
dw = exr.header()['dataWindow']
size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
assert size == (W, H), "depth map size error"

pt = Imath.PixelType(Imath.PixelType.FLOAT)
depth_channel_str = exr.channel('R', pt)
depth_map = np.frombuffer(depth_channel_str, dtype=np.float32)
depth_map = depth_map.reshape(H, W)
exr.close()

def create_colored_point_cloud(depth_map, image_rgb, fx, fy, cx, cy, cam2world):
    """將深度圖和RGB影像轉換為世界座標系中的彩色點雲"""
    height, width = depth_map.shape
    
    # build pixel coordinates
    u = np.arange(width)
    v = np.arange(height)
    u, v = np.meshgrid(u, v)
    
    # filter out invalid depth values
    valid_depth_mask = (depth_map > 0) & (depth_map < 100)
    
    Z = depth_map[valid_depth_mask]
    u_valid = u[valid_depth_mask]
    v_valid = v[valid_depth_mask]
    colors = image_rgb[valid_depth_mask]
    
    # Transform to Camera coordinates
    X_cam = (u_valid - cx) * Z / fx
    Y_cam = -((v_valid - cy) * Z / fy)
    Z_cam = -Z 

    # Homogenous coordinates
    points_camera = np.vstack((X_cam, Y_cam, Z_cam, np.ones_like(Z)))

    # Transform to world coordinates
    points_world = cam2world @ points_camera

    return points_world[:3, :].T, colors


def save_ply(filename, points, colors):
    """將點和顏色資料儲存為 ASCII PLY 檔案"""

    points_colored = np.hstack((points, colors.astype(np.uint8)))
    num_points = len(points_colored)
    
    # PLY 
    header = f"""ply
                format ascii 1.0
                element vertex {num_points}
                property float x
                property float y
                property float z
                property uchar red
                property uchar green
                property uchar blue
                end_header
            """    
    # write to file
    with open(filename, 'w') as f:
        f.write(header)
        np.savetxt(f, points_colored, fmt='%f %f %f %d %d %d')
    print(f"Saved to: {filename}")

if __name__ == "__main__":

    points_3d, point_colors = create_colored_point_cloud(depth_map, img_rgb, fx, fy, cx, cy, cam2world)

    ply_output_path = os.path.join(OUT_DIR, "colored_point_cloud.ply")
    save_ply(ply_output_path, points_3d, point_colors)