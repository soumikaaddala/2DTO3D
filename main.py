# Run this in a Colab cell
!pip install gdown
import gdown



# Install Kaggle API
!pip install -q kaggle

# Upload your Kaggle API key (upload kaggle.json file when prompted)
from google.colab import files
files.upload()

# Set up Kaggle API key
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json


# Download dataset using the correct Kaggle dataset identifier
!kaggle datasets download -d qmarva/cubicasa5k

# Unzip the downloaded dataset
!unzip -q cubicasa5k.zip -d cubicasa5k


import os, json
from PIL import Image
import matplotlib.pyplot as plt


!pip install svgpathtools trimesh shapely


# Install required libraries
!pip install svgpathtools numpy matplotlib trimesh

import os
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from svgpathtools import svg2paths


import trimesh

# Verify dataset path
dataset_path = "/content/cubicasa5k/cubicasa5k/cubicasa5k"
sample_house = os.path.join(dataset_path, "high_quality/107")
print("Sample house contents:", os.listdir(sample_house))

!pip install --upgrade svgpathtools

!pip install numpy matplotlib trimesh

!pip install --upgrade svgpathtools
!pip install numpy matplotlib trimesh opencv-python

import os
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import trimesh
from svgpathtools import parse_path

# SVG file path (adjust to your Google Drive path)
svg_path = "/content/cubicasa5k/cubicasa5k/cubicasa5k/high_quality/107/model.svg"

# Parse SVG with ElementTree
namespace = {'svg': 'http://www.w3.org/2000/svg'}
tree = ET.parse(svg_path)
root = tree.getroot()

# Collect paths from relevant groups
relevant_groups = ['Wall', 'Door', 'Window']
wall_paths = []
door_paths = []
window_paths = []

for g in root.findall('.//svg:g', namespace):
    group_id = g.attrib.get('id', '')
    if group_id in relevant_groups:
        for path in g.findall('.//svg:path', namespace):
            path_d = path.attrib.get('d', '')
            if path_d:
                if group_id == 'Wall':
                    wall_paths.append(path_d)
                elif group_id == 'Door':
                    door_paths.append(path_d)
                elif group_id == 'Window':
                    window_paths.append(path_d)

print(f"Found {len(wall_paths)} wall paths, {len(door_paths)} door paths, {len(window_paths)} window paths")

# Convert paths to 2D lines
wall_lines = []
for path_d in wall_paths:
    try:
        path = parse_path(path_d)
        for segment in path:
            start = (segment.start.real, segment.start.imag)
            end = (segment.end.real, segment.end.imag)
            if abs(start[0] - end[0]) > 1e-6 or abs(start[1] - end[1]) > 1e-6:  # Skip zero-length segments
                wall_lines.append([start, end])
    except Exception as e:
        print(f"Error parsing path {path_d[:50]}...: {e}")

# Plot 2D floor plan
plt.figure(figsize=(10, 10))
for line in wall_lines:
    x = [line[0][0], line[1][0]]
    y = [line[0][1], line[1][1]]
    plt.plot(x, y, 'b-')
plt.gca().set_aspect('equal')
plt.title("2D Floor Plan (Walls)")
plt.savefig("/content/wall_floor_plan_2d.png")
plt.show()

# Create 3D mesh for walls
wall_height = 3.0  # Meters
wall_thickness = 0.2  # Meters
meshes = []

for line in wall_lines:
    p1, p2 = np.array(line[0]), np.array(line[1])
    direction = p2 - p1
    length = np.linalg.norm(direction)
    if length < 1e-6:
        continue
    direction /= length
    perpendicular = np.array([-direction[1], direction[0]])

    vertices = [
        p1 + perpendicular * wall_thickness / 2,
        p1 - perpendicular * wall_thickness / 2,
        p2 - perpendicular * wall_thickness / 2,
        p2 + perpendicular * wall_thickness / 2,
        p1 + perpendicular * wall_thickness / 2 + np.array([0, wall_height]),
        p1 - perpendicular * wall_thickness / 2 + np.array([0, wall_height]),
        p2 - perpendicular * wall_thickness / 2 + np.array([0, wall_height]),
        p2 + perpendicular * wall_thickness / 2 + np.array([0, wall_height]),
    ]
    faces = [
        [0, 1, 2], [2, 3, 0],
        [4, 5, 6], [6, 7, 4],
        [0, 4, 5], [5, 1, 0],
        [1, 5, 6], [6, 2, 1],
        [2, 6, 7], [7, 3, 2],
        [3, 7, 4], [4, 0, 3],
    ]
    wall_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    meshes.append(wall_mesh)

# Combine meshes
scene = trimesh.Scene()
for mesh in meshes:
    scene.add_geometry(mesh)

# Export 3D model
scene.export("/content/floor_plan_3d.obj")
print("3D model saved as floor_plan_3d.obj")

import os
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import trimesh
from svgpathtools import parse_path

# SVG file path (adjust if needed)
svg_path = "/content/cubicasa5k/cubicasa5k/cubicasa5k/high_quality/107/model.svg"

# Parse SVG (re-run to ensure data is fresh)
namespace = {'svg': 'http://www.w3.org/2000/svg'}
tree = ET.parse(svg_path)
root = tree.getroot()

# Collect paths from relevant groups
relevant_groups = ['Wall', 'Door', 'Window']
wall_paths = []
door_paths = []
window_paths = []

for g in root.findall('.//svg:g', namespace):
    group_id = g.attrib.get('id', '')
    if group_id in relevant_groups:
        for path in g.findall('.//svg:path', namespace):
            path_d = path.attrib.get('d', '')
            if path_d:
                if group_id == 'Wall':
                    wall_paths.append(path_d)
                elif group_id == 'Door':
                    door_paths.append(path_d)
                elif group_id == 'Window':
                    window_paths.append(path_d)

print(f"Found {len(wall_paths)} wall paths, {len(door_paths)} door paths, {len(window_paths)} window paths")

# Convert paths to 2D lines
wall_lines = []
door_lines = []

for path_d in wall_paths:
    try:
        path = parse_path(path_d)
        for segment in path:
            start = (segment.start.real, segment.start.imag)
            end = (segment.end.real, segment.end.imag)
            if abs(start[0] - end[0]) > 1e-6 or abs(start[1] - end[1]) > 1e-6:
                wall_lines.append([start, end])
    except Exception as e:
        print(f"Error parsing wall path {path_d[:50]}...: {e}")

for path_d in door_paths:
    try:
        path = parse_path(path_d)
        for segment in path:
            start = (segment.start.real, segment.start.imag)
            end = (segment.end.real, segment.end.imag)
            if abs(start[0] - end[0]) > 1e-6 or abs(start[1] - end[1]) > 1e-6:
                door_lines.append([start, end])
    except Exception as e:
        print(f"Error parsing door path {path_d[:50]}...: {e}")

# Plot 2D floor plan with walls and doors
plt.figure(figsize=(10, 10))
for line in wall_lines:

    x = [line[0][0], line[1][0]]
    y = [line[0][1], line[1][1]]
    plt.plot(x, y, 'b-', label='Walls' if 'Walls' not in plt.gca().get_legend_handles_labels()[1] else '')
for line in door_lines:
    x = [line[0][0], line[1][0]]
    y = [line[0][1], line[1][1]]
    plt.plot(x, y, 'r--', label='Doors' if 'Doors' not in plt.gca().get_legend_handles_labels()[1] else '')
plt.gca().set_aspect('equal')
plt.legend()
plt.title("2D Floor Plan (Walls and Doors)")
plt.savefig("/content/floor_plan_2d.png")
plt.show()

# Create 3D mesh for walls and doors
wall_height = 3.0  # Meters
wall_thickness = 0.2  # Meters
door_height = 2.0  # Meters
door_thickness = 0.1  # Meters
meshes = []

# Extrude walls
for line in wall_lines:
    p1, p2 = np.array(line[0]), np.array(line[1])
    direction = p2 - p1
    length = np.linalg.norm(direction)
    if length < 1e-6:
        continue
    direction /= length
    perpendicular = np.array([-direction[1], direction[0]])

    vertices = [
        p1 + perpendicular * wall_thickness / 2,
        p1 - perpendicular * wall_thickness / 2,
        p2 - perpendicular * wall_thickness / 2,
        p2 + perpendicular * wall_thickness / 2,
        p1 + perpendicular * wall_thickness / 2 + np.array([0, wall_height]),
        p1 - perpendicular * wall_thickness / 2 + np.array([0, wall_height]),
        p2 - perpendicular * wall_thickness / 2 + np.array([0, wall_height]),
        p2 + perpendicular * wall_thickness / 2 + np.array([0, wall_height]),
    ]
    faces = [
        [0, 1, 2], [2, 3, 0],
        [4, 5, 6], [6, 7, 4],
        [0, 4, 5], [5, 1, 0],
        [1, 5, 6], [6, 2, 1],
        [2, 6, 7], [7, 3, 2],
        [3, 7, 4], [4, 0, 3],
    ]
    wall_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    meshes.append(wall_mesh)

# Extrude doors
for line in door_lines:
    p1, p2 = np.array(line[0]), np.array(line[1])
    direction = p2 - p1
    length = np.linalg.norm(direction)
    if length < 1e-6:
        continue
    direction /= length
    perpendicular = np.array([-direction[1], direction[0]])

    vertices = [
        p1 + perpendicular * door_thickness / 2,
        p1 - perpendicular * door_thickness / 2,
        p2 - perpendicular * door_thickness / 2,
        p2 + perpendicular * door_thickness / 2,
        p1 + perpendicular * door_thickness / 2 + np.array([0, door_height]),
        p1 - perpendicular * door_thickness / 2 + np.array([0, door_height]),
        p2 - perpendicular * door_thickness / 2 + np.array([0, door_height]),
        p2 + perpendicular * door_thickness / 2 + np.array([0, door_height]),
    ]
    faces = [
        [0, 1, 2], [2, 3, 0],
        [4, 5, 6], [6, 7, 4],
        [0, 4, 5], [5, 1, 0],
        [1, 5, 6], [6, 2, 1],
        [2, 6, 7], [7, 3, 2],
        [3, 7, 4], [4, 0, 3],
    ]
    door_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    meshes.append(door_mesh)

# Combine meshes
scene = trimesh.Scene()
for mesh in meshes:
    scene.add_geometry(mesh)

# Export 3D model
scene.export("/content/floor_plan_3d.obj")
print("3D model saved as /content/floor_plan_3d.obj")

import os
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import trimesh
from svgpathtools import parse_path

# SVG file path (adjust to your Google Drive path)
svg_path = "/content/cubicasa5k/cubicasa5k/cubicasa5k/high_quality/107/model.svg"

# Parse SVG
namespace = {'svg': 'http://www.w3.org/2000/svg'}
tree = ET.parse(svg_path)
root = tree.getroot()

# Collect paths from relevant groups
relevant_groups = ['Wall', 'Door', 'Window']
wall_paths = []
door_paths = []
window_paths = []

for g in root.findall('.//svg:g', namespace):
    group_id = g.attrib.get('id', '')
    if group_id in relevant_groups:
        for path in g.findall('.//svg:path', namespace):
            path_d = path.attrib.get('d', '')
            if path_d:
                if group_id == 'Wall':
                    wall_paths.append(path_d)
                elif group_id == 'Door':
                    door_paths.append(path_d)
                elif group_id == 'Window':
                    window_paths.append(path_d)

print(f"Found {len(wall_paths)} wall paths, {len(door_paths)} door paths, {len(window_paths)} window paths")

# Check Window, Glass, and Panel groups for paths or polylines
check_groups = ['Window', 'Glass', 'Panel']
for g in root.findall('.//svg:g', namespace):
    group_id = g.attrib.get('id', '')
    if group_id in check_groups:
        paths = g.findall('.//svg:path', namespace)
        polylines = g.findall('.//svg:polyline', namespace)
        print(f"Group {group_id}: {len(paths)} paths, {len(polylines)} polylines")
        for path in paths:
            print(f"  Path: {path.attrib.get('d', '')[:50]}...")
        for polyline in polylines:
            print(f"  Polyline: points={polyline.attrib.get('points', '')[:50]}...")

# Convert paths to 2D lines
wall_lines = []
door_lines = []

for path_d in wall_paths:
    try:
        path = parse_path(path_d)
        for segment in path:
            start = (segment.start.real, segment.start.imag)
            end = (segment.end.real, segment.end.imag)
            if abs(start[0] - end[0]) > 1e-6 or abs(start[1] - end[1]) > 1e-6:
                wall_lines.append([start, end])
    except Exception as e:
        print(f"Error parsing wall path {path_d[:50]}...: {e}")

for path_d in door_paths:
    try:
        path = parse_path(path_d)
        for segment in path:
            start = (segment.start.real, segment.start.imag)
            end = (segment.end.real, segment.end.imag)
            if abs(start[0] - end[0]) > 1e-6 or abs(start[1] - end[1]) > 1e-6:
                door_lines.append([start, end])
    except Exception as e:
        print(f"Error parsing door path {path_d[:50]}...: {e}")

# Plot 2D floor plan with walls and doors
plt.figure(figsize=(10, 10))
for line in wall_lines:
    x = [line[0][0], line[1][0]]
    y = [line[0][1], line[1][1]]
    plt.plot(x, y, 'b-', label='Walls' if 'Walls' not in plt.gca().get_legend_handles_labels()[1] else '')
for line in door_lines:
    x = [line[0][0], line[1][0]]
    y = [line[0][1], line[1][1]]
    plt.plot(x, y, 'r--', label='Doors' if 'Doors' not in plt.gca().get_legend_handles_labels()[1] else '')
plt.gca().set_aspect('equal')
plt.legend()
plt.title("2D Floor Plan (Walls and Doors)")
plt.savefig("/content/floor_plan_2d.png")
plt.show()

# Create 3D mesh for walls and doors
wall_height = 3.0  # Meters
wall_thickness = 0.2  # Meters
door_height = 2.0  # Meters
door_thickness = 0.1  # Meters
meshes = []

# Scale coordinates (if SVG uses pixels, adjust to meters)
scale_factor = 0.01  # Assuming 1 pixel = 1 cm, adjust as needed
wall_lines = [[[x * scale_factor, y * scale_factor] for x, y in line] for line in wall_lines]
door_lines = [[[x * scale_factor, y * scale_factor] for x, y in line] for line in door_lines]

# Extrude walls
for line in wall_lines:
    p1, p2 = np.array(line[0]), np.array(line[1])
    direction = p2 - p1
    length = np.linalg.norm(direction)
    if length < 1e-6:
        continue
    direction /= length
    perpendicular = np.array([-direction[1], direction[0]])

    # Ensure vertices are 3D
    vertices = [
        np.array([p1[0] + perpendicular[0] * wall_thickness / 2, p1[1] + perpendicular[1] * wall_thickness / 2, 0]),
        np.array([p1[0] - perpendicular[0] * wall_thickness / 2, p1[1] - perpendicular[1] * wall_thickness / 2, 0]),
        np.array([p2[0] - perpendicular[0] * wall_thickness / 2, p2[1] - perpendicular[1] * wall_thickness / 2, 0]),
        np.array([p2[0] + perpendicular[0] * wall_thickness / 2, p2[1] + perpendicular[1] * wall_thickness / 2, 0]),
        np.array([p1[0] + perpendicular[0] * wall_thickness / 2, p1[1] + perpendicular[1] * wall_thickness / 2, wall_height]),
        np.array([p1[0] - perpendicular[0] * wall_thickness / 2, p1[1] - perpendicular[1] * wall_thickness / 2, wall_height]),
        np.array([p2[0] - perpendicular[0] * wall_thickness / 2, p2[1] - perpendicular[1] * wall_thickness / 2, wall_height]),
        np.array([p2[0] + perpendicular[0] * wall_thickness / 2, p2[1] + perpendicular[1] * wall_thickness / 2, wall_height]),
    ]
    faces = [
        [0, 1, 2], [2, 3, 0],
        [4, 5, 6], [6, 7, 4],
        [0, 4, 5], [5, 1, 0],
        [1, 5, 6], [6, 2, 1],
        [2, 6, 7], [7, 3, 2],
        [3, 7, 4], [4, 0, 3],
    ]
    wall_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    # Validate mesh
    if not wall_mesh.is_empty and wall_mesh.is_watertight:
        meshes.append(wall_mesh)
    else:
        print(f"Skipping invalid wall mesh: {wall_mesh.vertices.shape}, {wall_mesh.faces.shape}")

# Extrude doors
for line in door_lines:
    p1, p2 = np.array(line[0]), np.array(line[1])
    direction = p2 - p1
    length = np.linalg.norm(direction)
    if length < 1e-6:
        continue
    direction /= length
    perpendicular = np.array([-direction[1], direction[0]])

    vertices = [
        np.array([p1[0] + perpendicular[0] * door_thickness / 2, p1[1] + perpendicular[1] * door_thickness / 2, 0]),
        np.array([p1[0] - perpendicular[0] * door_thickness / 2, p1[1] - perpendicular[1] * door_thickness / 2, 0]),
        np.array([p2[0] - perpendicular[0] * door_thickness / 2, p2[1] - perpendicular[1] * door_thickness / 2, 0]),
        np.array([p2[0] + perpendicular[0] * door_thickness / 2, p2[1] + perpendicular[1] * door_thickness / 2, 0]),
        np.array([p1[0] + perpendicular[0] * door_thickness / 2, p1[1] + perpendicular[1] * door_thickness / 2, door_height]),
        np.array([p1[0] - perpendicular[0] * door_thickness / 2, p1[1] - perpendicular[1] * door_thickness / 2, door_height]),
        np.array([p2[0] - perpendicular[0] * door_thickness / 2, p2[1] - perpendicular[1] * door_thickness / 2, door_height]),
        np.array([p2[0] + perpendicular[0] * door_thickness / 2, p2[1] + perpendicular[1] * door_thickness / 2, door_height]),
    ]
    faces = [
        [0, 1, 2], [2, 3, 0],
        [4, 5, 6], [6, 7, 4],
        [0, 4, 5], [5, 1, 0],
        [1, 5, 6], [6, 2, 1],
        [2, 6, 7], [7, 3, 2],
        [3, 7, 4], [4, 0, 3],
    ]
    door_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    # Validate mesh
    if not door_mesh.is_empty and door_mesh.is_watertight:
        meshes.append(door_mesh)
    else:
        print(f"Skipping invalid door mesh: {door_mesh.vertices.shape}, {door_mesh.faces.shape}")

# Combine meshes
scene = trimesh.Scene()
for mesh in meshes:
    scene.add_geometry(mesh)

# Validate scene before export
if not meshes:
    print("No valid meshes to export!")
else:
    # Export 3D model
    scene.export("/content/floor_plan_3d.obj", file_type='obj')
    print("3D model saved as /content/floor_plan_3d.obj")
    # Export as GLTF as an alternative
    scene.export("/content/floor_plan_3d.gltf", file_type='gltf')
    print("3D model also saved as /content/floor_plan_3d.gltf")

import os
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import trimesh
from svgpathtools import parse_path

# SVG file path
svg_path = "/content/cubicasa5k/cubicasa5k/cubicasa5k/high_quality/107/model.svg"

# Parse SVG
namespace = {'svg': 'http://www.w3.org/2000/svg'}
tree = ET.parse(svg_path)
root = tree.getroot()

# Collect paths from Floor-1, Wall, and Door groups
wall_paths = []
door_paths = []
floor_paths = []

for g in root.findall('.//svg:g', namespace):
    group_id = g.attrib.get('id', '')
    for path in g.findall('.//svg:path', namespace):
        path_d = path.attrib.get('d', '')
        if not path_d:
            continue
        if group_id == 'Floor-1':
            floor_paths.append(path_d)
        elif group_id == 'Wall':
            wall_paths.append(path_d)
        elif group_id == 'Door':
            door_paths.append(path_d)

print(f"Found {len(floor_paths)} Floor-1 paths, {len(wall_paths)} Wall paths, {len(door_paths)} Door paths")

# Check Window, Glass, and Panel groups for paths or polylines
check_groups = ['Window', 'Glass', 'Panel']
for g in root.findall('.//svg:g', namespace):
    group_id = g.attrib.get('id', '')
    if group_id in check_groups:
        paths = g.findall('.//svg:path', namespace)
        polylines = g.findall('.//svg:polyline', namespace)
        print(f"Group {group_id}: {len(paths)} paths, {len(polylines)} polylines")
        for path in paths:
            print(f"  Path: {path.attrib.get('d', '')[:50]}...")
        for polyline in polylines:
            print(f"  Polyline: points={polyline.attrib.get('points', '')[:50]}...")

# Convert paths to 2D lines
wall_lines = []
door_lines = []

# Try Floor-1 paths first
if floor_paths:
    print("Using Floor-1 paths for walls...")
    for path_d in floor_paths:
        try:
            path = parse_path(path_d)
            # Sample points along the path to approximate straight lines
            points = []
            for t in np.linspace(0, 1, 10):  # Sample 10 points along the path
                point = path.point(t)
                points.append((point.real, point.imag))
            # Convert sampled points to line segments
            for i in range(len(points) - 1):
                if abs(points[i][0] - points[i+1][0]) > 1e-6 or abs(points[i][1] - points[i+1][1]) > 1e-6:
                    wall_lines.append([points[i], points[i+1]])
        except Exception as e:
            print(f"Error parsing Floor-1 path {path_d[:50]}...: {e}")
else:
    print("Using Wall paths with sampling...")
    for path_d in wall_paths:
        try:
            path = parse_path(path_d)
            # Sample points along the path to avoid triangular shapes
            points = []
            for t in np.linspace(0, 1, 10):
                point = path.point(t)
                points.append((point.real, point.imag))
            # Convert sampled points to line segments
            for i in range(len(points) - 1):
                if abs(points[i][0] - points[i+1][0]) > 1e-6 or abs(points[i][1] - points[i+1][1]) > 1e-6:
                    wall_lines.append([points[i], points[i+1]])
        except Exception as e:
            print(f"Error parsing Wall path {path_d[:50]}...: {e}")

for path_d in door_paths:
    try:
        path = parse_path(path_d)
        points = []
        for t in np.linspace(0, 1, 10):
            point = path.point(t)
            points.append((point.real, point.imag))
        for i in range(len(points) - 1):
            if abs(points[i][0] - points[i+1][0]) > 1e-6 or abs(points[i][1] - points[i+1][1]) > 1e-6:
                door_lines.append([points[i], points[i+1]])
    except Exception as e:
        print(f"Error parsing Door path {path_d[:50]}...: {e}")

# Plot 2D floor plan with walls and doors
plt.figure(figsize=(10, 10))
for line in wall_lines:
    x = [line[0][0], line[1][0]]
    y = [line[0][1], line[1][1]]
    plt.plot(x, y, 'b-', label='Walls' if 'Walls' not in plt.gca().get_legend_handles_labels()[1] else '')
for line in door_lines:
    x = [line[0][0], line[1][0]]
    y = [line[0][1], line[1][1]]
    plt.plot(x, y, 'r--', label='Doors' if 'Doors' not in plt.gca().get_legend_handles_labels()[1] else '')
plt.gca().set_aspect('equal')
plt.legend()
plt.title("2D Floor Plan (Walls and Doors)")
plt.savefig("/content/floor_plan_2d.png")
plt.show()

# Create 3D mesh for walls and doors
wall_height = 3.0  # Meters
wall_thickness = 0.2  # Meters
door_height = 2.0  # Meters
door_thickness = 0.1  # Meters
meshes = []

# Scale coordinates (adjust to meters)
scale_factor = 0.01  # 1 pixel = 1 cm
wall_lines = [[[x * scale_factor, y * scale_factor] for x, y in line] for line in wall_lines]
door_lines = [[[x * scale_factor, y * scale_factor] for x, y in line] for line in door_lines]

# Extrude walls
for line in wall_lines:
    p1, p2 = np.array(line[0]), np.array(line[1])
    direction = p2 - p1
    length = np.linalg.norm(direction)
    if length < 1e-6:
        continue
    direction /= length
    perpendicular = np.array([-direction[1], direction[0]])

    vertices = [
        np.array([p1[0] + perpendicular[0] * wall_thickness / 2, p1[1] + perpendicular[1] * wall_thickness / 2, 0]),
        np.array([p1[0] - perpendicular[0] * wall_thickness / 2, p1[1] - perpendicular[1] * wall_thickness / 2, 0]),
        np.array([p2[0] - perpendicular[0] * wall_thickness / 2, p2[1] - perpendicular[1] * wall_thickness / 2, 0]),
        np.array([p2[0] + perpendicular[0] * wall_thickness / 2, p2[1] + perpendicular[1] * wall_thickness / 2, 0]),
        np.array([p1[0] + perpendicular[0] * wall_thickness / 2, p1[1] + perpendicular[1] * wall_thickness / 2, wall_height]),
        np.array([p1[0] - perpendicular[0] * wall_thickness / 2, p1[1] - perpendicular[1] * wall_thickness / 2, wall_height]),
        np.array([p2[0] - perpendicular[0] * wall_thickness / 2, p2[1] - perpendicular[1] * wall_thickness / 2, wall_height]),
        np.array([p2[0] + perpendicular[0] * wall_thickness / 2, p2[1] + perpendicular[1] * wall_thickness / 2, wall_height]),
    ]
    faces = [
        [0, 1, 2], [2, 3, 0],
        [4, 5, 6], [6, 7, 4],
        [0, 4, 5], [5, 1, 0],
        [1, 5, 6], [6, 2, 1],
        [2, 6, 7], [7, 3, 2],
        [3, 7, 4], [4, 0, 3],
    ]
    wall_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    if not wall_mesh.is_empty and wall_mesh.is_watertight:
        meshes.append(wall_mesh)
    else:
        print(f"Skipping invalid wall mesh: {wall_mesh.vertices.shape}, {wall_mesh.faces.shape}")

# Extrude doors
for line in door_lines:
    p1, p2 = np.array(line[0]), np.array(line[1])
    direction = p2 - p1
    length = np.linalg.norm(direction)
    if length < 1e-6:
        continue
    direction /= length
    perpendicular = np.array([-direction[1], direction[0]])

    vertices = [
        np.array([p1[0] + perpendicular[0] * door_thickness / 2, p1[1] + perpendicular[1] * door_thickness / 2, 0]),
        np.array([p1[0] - perpendicular[0] * door_thickness / 2, p1[1] - perpendicular[1] * door_thickness / 2, 0]),
        np.array([p2[0] - perpendicular[0] * door_thickness / 2, p2[1] - perpendicular[1] * wall_thickness / 2, 0]),
        np.array([p2[0] + perpendicular[0] * door_thickness / 2, p2[1] + perpendicular[1] * door_thickness / 2, 0]),
        np.array([p1[0] + perpendicular[0] * door_thickness / 2, p1[1] + perpendicular[1] * door_thickness / 2, door_height]),
        np.array([p1[0] - perpendicular[0] * door_thickness / 2, p1[1] - perpendicular[1] * door_thickness / 2, door_height]),
        np.array([p2[0] - perpendicular[0] * door_thickness / 2, p2[1] - perpendicular[1] * door_thickness / 2, door_height]),
        np.array([p2[0] + perpendicular[0] * door_thickness / 2, p2[1] + perpendicular[1] * door_thickness / 2, door_height]),
    ]
    faces = [
        [0, 1, 2], [2, 3, 0],
        [4, 5, 6], [6, 7, 4],
        [0, 4, 5], [5, 1, 0],
        [1, 5, 6], [6, 2, 1],
        [2, 6, 7], [7, 3, 2],
        [3, 7, 4], [4, 0, 3],
    ]
    door_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    if not door_mesh.is_empty and door_mesh.is_watertight:
        meshes.append(door_mesh)
    else:
        print(f"Skipping invalid door mesh: {door_mesh.vertices.shape}, {door_mesh.faces.shape}")

# Combine meshes
scene = trimesh.Scene()
for mesh in meshes:
    scene.add_geometry(mesh)

# Export 3D model
if not meshes:
    print("No valid meshes to export!")
else:
    scene.export("/content/floor_plan_3d.obj", file_type='obj')
    print("3D model saved as /content/floor_plan_3d.obj")
    scene.export("/content/floor_plan_3d.gltf", file_type='gltf')
    print("3D model also saved as /content/floor_plan_3d.gltf")

import os
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import trimesh
from svgpathtools import parse_path

# SVG file path
svg_path = "/content/cubicasa5k/cubicasa5k/cubicasa5k/high_quality/107/model.svg"

# Parse SVG
namespace = {'svg': 'http://www.w3.org/2000/svg'}
tree = ET.parse(svg_path)
root = tree.getroot()

# Collect paths from Floor-1, Wall, and Door groups
wall_paths = []
door_paths = []
floor_paths = []

for g in root.findall('.//svg:g', namespace):
    group_id = g.attrib.get('id', '')
    for path in g.findall('.//svg:path', namespace):
        path_d = path.attrib.get('d', '')
        if not path_d:
            continue
        if group_id == 'Floor-1':
            floor_paths.append(path_d)
        elif group_id == 'Wall':
            wall_paths.append(path_d)
        elif group_id == 'Door':
            door_paths.append(path_d)

print(f"Found {len(floor_paths)} Floor-1 paths, {len(wall_paths)} Wall paths, {len(door_paths)} Door paths")

# Convert paths to 2D lines
wall_lines = []
door_lines = []

# Use Floor-1 paths for walls
for path_d in floor_paths:
    try:
        path = parse_path(path_d)
        points = []
        for t in np.linspace(0, 1, 10):
            point = path.point(t)
            points.append((point.real, point.imag))
        for i in range(len(points) - 1):
            if abs(points[i][0] - points[i+1][0]) > 1e-6 or abs(points[i][1] - points[i+1][1]) > 1e-6:
                wall_lines.append([points[i], points[i+1]])
    except Exception as e:
        print(f"Error parsing Floor-1 path {path_d[:50]}...: {e}")

for path_d in door_paths:
    try:
        path = parse_path(path_d)
        points = []
        for t in np.linspace(0, 1, 10):
            point = path.point(t)
            points.append((point.real, point.imag))
        for i in range(len(points) - 1):
            if abs(points[i][0] - points[i+1][0]) > 1e-6 or abs(points[i][1] - points[i+1][1]) > 1e-6:
                door_lines.append([points[i], points[i+1]])
    except Exception as e:
        print(f"Error parsing Door path {path_d[:50]}...: {e}")

# Scale coordinates
scale_factor = 0.01  # 1 pixel = 1 cm
wall_lines = [[[x * scale_factor, y * scale_factor] for x, y in line] for line in wall_lines]
door_lines = [[[x * scale_factor, y * scale_factor] for x, y in line] for line in door_lines]

# Create 3D mesh for walls and doors
wall_height = 3.0  # Meters
wall_thickness = 0.2  # Meters
door_height = 2.0  # Meters
door_thickness = 0.1  # Meters
meshes = []

# Extrude walls
for line in wall_lines:
    p1, p2 = np.array(line[0]), np.array(line[1])
    direction = p2 - p1
    length = np.linalg.norm(direction)
    if length < 1e-6:
        continue
    direction /= length
    perpendicular = np.array([-direction[1], direction[0]])

    vertices = [
        np.array([p1[0] + perpendicular[0] * wall_thickness / 2, p1[1] + perpendicular[1] * wall_thickness / 2, 0]),
        np.array([p1[0] - perpendicular[0] * wall_thickness / 2, p1[1] - perpendicular[1] * wall_thickness / 2, 0]),
        np.array([p2[0] - perpendicular[0] * wall_thickness / 2, p2[1] - perpendicular[1] * wall_thickness / 2, 0]),
        np.array([p2[0] + perpendicular[0] * wall_thickness / 2, p2[1] + perpendicular[1] * wall_thickness / 2, 0]),
        np.array([p1[0] + perpendicular[0] * wall_thickness / 2, p1[1] + perpendicular[1] * wall_thickness / 2, wall_height]),
        np.array([p1[0] - perpendicular[0] * wall_thickness / 2, p1[1] - perpendicular[1] * wall_thickness / 2, wall_height]),
        np.array([p2[0] - perpendicular[0] * wall_thickness / 2, p2[1] - perpendicular[1] * wall_thickness / 2, wall_height]),
        np.array([p2[0] + perpendicular[0] * wall_thickness / 2, p2[1] + perpendicular[1] * wall_thickness / 2, wall_height]),
    ]
    faces = [
        [0, 1, 2], [2, 3, 0],
        [4, 5, 6], [6, 7, 4],
        [0, 4, 5], [5, 1, 0],
        [1, 5, 6], [6, 2, 1],
        [2, 6, 7], [7, 3, 2],
        [3, 7, 4], [4, 0, 3],
    ]
    wall_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    if not wall_mesh.is_empty and wall_mesh.is_watertight:
        meshes.append(wall_mesh)

# Extrude doors
for line in door_lines:
    p1, p2 = np.array(line[0]), np.array(line[1])
    direction = p2 - p1
    length = np.linalg.norm(direction)
    if length < 1e-6:
        continue
    direction /= length
    perpendicular = np.array([-direction[1], direction[0]])

    vertices = [
        np.array([p1[0] + perpendicular[0] * door_thickness / 2, p1[1] + perpendicular[1] * door_thickness / 2, 0]),
        np.array([p1[0] - perpendicular[0] * door_thickness / 2, p1[1] - perpendicular[1] * door_thickness / 2, 0]),
        np.array([p2[0] - perpendicular[0] * door_thickness / 2, p2[1] - perpendicular[1] * door_thickness / 2, 0]),
        np.array([p2[0] + perpendicular[0] * door_thickness / 2, p2[1] + perpendicular[1] * door_thickness / 2, 0]),
        np.array([p1[0] + perpendicular[0] * door_thickness / 2, p1[1] + perpendicular[1] * door_thickness / 2, door_height]),
        np.array([p1[0] - perpendicular[0] * door_thickness / 2, p1[1] - perpendicular[1] * door_thickness / 2, door_height]),
        np.array([p2[0] - perpendicular[0] * door_thickness / 2, p2[1] - perpendicular[1] * door_thickness / 2, door_height]),
        np.array([p2[0] + perpendicular[0] * door_thickness / 2, p2[1] + perpendicular[1] * door_thickness / 2, door_height]),
    ]
    faces = [
        [0, 1, 2], [2, 3, 0],
        [4, 5, 6], [6, 7, 4],
        [0, 4, 5], [5, 1, 0],
        [1, 5, 6], [6, 2, 1],
        [2, 6, 7], [7, 3, 2],
        [3, 7, 4], [4, 0, 3],
    ]
    door_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    if not door_mesh.is_empty and door_mesh.is_watertight:
        meshes.append(door_mesh)

# Add a floor mesh
if wall_lines:
    all_points = np.array([pt for line in wall_lines for pt in line])
    min_xy = np.min(all_points, axis=0)
    max_xy = np.max(all_points, axis=0)
    floor_vertices = [
        [min_xy[0], min_xy[1], 0],
        [max_xy[0], min_xy[1], 0],
        [max_xy[0], max_xy[1], 0],
        [min_xy[0], max_xy[1], 0],
    ]
    floor_faces = [[0, 1, 2], [2, 3, 0]]
    floor_mesh = trimesh.Trimesh(vertices=floor_vertices, faces=floor_faces)
    meshes.append(floor_mesh)

# Combine meshes
scene = trimesh.Scene()
for mesh in meshes:
    scene.add_geometry(mesh)

# Export 3D model
if not meshes:
    print("No valid meshes to export!")
else:
    scene.export("/content/floor_plan_3d_with_floor.obj", file_type='obj')
    print("3D model saved as /content/floor_plan_3d_with_floor.obj")
    scene.export("/content/floor_plan_3d_with_floor.gltf", file_type='gltf')
    print("3D model also saved as /content/floor_plan_3d_with_floor.gltf")

