import numpy as np
import json
import random

# -------- L-System Funktion --------
def apply_lsystem(axiom, rules, iterations):
    for _ in range(iterations):
        next_sentence = ""
        for char in axiom:
            if char in rules:
                next_sentence += rules[char]
            else:
                next_sentence += char
        axiom= next_sentence
    return axiom

# -------- Baum Geometrie --------
def create_tree(sentence, startPosition=(0,0,0), startAngle=np.array([0,1,0]), treeHeight=1, startRadius=0.1):

    stack = []
    vertices = []
    faces = []
    radii = []
    leaves = []
    
    currentPosition = np.array(startPosition)
    currentAngle = np.array(startAngle)
    currentRadius = startRadius
    currentLength = treeHeight
    vertexIndex = 0

    for char in sentence:
        if char in "SF":
            newPosition = currentPosition + currentAngle * currentLength
            vertices.append([float(currentPosition[0]), float(currentPosition[1]), float(currentPosition[2])])
            vertices.append([float(newPosition[0]), float(newPosition[1]), float(newPosition[2])])
            faces.append([int(vertexIndex), int(vertexIndex+1)])
            vertexIndex += 2
            
            radii.append(currentRadius)
            radii.append(currentRadius * 0.7)

            currentPosition = newPosition

            if char == "S":  # Stamm
                currentLength *= random.uniform(0.9, 0.95)
                currentRadius *= random.uniform(1, 1)
            else:            # Äste
                currentLength *= random.uniform(0.6, 0.7)
                currentRadius *= random.uniform(0.4, 0.5)

        elif char in "+-<>^&": # Drehungen
            angle_deg = 25
            if char in "->^&":
                angle_deg *= -1
            angle_rad = np.radians(angle_deg)

            Rz = np.array([
                 [np.cos(angle_rad), -np.sin(angle_rad), 0],
                 [np.sin(angle_rad),  np.cos(angle_rad), 0],
                 [0, 0, 1]
            ])
            Rx = np.array([
                [1, 0, 0],
                [0, np.cos(angle_rad), -np.sin(angle_rad)],
                [0, np.sin(angle_rad),  np.cos(angle_rad)]
            ])
            Ry = np.array([
                [np.cos(angle_rad), 0, np.sin(angle_rad)],
                [0, 1, 0],
                [-np.sin(angle_rad), 0, np.cos(angle_rad)]
            ])
            #Matrixmultiplikation
            #Drehung in x Richtung
            if char in "+-":
                currentAngle = Rx @ currentAngle
            #Drehung in z Richtung
            elif char in "<>":
                currentAngle = Rz @ currentAngle
            #Drehung in y Richtung
            elif char in "^&":
                currentAngle = Ry @ currentAngle    

        elif char == "[": # Stack speichern
            stack.append((currentPosition.copy(), currentAngle.copy(), currentLength, currentRadius))

        elif char == "]":
            # Blatt nur an der Spitze des Astes
            if currentRadius < 0.15:  
                leaves.append([float(currentPosition[0]), float(currentPosition[1]), float(currentPosition[2])])
            currentPosition, currentAngle, currentLength, currentRadius = stack.pop()

    return {
        "vertices": vertices,
        "faces": faces,
        "radii": radii,
        "leaves": leaves}

