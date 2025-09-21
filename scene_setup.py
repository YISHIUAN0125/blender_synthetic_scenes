import bpy
import numpy as np
import bmesh

def add_texture_node(nodes, path, colorspace='sRGB'):
    """添加 Image Texture 節點並載入圖片"""
    tex_node = nodes.new("ShaderNodeTexImage")
    try:
        img = bpy.data.images.load(path)
        tex_node.image = img
        tex_node.image.colorspace_settings.name = colorspace
    except RuntimeError:
        print(f"Warning: Could not load image at {path}. Check file path.")
        # 可以設置為紅色或其他顏色來提示缺失紋理
        # tex_node.outputs["Color"].default_value = (1, 0, 0, 1) 
    return tex_node

def setup_principled_material(name, base_color_path=None, roughness_path=None, 
                             normal_path=None, displacement_path=None, 
                             normal_strength=0.8, displacement_strength=1.0):
    """
    建立一個 Principled BSDF 材質，並根據提供的路徑連接紋理。
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # 清理不要的節點 (保留 Principled BSDF 和 Material Output)
    for n in nodes:
        if n.type not in ['BSDF_PRINCIPLED', 'OUTPUT_MATERIAL']:
            nodes.remove(n)

    principled = nodes.get("Principled BSDF") or nodes.new("ShaderNodeBsdfPrincipled")
    mat_output = [n for n in nodes if n.type == 'OUTPUT_MATERIAL'][0]

    # 設定節點位置以保持整潔
    principled.location = (200, 0)
    mat_output.location = (400, 0)

    # Base Color
    if base_color_path:
        tex_base = add_texture_node(nodes, base_color_path)
        links.new(tex_base.outputs["Color"], principled.inputs["Base Color"])
        tex_base.location = (-600, 300)

    # Roughness
    if roughness_path:
        tex_rough = add_texture_node(nodes, roughness_path, colorspace='Non-Color')
        links.new(tex_rough.outputs["Color"], principled.inputs["Roughness"])
        tex_rough.location = (-600, 150)

    # Normal
    if normal_path:
        tex_norm = add_texture_node(nodes, normal_path, colorspace='Non-Color')
        normal_map = nodes.new("ShaderNodeNormalMap")
        normal_map.inputs["Strength"].default_value = normal_strength
        links.new(tex_norm.outputs["Color"], normal_map.inputs["Color"])
        links.new(normal_map.outputs["Normal"], principled.inputs["Normal"])
        tex_norm.location = (-600, 0)
        normal_map.location = (0, 0)

    # Displacement
    if displacement_path:
        tex_disp = add_texture_node(nodes, displacement_path, colorspace='Non-Color')
        disp_node = nodes.new("ShaderNodeDisplacement")
        disp_node.inputs["Height"].default_value = displacement_strength # 根據需求調整
        links.new(tex_disp.outputs["Color"], disp_node.inputs["Height"])
        links.new(disp_node.outputs["Displacement"], mat_output.inputs["Displacement"])
        mat.cycles.displacement_method = 'DISPLACEMENT_AND_BUMP'
        tex_disp.location = (-600, -150)
        disp_node.location = (0, -150)
        
    return mat

def transformation(obj, location=None, scale=None, rotation_euler=None):
    """應用物體的變換"""
    if scale:
        obj.scale = scale
    if rotation_euler:
        obj.rotation_euler = rotation_euler
    if location:
        obj.location = location

def stretch_object_from_side(obj, axis, direction, new_position):
    """
    拉伸物體的指定側到新的位置。
    obj: 要拉伸的物體
    axis: 0=X, 1=Y, 2=Z
    direction: 1 (正向) 或 -1 (負向)
    new_position: 該側的新坐標
    """
    if obj.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # 選中物體並進入編輯模式
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table() # 確保頂點索引可查找
    
    epsilon = 1e-5 
    
    coords = [v.co[axis] for v in bm.verts]
    
    if direction > 0:
        boundary_value = max(coords)
    else:
        boundary_value = min(coords)
        
    verts_to_move = []
    for v in bm.verts:
        if abs(v.co[axis] - boundary_value) < epsilon:
            verts_to_move.append(v)
            
    move_distance = new_position - boundary_value
    
    move_vector = [0, 0, 0]
    move_vector[axis] = move_distance
    
    bmesh.ops.translate(bm,
                        verts=verts_to_move,
                        vec=move_vector)
                        
    bmesh.update_edit_mesh(obj.data)
    bm.free()

    bpy.ops.object.mode_set(mode='OBJECT')    

def apply_stretches(obj, stretches):
    """應用一系列的拉伸操作"""
    for axis, direction, position in stretches:
        stretch_object_from_side(obj, axis, direction, position)

# ====== Build floor ======
bpy.ops.mesh.primitive_plane_add(size=3, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"
floor.scale = (2, 2, 0.005)

# 建立地板材質
floor_mat = setup_principled_material(
    name="WoodMaterial",
    base_color_path="//../texture/Wood092_1K-JPG/Wood092_1K-JPG_Color.jpg",
    roughness_path="//../texture/Wood092_1K-JPG/Wood092_1K-JPG_Roughness.jpg",
    normal_path="//../texture/Wood092_1K-JPG/Wood092_1K-JPG_NormalGL.jpg",
    displacement_path="//../texture/Wood092_1K-JPG/Wood092_1K-JPG_Displacement.jpg",
    normal_strength=0.8
)
floor.data.materials.append(floor_mat)

# 地板拉伸
floor_stretches = [
    (0, -1, -2.9), # X軸負方向拉伸到 -2.9
    (0, 1, 2.5),   # X軸正方向拉伸到 2.5
    (1, -1, -3)    # Y軸負方向拉伸到 -3
]
apply_stretches(floor, floor_stretches)

# ====== Build walls ======

# 統一牆壁材質
wall_mat_white = bpy.data.materials.new(name="WhiteWall")
wall_mat_white.use_nodes = True
bsdf = wall_mat_white.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)
bsdf.inputs["Roughness"].default_value = 0.9

# 牆壁數據
walls_data = [
    {"name": "Wall1", "location": (5, -1.5, 1.75), "rotation_euler": (0, 0, np.deg2rad(90)), "scale": (3, 0.1, 1.2)},
    {"name": "Wall1_copy1", "location": (-5.8, -1.5, 1.75), "rotation_euler": (0, 0, np.deg2rad(90)), "base_obj_name": "Wall1"},
    {"name": "Wall2", "location": (-0.4, 3, 1.75), "rotation_euler": (0, 0, np.deg2rad(0)), "scale": (3.6, 0.1, 1.2)},
    {"name": "Wall2_copy1", "location": (-0.4, -6, 1.75), "rotation_euler": (0, 0, np.deg2rad(0)), "scale": (3.6, 0.1, 1.2)}, # 從 Wall2 複製的
    {"name": "Wall3", "location": (-0.9, -3, 1.75), "rotation_euler": (0, 0, np.deg2rad(0)), "scale": (2, 0.1, 1.2), "stretches": [(0, -1, -2.45), (0, 1, 1.58)]},
    {"name": "Wall4", "location": (-2, -4.5, 1.75), "rotation_euler": (0, 0, np.deg2rad(90)), "scale": (1, 0.1, 1.2)},
    {"name": "Wall4_copy1", "location": (-2+4.1, -4.5, 1.75), "base_obj_name": "Wall4"} # 從 Wall4 複製的
]

for wall_info in walls_data:
    obj_name = wall_info["name"]
    base_obj = None

    if "base_obj_name" in wall_info: # 這是複製的牆壁
        base_obj = bpy.data.objects.get(wall_info["base_obj_name"])
        if base_obj:
            new_wall = base_obj.copy()
            new_wall.data = base_obj.data # 鏈接數據塊，而非複製
            bpy.context.collection.objects.link(new_wall)
            new_wall.name = obj_name
        else:
            print(f"Warning: Base object '{wall_info['base_obj_name']}' not found for '{obj_name}'. Skipping.")
            continue
    else: # 這是新創建的牆壁
        bpy.ops.mesh.primitive_cube_add(size=3) # 初始大小無關緊要，因為會被 scale 覆蓋
        new_wall = bpy.context.active_object
        new_wall.name = obj_name
        new_wall.data.materials.append(wall_mat_white)

    transformation(
        new_wall, 
        location=wall_info.get("location"),
        scale=wall_info.get("scale"),
        rotation_euler=wall_info.get("rotation_euler")
    )

    if "stretches" in wall_info:
        apply_stretches(new_wall, wall_info["stretches"])


# ====== Build ceiling ======
bpy.ops.mesh.primitive_plane_add(size=3, location=(0, 0, 3.56))
ceiling = bpy.context.active_object
ceiling.name = "Ceiling"
ceiling.scale = (2, 2, 0.05) 

# 建立天花板材質
ceiling_mat = setup_principled_material(
    name="CeilingMaterial",
    base_color_path="//../texture/OfficeCeiling001_4K-JPG/OfficeCeiling001_4K_Color.jpg",
    roughness_path="//../texture/OfficeCeiling001_4K-JPG/OfficeCeiling001_4K_Roughness.jpg",
    normal_path="//../texture/OfficeCeiling001_4K-JPG/OfficeCeiling001_4K_NormalGL.jpg",
    displacement_path="//../texture/OfficeCeiling001_4K-JPG/OfficeCeiling001_4K_Displacement.jpg",
    normal_strength=0.8
)
ceiling.data.materials.append(ceiling_mat)

# 天花板拉伸
ceiling_stretches = [
    (0, -1, -2.9),
    (0, 1, 2.5),
    (1, -1, -3)
]
apply_stretches(ceiling, ceiling_stretches)

# ====== Build door ======
def build_door(wall, location, scale):
    bpy.ops.mesh.primitive_cube_add(size=2, location=location)
    door_hole = bpy.context.active_object
    door_hole.name = "DoorHole"
    door_hole.scale = scale
    bool_mod = wall.modifiers.new(name="DoorBoolean", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = door_hole
    wall.data=wall.data.copy()
    bpy.context.view_layer.objects.active = wall
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)

    bpy.data.objects.remove(door_hole, do_unlink=True)
    
wall = bpy.data.objects.get("Wall1")
build_door(wall, location=(5, 1.5, 1), scale=(1, 0.8, 1))
wall = bpy.data.objects.get("Wall3")
build_door(wall, location=(-3, -3, 1), scale=(0.5, 0.5, 1))
build_door(wall, location=(-1, -3, 1), scale=(0.5, 0.5, 1))