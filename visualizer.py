from sklearn.neighbors import NearestNeighbors
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import json

class Operator():
    def __init__(self):
        pass

    def get_vertices(self, mesh) -> np.ndarray:
        return np.asarray(mesh.vertices, dtype=np.float32)

    def get_faces(self, mesh) -> np.ndarray:
        return np.asarray(mesh.triangles, dtype=np.float32)

    def get_xyz(self, pcd) -> np.ndarray:
        return np.asarray(pcd.points, dtype=np.float32)

    def get_colors(self, pcd) -> np.ndarray:
        return np.asarray(pcd.colors, dtype=np.float32)


class Visualizer(Operator):
    def __init__(self):
        super().__init__()
    def _create_bbox_lines(self, bboxes, color=[1, 0, 0]):
        """
        bboxes: (N, 7) [x, y, z, dx, dy, dz, heading]
        """
        linesets = []
        for box in bboxes:
            center = box[:3]
            size = box[3:6]
            # center[2] += size[2] / 2
            R = o3d.geometry.OrientedBoundingBox.get_rotation_matrix_from_axis_angle([0, 0, box[6]])
            obb = o3d.geometry.OrientedBoundingBox(center, R, size)
            lineset = o3d.geometry.LineSet.create_from_oriented_bounding_box(obb)
            lineset.paint_uniform_color(color)
            linesets.append(lineset)
        return linesets

    def create_point_cloud_from_unidet(self, points):
        pcd = o3d.geometry.PointCloud()
        xyz = np.array(points)[:, :3]
        rgb = (np.array(points)[:, 3:6]*127.5+127.5)/255  # RGB 必須是 0~1
        pcd.points = o3d.utility.Vector3dVector(xyz)
        pcd.colors = o3d.utility.Vector3dVector(rgb)
        return pcd

    def read_point_cloud_bin(self, pc_file):
        points = np.fromfile(pc_file, dtype=np.float32).reshape(-1, 6)
        pcd = o3d.geometry.PointCloud()
        xyz = np.array(points)[:, :3]
        print(xyz.shape)
        rgb = (np.array(points)[:, 3:6])  # RGB 必須是 0~1
        pcd.points = o3d.utility.Vector3dVector(xyz)
        pcd.colors = o3d.utility.Vector3dVector(rgb)
        return pcd

    def read_superpoints(self, sp_file):
        superpoints = np.fromfile(sp_file, dtype=np.int64)
        return superpoints

    def paint_sp(self, xyz_orig, vertices, superpoints):
        nbrs = NearestNeighbors(n_neighbors=1).fit(vertices)
        _, indices = nbrs.kneighbors(xyz_orig)
        print(indices.shape)
        mapped_labels = superpoints[indices.flatten()]  # shape: (N,)
        # mapped_labels = superpoints[indices]  # shape: (N,)
        cmap = plt.get_cmap("tab20")
        colors_sp = cmap(mapped_labels % 20)[:, :3]  # shape: (N, 3)
        painted_sp = o3d.geometry.PointCloud(
            o3d.utility.Vector3dVector(xyz_orig)
        )
        painted_sp.colors = o3d.utility.Vector3dVector(colors_sp)
        return painted_sp

    def read_mesh(self, mesh_file, enable_post_processing=True):
        mesh = o3d.io.read_triangle_mesh(mesh_file, enable_post_processing=enable_post_processing)
        return mesh

    def read_point_cloud(self, pc_file):
        pcd = o3d.io.read_point_cloud(pc_file)
        return pcd

    def show(self, data, bboxes=None):
        if bboxes is not None:
            bbox_linesets = self._create_bbox_lines(bboxes)
            o3d.visualization.draw_geometries([data] + bbox_linesets)
        else:
            o3d.visualization.draw_geometries([data])


if __name__ == '__main__':
    vis = Visualizer()
    # pcd = vis.read_point_cloud('zed_data\point_cloud_PLY_36207547_720_05-08-2025-15-38-18.ply')
    pcd = vis.read_point_cloud_bin(r'sunrgbd\points\000001.bin')
    superpoints = vis.read_superpoints(r'sunrgbd\superpoints\000001.bin')
    print(superpoints.max())
    points = vis.get_xyz(pcd)
    colors = vis.get_colors(pcd)
    sp = vis.paint_sp(points, points, superpoints)
    print(points.shape)
    # print(colors.shape)
    print(superpoints.shape)
    vis.show(sp)
    # vis.show(pcd)

    # with open(r'arkitscenes\results\zed_test_with_RGcpp.json', 'r') as f:
    #     data = json.load(f)
    # pcd = vis.create_point_cloud_from_unidet(data['points'])
    # bboxes = np.array(data['bboxes_3d'])
    # vis.show(pcd, bboxes)