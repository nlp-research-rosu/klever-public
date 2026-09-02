def Strongest_Extension(class_name, extensions):
    strongest = ""
    best_strength = None
    extension = ""
    character = ""

    for extension in extensions:
        strength = 0

        for character in extension:
            if character.isupper():
                strength += 1
            elif character.islower():
                strength -= 1

        if best_strength is None or strength > best_strength:
            strongest = extension
            best_strength = strength

    return class_name + "." + strongest


assert Strongest_Extension(
    "Slices", ["SErviNGSliCes", "Cheese", "StuFfed"]
) == "Slices.SErviNGSliCes"
assert Strongest_Extension("my_class", ["AA", "Be", "CC"]) == "my_class.AA"
assert Strongest_Extension("C", ["", "Z"]) == "C.Z"
assert Strongest_Extension("C", ["", "z"]) == "C."
assert Strongest_Extension("C", ["9-_", ""]) == "C.9-_"
assert Strongest_Extension("C", ["Ab", "Cd", "XYzz"]) == "C.Ab"
assert Strongest_Extension("Empty", []) == "Empty."
