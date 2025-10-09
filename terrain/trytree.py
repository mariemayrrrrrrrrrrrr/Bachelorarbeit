import json
from tree import apply_lsystem, create_tree
import random
with open('terrain.json', 'r') as f:
    terrain_data = json.load(f)

vertices = terrain_data['vertices']
faces = terrain_data['faces']
colors = terrain_data['colors']

print('Colors', colors[1])

#-------- Startpunkte finden --------
waldalle= []
wald =[]

for i in range (0,len(colors),10):
    if colors[i] == [0, 0.4, 0.1]:
        waldalle.append(vertices[i])
    else:
        continue

for i in range (0,20):
    wald.append(random.choice(waldalle))


# --- Bäume generieren ---
axiom = "S"
rules = {
    "S": "FFF[+F][-F][&F][^F][<F][>F]",
    "F": "F[+F][-F][&F][^F][<F][>F]L"
}
forest = []
for position in wald:
    #iterations = random.randint(4,4)
    lsystem_string = apply_lsystem(axiom, rules, 4)
    array= ['lsystem_string', lsystem_string]
    tree_data = create_tree(lsystem_string, startPosition=(position[0], position[2]*20, position[1]),)
    forest.append(tree_data)
    print('Baum', position)
print('Anzahl Bäume', forest.__len__())
# --- Gesamt-Export ---

with open("forest.json", "w") as f:
    json.dump(forest, f)

print("✅ forest.json erzeugt – mehrere Bäume im Gelände platziert.")

