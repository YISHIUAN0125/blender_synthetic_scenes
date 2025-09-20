import bpy
import numpy as np
import bmesh

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

def stretch_object_from_side(obj, axis, direction, new_position):
    if obj.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    bm = bmesh.from_edit_mesh(obj.data)
    
    epsilon = 1e-5 
    
    coords = [v.co[axis] for v in bm.verts]
    
    if direction > 0:
        boundary_value = max(coords)
    else:
        boundary_value = min(coords)
        
    verts_to_move = []
    for v in bm.verts:
        v.select = False 
        if abs(v.co[axis] - boundary_value) < epsilon:
            v.select = True
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


## ====== Build floor ======
#bpy.ops.mesh.primitive_plane_add(size=3, location=(0, 0, 0))
#floor = bpy.context.active_object
#floor.name = "Floor"
#floor.scale = (2, 2, 0.005)

## 建立材質
#mat = bpy.data.materials.new(name="WoodMaterial")
#mat.use_nodes = True
#nodes = mat.node_tree.nodes
#links = mat.node_tree.links

## 清理不要的節點
#for n in nodes:
#   if n.type not in ['BSDF_PRINCIPLED', 'OUTPUT_MATERIAL']:
#       nodes.remove(n)

#principled = nodes["Principled BSDF"]

## Base Color
#tex_base = add_texture_node(nodes, r"E:\NCU\blender_synthetic_scenes\texture\Wood092_1K-JPG\Wood092_1K-JPG_Color.jpg")
#links.new(tex_base.outputs["Color"], principled.inputs["Base Color"])

## Roughness
#tex_rough = add_texture_node(nodes, r"E:\NCU\blender_synthetic_scenes\texture\Wood092_1K-JPG\Wood092_1K-JPG_Roughness.jpg", colorspace='Non-Color')
#links.new(tex_rough.outputs["Color"], principled.inputs["Roughness"])

## Normal
#tex_norm = add_texture_node(nodes, r"E:\NCU\blender_synthetic_scenes\texture\Wood092_1K-JPG\Wood092_1K-JPG_NormalGL.jpg", colorspace='Non-Color')
#normal_map = nodes.new("ShaderNodeNormalMap")
#normal_map.inputs["Strength"].default_value = 0.8
#links.new(tex_norm.outputs["Color"], normal_map.inputs["Color"])
#links.new(normal_map.outputs["Normal"], principled.inputs["Normal"])

## Displacement (可選)
#tex_disp = add_texture_node(nodes, r"E:\NCU\blender_synthetic_scenes\texture\Wood092_1K-JPG\Wood092_1K-JPG_Displacement.jpg", colorspace='Non-Color')

#disp_node = nodes.new("ShaderNodeDisplacement")
#links.new(tex_disp.outputs["Color"], disp_node.inputs["Height"])
#mat_output = [n for n in nodes if n.type == 'OUTPUT_MATERIAL'][0]
#links.new(disp_node.outputs["Displacement"], mat_output.inputs["Displacement"])
#mat.cycles.displacement_method = 'DISPLACEMENT_AND_BUMP'

## 指定給物件
#floor = bpy.data.objects["Floor"]
#floor.data.materials.append(mat)

## stretch
#target_object = bpy.data.objects.get("Floor")
#stretch_axis = 0 
#stretch_direction = -1 
#target_position = -2.9

#stretch_object_from_side(target_object, 
#                        stretch_axis, 
#                        stretch_direction, 
#                        target_position)
## stretch
#target_object = bpy.data.objects.get("Floor")
#stretch_axis = 0 
#stretch_direction = 1 
#target_position = 2.5

#stretch_object_from_side(target_object, 
#                        stretch_axis, 
#                        stretch_direction, 
#                        target_position)

## stretch
#target_object = bpy.data.objects.get("Floor")
#stretch_axis = 0 
#stretch_direction = -1 
#target_position = -2.9

#stretch_object_from_side(target_object, 
#                        stretch_axis, 
#                        stretch_direction, 
#                        target_position)
#target_object = bpy.data.objects.get("Floor")
#stretch_axis = 1 
#stretch_direction = -1 
#target_position = -3

#stretch_object_from_side(target_object, 
#                        stretch_axis, 
#                        stretch_direction, 
#                        target_position)


## ====== Build walls ======
#bpy.ops.mesh.primitive_cube_add(size=3, location=(5, -1.5, 1.75), rotation=(0, 0, np.deg2rad(90)))
#wall = bpy.context.active_object
#wall.name = "Wall"
#wall.scale = (3, 0.005, 1.2)

#mat_wall = bpy.data.materials.new(name="WhiteWall")
#mat_wall.use_nodes = True
#bsdf = mat_wall.node_tree.nodes["Principled BSDF"]
#bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)
#bsdf.inputs["Roughness"].default_value = 0.9
#wall.data.materials.append(mat_wall)

#obj = bpy.context.scene.objects["Wall"]
#for i in range(1):
#   wall_copy = wall.copy()
#   wall_copy.name = f"Wall_copy{i+1}"
#   bpy.context.collection.objects.link(wall_copy)
#obj = bpy.context.scene.objects["Wall_copy1"]
#transformation(
#   obj, 
#   location=(-3-2.8, -1.5, 1.75),
#   rotation_euler=(0, 0, np.deg2rad(90))
#)

#bpy.ops.mesh.primitive_cube_add(size=3, location=(-0.4, 3, 1.75), rotation=(0, 0, np.deg2rad(0)))
#wall = bpy.context.active_object
#wall.name = "Wall2"
#wall.scale = (3.6, 0.005, 1.2)

#mat_wall = bpy.data.materials.new(name="WhiteWall")
#mat_wall.use_nodes = True
#bsdf = mat_wall.node_tree.nodes["Principled BSDF"]
#bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)
#bsdf.inputs["Roughness"].default_value = 0.9
#wall.data.materials.append(mat_wall)

#obj = bpy.context.scene.objects["Wall2"]
#for i in range(1):
#   wall_copy = wall.copy()
#   wall_copy.name = f"Wall2_copy{i+1}"
#   bpy.context.collection.objects.link(wall_copy)
#obj = bpy.context.scene.objects["Wall2_copy1"]
#transformation(
#   obj, 
#   location=(-0.4, -6, 1.75),
#   rotation_euler=(0, 0, np.deg2rad(0)),
#   scale=(3.6, 0.005, 1.2)
#)

#bpy.ops.mesh.primitive_cube_add(size=3, location=(-0.9, -3, 1.75), rotation=(0, 0, np.deg2rad(0)))
#wall = bpy.context.active_object
#wall.name = "Wall3"
#wall.scale = (2, 0.005, 1.2)

#mat_wall = bpy.data.materials.new(name="WhiteWall")
#mat_wall.use_nodes = True
#bsdf = mat_wall.node_tree.nodes["Principled BSDF"]
#bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)
#bsdf.inputs["Roughness"].default_value = 0.9
#wall.data.materials.append(mat_wall)

#target_object = bpy.data.objects.get("Wall3")
#stretch_axis = 0 
#stretch_direction = -1 
#target_position = -2.45

#stretch_object_from_side(target_object, 
#                        stretch_axis, 
#                        stretch_direction, 
#                        target_position)
#                        
#bpy.ops.mesh.primitive_cube_add(size=3, location=(-2, -4.5, 1.75), rotation=(0, 0, np.deg2rad(90)))
#wall = bpy.context.active_object
#wall.name = "Wall4"
#wall.scale = (1, 0.005, 1.2)
#obj = bpy.context.scene.objects["Wall4"]
#obj.scale=(1, 0.1, 1.2)

#mat_wall = bpy.data.materials.new(name="WhiteWall")
#mat_wall.use_nodes = True
#bsdf = mat_wall.node_tree.nodes["Principled BSDF"]
#bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)
#bsdf.inputs["Roughness"].default_value = 0.9
#wall.data.materials.append(mat_wall)

#obj = bpy.context.scene.objects["Wall4"]
#wall_copy = obj.copy()
#bpy.context.collection.objects.link(wall_copy)
#wall_copy.name = "Wall4_copy"
#obj = bpy.context.scene.objects["Wall4_copy"]
#transformation(
#   obj, 
#   location=(-2+4.1, -4.5, 1.75),
#)

## ====== Build ceiling ======
#bpy.ops.mesh.primitive_plane_add(size=3, location=(0, 0, 3.56))
#ceiling = bpy.context.active_object
#ceiling.name = "Ceiling"
#ceiling.scale = (2, 2, 0.05)

## 建立材質
#mat = bpy.data.materials.new(name="CeilingMaterial")
#mat.use_nodes = True
#nodes = mat.node_tree.nodes
#links = mat.node_tree.links

## 清理不要的節點
#for n in nodes:
#  if n.type not in ['BSDF_PRINCIPLED', 'OUTPUT_MATERIAL']:
#      nodes.remove(n)

#principled = nodes["Principled BSDF"]

## Base Color
#tex_base = add_texture_node(nodes, r"E:\NCU\blender_synthetic_scenes\texture\OfficeCeiling001_4K-JPG\OfficeCeiling001_4K_Color.jpg")
#links.new(tex_base.outputs["Color"], principled.inputs["Base Color"])

## Roughness
#tex_rough = add_texture_node(nodes, r"E:\NCU\blender_synthetic_scenes\texture\OfficeCeiling001_4K-JPG\OfficeCeiling001_4K_Roughness.jpg", colorspace='Non-Color')
#links.new(tex_rough.outputs["Color"], principled.inputs["Roughness"])

## Normal
#tex_norm = add_texture_node(nodes, r"E:\NCU\blender_synthetic_scenes\texture\OfficeCeiling001_4K-JPG\OfficeCeiling001_4K_NormalGL.jpg", colorspace='Non-Color')
#normal_map = nodes.new("ShaderNodeNormalMap")
#normal_map.inputs["Strength"].default_value = 0.8
#links.new(tex_norm.outputs["Color"], normal_map.inputs["Color"])
#links.new(normal_map.outputs["Normal"], principled.inputs["Normal"])

## Displacement (可選)
#tex_disp = add_texture_node(nodes, r"E:\NCU\blender_synthetic_scenes\texture\OfficeCeiling001_4K-JPG\OfficeCeiling001_4K_Displacement.jpg", colorspace='Non-Color')

#disp_node = nodes.new("ShaderNodeDisplacement")
#links.new(tex_disp.outputs["Color"], disp_node.inputs["Height"])
#mat_output = [n for n in nodes if n.type == 'OUTPUT_MATERIAL'][0]
#links.new(disp_node.outputs["Displacement"], mat_output.inputs["Displacement"])
#mat.cycles.displacement_method = 'DISPLACEMENT_AND_BUMP'

## 指定給物件
#ceiling = bpy.data.objects["Ceiling"]
#ceiling.data.materials.append(mat)

## stretch
#target_object = bpy.data.objects.get("Ceiling")
#stretch_axis = 0 
#stretch_direction = -1 
#target_position = -2.9

#stretch_object_from_side(target_object, 
#                        stretch_axis, 
#                        stretch_direction, 
#                        target_position)
## stretch
#target_object = bpy.data.objects.get("Ceiling")
#stretch_axis = 0 
#stretch_direction = 1 
#target_position = 2.5

#stretch_object_from_side(target_object, 
#                        stretch_axis, 
#                        stretch_direction, 
#                        target_position)

## stretch
#target_object = bpy.data.objects.get("Ceiling")
#stretch_axis = 0 
#stretch_direction = -1 
#target_position = -2.9

#stretch_object_from_side(target_object, 
#                        stretch_axis, 
#                        stretch_direction, 
#                        target_position)
#target_object = bpy.data.objects.get("Ceiling")
#stretch_axis = 1 
#stretch_direction = -1 
#target_position = -3

#stretch_object_from_side(target_object, 
#                        stretch_axis, 
#                        stretch_direction, 
#                        target_position)

# ====== Build door ======
def build_door(location, scale):
    pass
