import bpy
import xml.etree.ElementTree as ET
import math

# Path to your SVG file
svg_path = "/absolute/path/to/floorplan.svg"

# Clean up scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Function to create a wall from a path (just a straight extrusion)
def create_wall(points, height=2.5, thickness=0.1):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        
        dx, dy = x2 - x1, y2 - y1
        length = math.sqrt(dx**2 + dy**2)
        angle = math.atan2(dy, dx)
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=((x1 + x2)/2, (y1 + y2)/2, height / 2))
        obj = bpy.context.active_object
        obj.scale = (length / 2, thickness / 2, height / 2)
        obj.rotation_euler[2] = angle

# Function to parse simple path "M x y L x y ..." to points
def parse_path(d):
    coords = []
    tokens = d.replace(',', ' ').split()
    i = 0
    while i < len(tokens):
        cmd = tokens[i]
        i += 1
        if cmd in 'ML':
            x = float(tokens[i])
            y = float(tokens[i + 1])
            coords.append((x / 100, y / 100))  # scaling SVG to meters
            i += 2
    return coords

# Parse SVG
tree = ET.parse(svg_path)
root = tree.getroot()

# Namespaces
ns = {'svg': 'http://www.w3.org/2000/svg'}

# Find all paths under 'Wall' group
for g in root.findall(".//svg:g[@id='Wall']", ns):
    for path in g.findall(".//svg:path", ns):
        d = path.attrib.get('d')
        if d:
            points = parse_path(d)
            if len(points) > 1:
                create_wall(points)
