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

# Beispiel
result = apply_lsystem(axiom, rules, 2)
print(result)
