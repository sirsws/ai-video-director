"""Runnable starter/smoke scene: a person follows a moving target through a gate.

blender --background --python previs_example.py -- --out <temp-folder> --ffmpeg <exe>
Illustrates explicit target, persistent geometry and exports, not validated choreography.
"""
from pathlib import Path
import argparse
import json
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from previs_common import setup, box, ball, Human, camera, aim, key, path_at, render

parser = argparse.ArgumentParser()
parser.add_argument('--out', required=True)
parser.add_argument('--ffmpeg')
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
scene = setup(fps=12, frames=24, size=(240, 400))
box('Ground', (0, 1, -.15), (10, 16, .3))
for x in (-2.5, 2.5):
    box('Gate pier', (x, 2, 1.7), (1, .5, 3.4))
box('Gate lintel', (0, 2, 3.6), (6, .5, .4))
target = ball('Moving target', (0, 0, 1.5), (.2, .3, .2), (.95, .3, .1))
person = Human('Follower')
cam = camera(lens=26)
count = len(bpy.data.objects)
route = [(0, (0, -2, 0)), (23 / 12, (0, 4, 0))]
assert path_at(-1, route) == Vector(route[0][1])
assert path_at(99, route) == Vector(route[-1][1])
for frame in range(1, 25):
    t = (frame - 1) / 12
    pos = path_at(t, route)
    person.pose(position=pos, frame=frame)
    target.location = pos + Vector((0, 1.2, 1.5))
    key(target, frame)
    aim(cam, pos + Vector((1.4, -4.5, 2.6)), pos + Vector((0, .6, 1)))
    key(cam, frame)
    assert target.location.y > person.root.location.y
    assert len(bpy.data.objects) == count, 'Animation must not create per-frame copies'
out = Path(args.out)
seconds = render(out, tempfile.mkdtemp(prefix='previs-example-'),
                 ffmpeg=args.ffmpeg, keyframes=(1, 8, 16, 24))
for name in ('previs_common.py', 'previs_example.py'):
    src = Path(__file__).resolve().parent / name
    if src.resolve() != (out / name).resolve():
        shutil.copy2(src, out / name)
metrics = dict(objects=count, frames=24, render_seconds=round(seconds, 3),
               checks='fixed object count, explicit leading target, path endpoint clamping')
(out / 'smoke.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
print(json.dumps(metrics))
