"""Reviewer-authored concrete cases for the submitted algorithm."""


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
assert Strongest_Extension("Boundary", ["", "A", "a"]) == "Boundary.A"
assert Strongest_Extension("Tie", ["Ab", "Cd", "XYzz"]) == "Tie.Ab"
assert Strongest_Extension("Empty", []) == "Empty."
