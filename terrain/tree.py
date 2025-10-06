import numpy as np
import json
# -------- Variablen --------
axiom = "F"
rules = {
    "F": "FF+[+F-F-F]-[-F+F+F]",
}

# -------- L-System Funktion --------
def apply_lsystem(sentence, rules, iterations):
    for _ in range(iterations):
        next_sentence = ""
        for char in sentence:
            if char in rules:
                next_sentence += rules[char]
            else:
                next_sentence += char
        sentence = next_sentence
    return sentence

# -------- Baum Geometrie --------
vertices = [] # Liste der Punkte im Raum
faces = []    # Liste der Kanten zwischen den Punkten
startPosition = (0, 0, 0)
startAngle = np.array([0, 1, 0]) # erzeugt ein Array / Vektor
treeHeight = 2

def create_tree(sentence,startPosition=(0,0,0), startAngle=np.array([0,1,0]), treeHeight=2):
    stack = [] # Stack für Positionen und Winkel
    currentPosition = np.array(startPosition) # Aktuelle Position als Vektor
    currentAngle = np.array(startAngle)       # Aktueller Winkel als Vektor
    vertexIndex = 0                           # Index für die Vertices

    for char in sentence:
        if char == "F":
            newPosition = currentPosition + currentAngle * treeHeight
            vertices.append([float(currentPosition[0]), float(currentPosition[1]), float(currentPosition[2])])
            vertices.append([float(newPosition[0]), float(newPosition[1]), float(newPosition[2])])
            faces.append([int(vertexIndex), int(vertexIndex+1)])
            vertexIndex += 2
            currentPosition = newPosition
            treeHeight *= 0.9  # Verkleinert die Länge der Äste
        elif char == "+":
            # Winkel in Grad
            angle_deg = 25
            angle_rad = np.radians(angle_deg)
            # Rotation um Z-Achse
            Rz = np.array([
                 [np.cos(angle_rad), -np.sin(angle_rad), 0],
                 [np.sin(angle_rad),  np.cos(angle_rad), 0],
                 [0, 0, 1]
                 ])
             # Rotation um X-Achse (nach oben/unten)
            Rx = np.array([
                [1, 0, 0],
                [0, np.cos(angle_rad), -np.sin(angle_rad)],
                [0, np.sin(angle_rad),  np.cos(angle_rad)]
                ])
            # Rotation um Y-Achse (links/rechts)
            Ry = np.array([
                [np.cos(angle_rad), 0, np.sin(angle_rad)],
                [0, 1, 0],
                [-np.sin(angle_rad), 0, np.cos(angle_rad)]
                ])
            # Gesamtrotation: zuerst X, dann Y, dann Z
            rotMatrix = Rz @ Ry @ Rx
            currentAngle = rotMatrix @ currentAngle
        
        elif char == "-":
            angle_deg = -25
            angle_rad = np.radians(angle_deg)
            # Rotation um Z-Achse
            Rz = np.array([
                 [np.cos(angle_rad), -np.sin(angle_rad), 0],
                 [np.sin(angle_rad),  np.cos(angle_rad), 0],
                 [0, 0, 1]
                 ])
             # Rotation um X-Achse (nach oben/unten)
            Rx = np.array([
                [1, 0, 0],
                [0, np.cos(angle_rad), -np.sin(angle_rad)],
                [0, np.sin(angle_rad),  np.cos(angle_rad)]
                ])
            # Rotation um Y-Achse (links/rechts)
            Ry = np.array([
                [np.cos(angle_rad), 0, np.sin(angle_rad)],
                [0, 1, 0],
                [-np.sin(angle_rad), 0, np.cos(angle_rad)]
                ])
            # Gesamtrotation: zuerst X, dann Y, dann Z
            rotMatrix = Rz @ Ry @ Rx
            currentAngle = rotMatrix @ currentAngle
        
        elif char == "[":
            #neuen Ast beginnen: aktuelle Position und Winkel speichern
            stack.append((currentPosition.copy(), currentAngle.copy(), treeHeight))
        elif char == "]":
            currentPosition, currentAngle, treeHeight = stack.pop()


# -------- Generierung --------
lsystem_string = apply_lsystem(axiom, rules, 4)
create_tree(lsystem_string)     

# ---------------- JSON Export ----------------
tree_data = {
    "vertices": vertices,
    "faces": faces,
}

with open("tree.json", "w") as f:
    json.dump(tree_data, f)

print("✅ tree.json erzeugt, Baum ist bereit.")
