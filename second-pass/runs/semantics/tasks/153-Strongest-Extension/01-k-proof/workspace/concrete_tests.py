def _extension_strength(extension):
    score = 0
    character = ""
    for character in extension:
        if character.isupper():
            score += 1
        if character.islower():
            score -= 1
    return score


def Strongest_Extension(class_name, extensions):
    strongest = extensions[0]
    strongest_strength = _extension_strength(strongest)
    extension = strongest
    score = strongest_strength
    for extension in extensions:
        score = _extension_strength(extension)
        if score > strongest_strength:
            strongest = extension
            strongest_strength = score
    return class_name + "." + strongest


assert Strongest_Extension(
    "Slices", ["SErviNGSliCes", "Cheese", "StuFfed"]
) == "Slices.SErviNGSliCes"
assert Strongest_Extension("my_class", ["AA", "Be", "CC"]) == "my_class.AA"
assert Strongest_Extension("X", ["abc", "AbC", "ZZ", "YY"]) == "X.ZZ"
assert Strongest_Extension("Tie", ["AA", "CC"]) == "Tie.AA"
assert Strongest_Extension("C", ["", "A", "BBb"]) == "C.A"
