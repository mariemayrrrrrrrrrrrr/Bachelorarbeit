import json
import numpy as np
from perlin_noise import octave_perlin

# ---------------- Parameter ----------------
MAP_SIZE = (300, 300)  # Breite x Höhe
MAX_HEIGHT = 2.4       # Maximale Höhe des Terrains
SCALE = 100.0           # Skalenfaktor für Perlin Noise (größer = glatter)
EXPO = 1.1             # Höhenanpassung hebt Berge hervor
COLORS = {
    "water": [0, 0.3, 0.7],      # Blau
    "sand": [0.9, 0.85, 0.7], # Sandfarbe
    "grass": [0.1, 0.6, 0.1],      # Grün
    "forest": [0, 0.4, 0.1],   # Dunkelgrün
    "rock": [0.5, 0.5, 0.5], # Grau
    "snow": [1, 1, 1]        # Weiß
}

# ---------------- Perlin Noise ----------------
def update_point(x, y):
    return octave_perlin(x / SCALE, y / SCALE, octaves=6, persistence=0.5)

# ---------------- Normalisierung ----------------
#suchen den kleinsten wer im Array und teilen es durch den Größten um so werte zwischen 0-1 zu bekommen
def normalize(arr):
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))

# ---------------- get_color ----------------
def get_color(height, slope):
    if height > 0.25 and height < 0.9 and slope > 0.45:
        return COLORS["rock"]
    if height <= 0.1:              # weniger Wasser
        return COLORS["water"]
    elif height > 0.1 and height <= 0.15:
        return COLORS["sand"]
    elif height > 0.15 and height <= 0.5:
        return COLORS["grass"]      # mehr Grünfläche
    elif height > 0.5 and height <= 0.85:
        return COLORS["forest"]     # Wälder nur auf höheren Hügeln
    elif height > 0.85 and height <= 0.9:
        return COLORS["rock"]
    elif height > 0.9:
        return COLORS["snow"]


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

# ---------------- JSON Export ----------------
terrain_data = {
    'vertices': vertices,
    'faces': faces,
    'colors': colors
}

with open('terrain.json', 'w') as f:
    json.dump(terrain_data, f)

print("✅ terrain.json erzeugt, Terrain ist zentriert.")
