#!/usr/bin/env python3
"""Blender 4.x: create a REAL 3D camera journey across a FIXED cathedral mural.

Run: blender --background --python production/blender_cathedral.py -- [--cathedral path.glb]
The built-in stone geometry is a BLOCKOUT, not a photoreal cathedral asset.
No animation exists anywhere except the camera transform/lens.
One logical 39m x 2m mural is ONE STATIC MESH with 13 static UV materials,
so the huge flat artwork needn't exceed GPU texture-size limits.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parent.parent
ARGS=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
ap=argparse.ArgumentParser()
ap.add_argument("--manifest",type=Path,default=ROOT/"production"/"frieze_manifest.json")
ap.add_argument("--assets-root",type=Path,default=ROOT)
ap.add_argument("--cathedral",type=Path,default=None,help="Optional supplied static cathedral .glb/.gltf model, pre-aligned to mural wall at y=0.")
ap.add_argument("--save",type=Path,default=ROOT/"output"/"mosaic_cathedral_blockout.blend")
ap.add_argument("--fps",type=int,default=24)
ap.add_argument("--preview-res",type=int,default=100,help="Render resolution percentage, 1-100.")
args=ap.parse_args(ARGS)
manifest=json.loads(args.manifest.read_text(encoding="utf-8"))
panels=manifest["assets"]
count=len(panels)
wall_m=manifest["layout"]["physical_m"]
width=float(wall_m["width"]); height=float(wall_m["height"])
if count==0 or args.fps<=0 or not 1<=args.preview_res<=100:
    raise ValueError("Invalid production camera configuration.")
for panel in panels:
    if not (args.assets_root/panel["file"]).is_file():
        raise FileNotFoundError(f"Required canonical mural art missing: {args.assets_root/panel['file']}")

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for material in list(bpy.data.materials):
    if material.users==0:
        bpy.data.materials.remove(material)

def static_material(name,color,roughness=0.68):
    mat=bpy.data.materials.new(name)
    mat.diffuse_color=(*color,1.0)
    mat.use_nodes=True
    node=mat.node_tree.nodes.get("Principled BSDF")
    node.inputs["Base Color"].default_value=(*color,1)
    node.inputs["Roughness"].default_value=roughness
    return mat

stone=static_material("Static limestone masonry",(0.34,0.32,0.31))
floor_mat=static_material("Static cathedral flagstone",(0.24,0.24,0.26),0.83)
gold=static_material("Static carved trim",(0.42,0.30,0.15),0.5)

def block(name,location,dimensions,mat):
    bpy.ops.mesh.primitive_cube_add(size=1,location=location)
    ob=bpy.context.object
    ob.name=name
    ob.dimensions=dimensions
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    ob.data.materials.append(mat)
    return ob

# Physically static blockout, replaceable by separately supplied cathedral asset.
block("STONE BACK WALL",(0,0.8,6.0),(width+8,1.0,12.0),stone)
block("CATHEDRAL FLOOR",(0,-13,-0.22),(width+16,29,0.36),floor_mat)
block("CEILING VAULT BLOCKOUT",(0,-12.0,12.0),(width+16,27,0.8),stone)
for i in range(12):
    x=-width/2+1.3+i*width/11
    block(f"Stone wall pier {i:02d}",(x,0.12,5.6),(.30,.55,8.5),stone)
    block(f"Roof rib {i:02d}",(x,-7.4,10.7),(.28,15.0,.35),stone)
    block(f"Remote nave column {i:02d}",(x,-14.0,5.6),(.60,.60,11.0),stone)
block("GOLD MURAL TRIM UPPER",(0,0.20,4.21),(width+0.26,.30,.15),gold)
block("GOLD MURAL TRIM LOWER",(0,0.20,2.00),(width+0.26,.30,.15),gold)

# This one planar object has one adjacent fixed quad per source image plate.
# Breaking the texture into GPUs' manageable image dimensions does NOT
# turn it into multiple animated tiles: all quads share one immobile mesh.
z0=2.1; z1=z0+height; y=-0.08
vertices=[]
faces=[]
face_uv=[]
for i in range(count):
    x0=-width/2+i*width/count
    x1=-width/2+(i+1)*width/count
    base=len(vertices)
    vertices.extend([(x0,y,z0),(x1,y,z0),(x1,y,z1),(x0,y,z1)])
    faces.append((base,base+1,base+2,base+3))
mesh=bpy.data.meshes.new("One frozen mural, internally tiled UV")
mesh.from_pydata(vertices,[],faces)
mesh.update()
mural=bpy.data.objects.new("ONE IMMOBILE STORY MURAL",mesh)
bpy.context.collection.objects.link(mural)
uv_layer=mesh.uv_layers.new(name="Mural plate UV")
for poly in mesh.polygons:
    for j,li in enumerate(poly.loop_indices):
        uv_layer.data[li].uv=[(0,0),(1,0),(1,1),(0,1)][j]
for i,panel in enumerate(panels):
    path=args.assets_root/panel["file"]
    img=bpy.data.images.load(str(path.resolve()),check_existing=True)
    img.name=f"MASTER / {i:02d} / {panel['id']}"
    mat=bpy.data.materials.new(f"FLAT STATIC ART {i:02d}")
    mat.use_nodes=True
    nodes=mat.node_tree.nodes
    principled=nodes.get("Principled BSDF")
    principled.inputs["Roughness"].default_value=0.30
    principled.inputs["Metallic"].default_value=0.02
    tex=nodes.new("ShaderNodeTexImage")
    tex.image=img
    tex.interpolation="Linear"
    mat.node_tree.links.new(tex.outputs["Color"],principled.inputs["Base Color"])
    mesh.materials.append(mat)
    mesh.polygons[i].material_index=i

if args.cathedral:
    if not args.cathedral.is_file():
        raise FileNotFoundError(args.cathedral)
    if args.cathedral.suffix.lower() not in (".glb",".gltf"):
        raise ValueError("Only glTF/GLB static scene supplied here.")
    bpy.ops.import_scene.gltf(filepath=str(args.cathedral.resolve()))
    print("Imported cathedral architecture, BUT procedural blockout also exists: hide/remove BLOCKOUT geometry and verify alignment before rendering.")

# Stationary, non-pulsing illumination.
world=bpy.context.scene.world
world.use_nodes=True
world.node_tree.nodes["Background"].inputs["Color"].default_value=(0.055,0.068,0.09,1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value=0.40

for i in range(9):
    light=bpy.data.lights.new(name=f"Static mural wash {i:02d}",type="AREA")
    light.energy=850
    light.shape="RECTANGLE"
    light.size=5.4
    light.size_y=3.1
    ob=bpy.data.objects.new(light.name,light)
    bpy.context.collection.objects.link(ob)
    ob.location=(-width/2+(i+0.5)*width/9,-3.5,6.5)
    target=Vector((ob.location.x,0,3))
    ob.rotation_euler=(target-Vector(ob.location)).to_track_quat("-Z","Y").to_euler()

camera_data=bpy.data.cameras.new("Only animated camera")
camera=bpy.data.objects.new("ONLY MOVING OBJECT / CAMERA",camera_data)
bpy.context.collection.objects.link(camera)
scene=bpy.context.scene
scene.camera=camera
camera_data.lens=48
camera_data.clip_end=250

def set_pose(seconds, u, y=-4.5, z=3.15, lens=48, focus_x=None):
    # Never run leftwards during the linear lyrical journey.
    x=max(-width/2+1.40,min(width/2-1.40,-width/2+width*u))
    t=(seconds*args.fps)+1
    camera.location=(x,y,z)
    target=Vector((x if focus_x is None else focus_x,0.0,z0+height/2))
    camera.rotation_euler=(target-Vector(camera.location)).to_track_quat("-Z","Y").to_euler()
    camera.data.lens=lens
    camera.keyframe_insert(data_path="location",frame=t)
    camera.keyframe_insert(data_path="rotation_euler",frame=t)
    camera.data.keyframe_insert(data_path="lens",frame=t)

set_pose(0.0,0.0)
for i,panel in enumerate(panels):
    set_pose(float(panel["end_s"]),(i+1)/count)
# Last lyric: continue to right edge then pull back into cathedral, no reverse pan.
end=manifest["horizontal_story_end_s"]
set_pose(manifest["song_duration_s"],1.0,y=-28.0,z=8.2,lens=18,focus_x=0.0)

# Smooth clamped Bézier curves to avoid overshoot (especially important for x)
# and preserve one-directional travel.
objects=[camera,camera.data]
for obj in objects:
    animation=obj.animation_data
    if not animation or not animation.action: continue
    action=animation.action
    fcurves=getattr(action,"fcurves",None)
    # Blender 4.4+ layered actions may expose fcurves through channelbags.
    if fcurves is None:
        continue
    for fc in fcurves:
        for key in fc.keyframe_points:
            key.interpolation="BEZIER"
            key.handle_left_type="AUTO_CLAMPED"
            key.handle_right_type="AUTO_CLAMPED"

# Detect any accidentally imported animated geometry: only the camera may move.
for obj in bpy.data.objects:
    if obj is not camera and obj.animation_data and obj.animation_data.action:
        raise RuntimeError(f"Non-camera animation prohibited: {obj.name}")

scene.frame_start=1
scene.frame_end=math.ceil(manifest["song_duration_s"]*args.fps)+1
scene.render.fps=args.fps
scene.render.resolution_x=1920
scene.render.resolution_y=1080
scene.render.resolution_percentage=args.preview_res
scene.render.image_settings.file_format="PNG"
try:
    scene.render.engine="BLENDER_EEVEE_NEXT"
except (TypeError,ValueError):
    try:
        scene.render.engine="BLENDER_EEVEE"
    except (TypeError,ValueError):
        scene.render.engine="CYCLES"
try:
    scene.view_settings.view_transform="AgX"
except (TypeError,ValueError):
    scene.view_settings.view_transform="Standard"
args.save.parent.mkdir(parents=True,exist_ok=True)
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(args.save.resolve()))
print(f"Saved static 3D cathedral BLOCKOUT + lyric-timed camera: {args.save}")
print("No render performed, no proof video claimed. Replace blockout with high-quality cathedral before final export.")
