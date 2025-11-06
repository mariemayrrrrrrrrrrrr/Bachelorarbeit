import json
import numpy as np
from perlin_noise import octave_perlin
import random

# ---------------- Parameter ----------------
MAP_SIZE = (200, 200)  # Breite x Höhe
MAX_HEIGHT = 2.4       # Maximale Höhe des Terrains
SCALE = 100.0           # Skalenfaktor für Perlin Noise (größer = glatter)
EXPO = 1.1             # Höhenanpassung hebt Berge hervor
COLORS = {
    "water": [0.02, 0.15, 0.3],     # dunkleres Blau
    "sand": [0.6, 0.55, 0.4],       # dunkleres, leicht bräunliches Sand
    "grass": [0.1, 0.35, 0.1],      # dunkleres Grün
    "forest": [0.03, 0.18, 0.07],   # dichter Wald, tiefgrün
    "rock": [0.35, 0.32, 0.3],      # dunklerer Stein
    "snow": [0.85, 0.87, 0.9]       # leicht gedämpftes Weiß  
}

# ---------------- Perlin Noise ----------------
def update_point(x, y):
    return octave_perlin(x / SCALE, y / SCALE, octaves=6, persistence=0.5)

# ---------------- Normalisierung ----------------
#suchen den kleinsten wer im Array und teilen es durch den Größten um so werte zwischen 0-1 zu bekommen
def normalize(arr):
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))

# ---------------- get_color ----------------
def lerp_color(color1, color2, t):
    "Zwischenwert zwischen zwei bekannten Werten zu berechnen."
    return [
        color1[i] * (1 - t) + color2[i] * t
        for i in range(3)
    ]
def get_color(height, slope):
    # Sonderfall: steile Felsen
    if 0.25 < height < 0.9 and slope > 0.45:
        return COLORS["rock"]

    # Wasser → Sand Übergang
    if height <= 0.1:
        return COLORS["water"]
    elif height <= 0.2:
        #normierter Abstand zwischen zwei Punkten = Interpolationswert
        t = (height - 0.1) / (0.15 - 0.1)
        return lerp_color(COLORS["water"], COLORS["sand"], t)

    # Sand → Gras
    elif height <= 0.3:
        t = (height - 0.15) / (0.3 - 0.15)
        return lerp_color(COLORS["sand"], COLORS["grass"], t)

    # Gras → Wald
    elif height <= 0.6:
        t = (height - 0.3) / (0.6 - 0.3)
        return lerp_color(COLORS["grass"], COLORS["forest"], t)

    # Wald → Felsen
    elif height <= 0.85:
        t = (height - 0.6) / (0.85 - 0.6)
        return lerp_color(COLORS["forest"], COLORS["rock"], t)

    # Felsen → Schnee
    else:
        t = min((height - 0.85) / (1.0 - 0.85), 1)
        return lerp_color(COLORS["rock"], COLORS["snow"], t)


# ---------------- Heightmap ----------------
#an jeden Punkt der Map den Perlin Noise Wert zuweisen
heightmap = np.zeros(MAP_SIZE)
for x in range(MAP_SIZE[0]):
    for y in range(MAP_SIZE[1]):
        heightmap[x][y] = update_point(x, y)

heightmap = np.power(normalize(heightmap), EXPO)

# ---------------- Vertices und Faces ----------------
vertices = []
colors=[]
faces = []

def compute_slope(heightmap, x, y):
    width, height = heightmap.shape
    dzdx = 0
    dzdy = 0
    if x > 0 and x < width-1:
        dzdx = abs(heightmap[x+1][y] - heightmap[x-1][y])
    if y > 0 and y < height-1:
        dzdy = abs(heightmap[x][y+1] - heightmap[x][y-1])
    slope = np.sqrt(dzdx**2 + dzdy**2)
    return slope

# sie speichern die Koordinaten: wo ist der Punkt und wie hoch liegt er.
width, height = MAP_SIZE
for x in range(width):
    for y in range(height):
        z = heightmap[x][y] * MAX_HEIGHT # Höhe skalieren
        # Zentrieren: x und y so verschieben, dass Mitte bei 0 liegt
        x_coord = x - (width - 1) / 2
        y_coord = y - (height - 1) / 2
        vertices.append([x_coord, y_coord, z])
        # Steigung berechnen
        slope = compute_slope(heightmap, x, y)
        # Farbe bestimmen
        color = get_color(heightmap[x][y], slope)
        colors.append(color)

#die Verbindungen zwischen diesen Punkten.
#  sie sagen nur: „dieses Dreieck besteht aus Vertex A, Vertex B, Vertex C“.
for x in range(width - 1):
    for y in range(height - 1):
        i = x * height + y
        faces.append([i, i + 1, i + height])
        faces.append([i + 1, i + height + 1, i + height])


#---------------- Waldpunkte finden --------
waldalle= []
waldpunkte = []
for i in range (0,len(vertices)):
    h = heightmap[i // height, i % height]
    if 0.25 < h < 1.0:
        prob = 100 * np.exp(-((h - 0.35)**2) / (2 * 0.07**2))
        if random.random()*100 < prob:
            waldalle.append(vertices[i])

for i in range (0,2500):
    vx,vy,vz = random.choice(waldalle)
    dx = random.uniform(-0.5, 0.5)
    dy = random.uniform(-0.5, 0.5)
    
    # neue Position
    nx = vx + dx
    ny = vy + dy
    
    # Höhe neu bestimmen (nächster Terrainpunkt)
    ix = int(round(nx + (width - 1) / 2))
    iy = int(round(ny + (height - 1) / 2))
    
    if 0 <= ix < width and 0 <= iy < height:
        nz = heightmap[ix][iy] * MAX_HEIGHT
        waldpunkte.append([nx, ny, nz])

#-------------- Steinpunkte ----------------
steine= []
steinpunkte = []
for i in range (0,len(vertices)):
    h = heightmap[i // height, i % height]
    if 0.4 < h <  1.0:
        prob = 100 / (1 + np.exp(-15 * (h - 0.7)))
        if random.random()*100 < prob:
            steine.append(vertices[i])

for i in range (0,300):
    vx,vy,vz = random.choice(steine)
    dx = random.uniform(-0.5, 0.5)
    dy = random.uniform(-0.5, 0.5)
    
    # neue Position
    nx = vx + dx
    ny = vy + dy
    
    # Höhe neu bestimmen (nächster Terrainpunkt)
    ix = int(round(nx + (width - 1) / 2))
    iy = int(round(ny + (height - 1) / 2))
    
    if 0 <= ix < width and 0 <= iy < height:
        nz = heightmap[ix][iy] * MAX_HEIGHT
        steinpunkte.append([nx, ny, nz])

# ---------------- JSON Export ----------------
terrain_data = {
    'vertices': vertices,
    'faces': faces,
    'colors': colors,
    'tree': waldpunkte,
    'rocks': steinpunkte
}

with open('terrain.json', 'w') as f:
    json.dump(terrain_data, f)

print("✅ terrain.json erzeugt, Terrain ist zentriert.")
