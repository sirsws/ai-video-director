"""Small Blender blocking helpers; run inside Blender, not system Python.

Objects are created once; animate transforms with key()/Human.pose().
No physics, chase logic, camera planning or aesthetic validation is implied.
"""
from pathlib import Path
import shutil
import subprocess
import time

import bpy
from mathutils import Vector


def setup(*, fps=12, frames=48, size=(360, 640)):
    """Reset the current scene. Use in a new background Blender process."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.context.preferences.filepaths.save_version = 0
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.render.resolution_x, scene.render.resolution_y = size
    scene.render.resolution_percentage = 100
    scene.render.fps = fps
    scene.frame_start, scene.frame_end = 1, frames
    scene.render.image_settings.file_format = 'PNG'
    scene.display.shading.light = 'STUDIO'
    scene.display.shading.color_type = 'OBJECT'
    scene.display.shading.background_type = 'WORLD'
    scene.world.color = (.18, .18, .18)
    return scene


def box(name, position, size, color=(.5, .5, .5)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    obj = bpy.context.object
    obj.name, obj.dimensions, obj.color = name, size, (*color, 1)
    return obj


def ball(name, position, size=(.2, .2, .2), color=(.5, .5, .5)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, location=position)
    obj = bpy.context.object
    obj.name, obj.scale, obj.color = name, size, (*color, 1)
    return obj


def place_link(obj, start, end):
    """Place an existing unit-depth cylinder between endpoints; no force simulation."""
    a, b = Vector(start), Vector(end)
    delta = b - a
    obj.location = (a + b) / 2
    obj.scale.z = delta.length
    if delta.length > 1e-8:
        obj.rotation_euler = delta.to_track_quat('Z', 'Y').to_euler()


def link(name, start, end, radius=.04, color=(.9, .5, .1)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=radius, depth=1)
    obj = bpy.context.object
    obj.name, obj.color = name, (*color, 1)
    place_link(obj, start, end)
    return obj


def key(obj, frame, props=('location', 'rotation_euler', 'scale')):
    # Explicit linear interpolation avoids hidden ease/overshoot between states.
    for prop in props:
        obj.keyframe_insert(data_path=prop, frame=frame)
    action = obj.animation_data.action
    for layer in action.layers:
        for strip in layer.strips:
            bag = strip.channelbag(obj.animation_data.action_slot)
            if bag:
                for curve in bag.fcurves:
                    for point in curve.keyframe_points:
                        point.interpolation = 'LINEAR'


def path_at(t, points):
    """Piecewise linear [(time, xyz), ...]; times must increase strictly."""
    if not points or any(b[0] <= a[0] for a, b in zip(points, points[1:])):
        raise ValueError('Provide nonempty points with strictly increasing times')
    if t <= points[0][0]:
        return Vector(points[0][1])
    for (ta, a), (tb, b) in zip(points, points[1:]):
        if t <= tb:
            return Vector(a).lerp(Vector(b), (t - ta) / (tb - ta))
    return Vector(points[-1][1])


def camera(name='Camera', lens=28):
    bpy.ops.object.camera_add()
    obj = bpy.context.object
    obj.name, obj.data.lens = name, lens
    bpy.context.scene.camera = obj
    return obj


def aim(obj, position, target):
    obj.location = position
    delta = Vector(target) - Vector(position)
    if delta.length == 0:
        raise ValueError('Camera position and target must differ')
    obj.rotation_euler = delta.to_track_quat('-Z', 'Y').to_euler()


class Human:
    """Complete jointed proxy facing +Y, feet at Z=0, local joints overrideable.

    Pose specifies geometry, not balance, locomotion or IK. Head nose shows facing.
    """
    joints = dict(hip=(0, 0, .9), chest=(0, 0, 1.4), head=(0, 0, 1.65),
                  ls=(-.23, 0, 1.4), le=(-.28, 0, 1.1), lh=(-.28, 0, .85),
                  rs=(.23, 0, 1.4), re=(.28, 0, 1.1), rh=(.28, 0, .85),
                  lk=(-.14, 0, .48), lf=(-.14, 0, .08),
                  rk=(.14, 0, .48), rf=(.14, 0, .08))
    bones = (('hip', 'chest'), ('ls', 'rs'), ('ls', 'le'), ('le', 'lh'),
             ('rs', 're'), ('re', 'rh'), ('hip', 'lk'), ('lk', 'lf'),
             ('hip', 'rk'), ('rk', 'rf'))

    def __init__(self, name, color=(.15, .5, .85)):
        self.root = bpy.data.objects.new(name, None)
        bpy.context.scene.collection.objects.link(self.root)
        self.parts = [link(name + f'-bone-{i}', (0, 0, 0), (0, 0, 1),
                           .2 if i == 0 else .07, color) for i in range(len(self.bones))]
        self.head = ball(name + '-head', (0, 0, 0), (.18, .18, .22), color)
        self.nose = ball(name + '-facing', (0, 0, 0), (.055, .09, .055), color)
        self.feet = [ball(name + '-foot-' + side, (0, 0, 0), (.10, .20, .08), color)
                     for side in ('left', 'right')]
        for obj in self.parts + [self.head, self.nose] + self.feet:
            obj.parent = self.root
        self.pose()

    def pose(self, *, position=(0, 0, 0), yaw=0, joints=None, frame=None):
        j = {**self.joints, **(joints or {})}
        self.root.location, self.root.rotation_euler.z = position, yaw
        for obj, (a, b) in zip(self.parts, self.bones):
            place_link(obj, j[a], j[b])
        self.head.location = j['head']
        self.nose.location = Vector(j['head']) + Vector((0, .19, 0))
        for foot, joint in zip(self.feet, ('lf', 'rf')):
            foot.location = Vector(j[joint]) + Vector((0, .08, 0))
        if frame is not None:
            for obj in [self.root, self.head, self.nose] + self.parts + self.feet:
                key(obj, frame)


def render(out, temp_frames, *, ffmpeg=None, keyframes=()):
    """Save scene, render PNGs to caller's OS-temp folder, optionally encode MP4.

    Use a unique temporary folder per run, so a failed render cannot reuse old frames.
    Pass an already located ffmpeg executable; no installation or network access.
    """
    out, temp_frames = Path(out), Path(temp_frames)
    out.mkdir(parents=True, exist_ok=True)
    temp_frames.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    scene.frame_set(scene.frame_start)
    scene.render.filepath = str(temp_frames / 'frame_')
    bpy.ops.wm.save_as_mainfile(filepath=str(out / 'scene.blend'))
    start = time.perf_counter()
    bpy.ops.render.render(animation=True)
    elapsed = time.perf_counter() - start
    for f in keyframes:
        shutil.copy2(temp_frames / f'frame_{f:04d}.png', out / f'key-{f:04d}.png')
    if ffmpeg:
        subprocess.run([str(ffmpeg), '-y', '-framerate', str(scene.render.fps),
                        '-start_number', str(scene.frame_start), '-i', str(temp_frames / 'frame_%04d.png'),
                        '-frames:v', str(scene.frame_end - scene.frame_start + 1),
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(out / 'preview.mp4')],
                       check=True, capture_output=True)
    return elapsed
